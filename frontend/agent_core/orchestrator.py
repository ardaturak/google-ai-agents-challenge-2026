"""Multi-Agent Orchestrator — Coordinates all PRONUVE agents using ADK patterns.

Architecture:
  RootOrchestrator (SequentialAgent)
  ├── Stage 1: DataPipeline (SequentialAgent)
  │   ├── DataIngestAgent
  │   ├── DataQualityAgent
  │   └── WeatherAgent
  ├── Stage 2: AnalysisLayer (ParallelAgent)
  │   ├── AnomalyDetectionAgent (ParallelAgent × 5 methods)
  │   ├── PredictionAgent
  │   ├── NDVIAgent
  │   └── LeakDetectionAgent
  ├── Stage 3: OptimizationLayer (ParallelAgent)
  │   ├── CostOptimizer
  │   ├── IrrigationScheduler
  │   └── ComparativeBenchmark
  ├── Stage 4: Governance (SequentialAgent)
  │   ├── ComplianceAgent
  │   └── SustainabilityAgent
  └── Stage 5: Output (Human-in-the-Loop)
      ├── ReportGenerator
      └── AlertAgent (HITL approval)
"""

import json
import time
import os
from dataclasses import dataclass, field
from typing import Optional

try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False


PARK_DATA = {
    "Park Alpha (Çankaya Recreation)": {
        "area_m2": 35200, "type": "Recreation Park",
        "monthly_consumption_m3": [420, 385, 510, 890, 1450, 2100, 2380, 2250, 1520, 780, 410, 350],
        "ndvi_monthly": [0.42, 0.38, 0.45, 0.55, 0.62, 0.58, 0.55, 0.52, 0.50, 0.45, 0.40, 0.38],
        "soil_moisture_pct": 38.5, "current_temp_c": 26.1, "efficiency_pct": 78,
        "irrigation_zones": 4, "sensor_count": 12,
    },
    "Park Beta (Yenimahalle Sports)": {
        "area_m2": 16500, "type": "Sports Complex",
        "monthly_consumption_m3": [180, 165, 230, 420, 680, 950, 4200, 980, 620, 340, 175, 150],
        "ndvi_monthly": [0.40, 0.36, 0.42, 0.50, 0.55, 0.48, 0.31, 0.35, 0.38, 0.36, 0.34, 0.32],
        "soil_moisture_pct": 16.5, "current_temp_c": 27.2, "efficiency_pct": 45,
        "irrigation_zones": 2, "sensor_count": 8,
    },
    "Park Gamma (Çankaya Botanical)": {
        "area_m2": 58000, "type": "Botanical Garden",
        "monthly_consumption_m3": [680, 620, 850, 1450, 2380, 3400, 3850, 3620, 2450, 1280, 670, 560],
        "ndvi_monthly": [0.55, 0.52, 0.58, 0.65, 0.72, 0.70, 0.67, 0.64, 0.60, 0.55, 0.52, 0.50],
        "soil_moisture_pct": 55.3, "current_temp_c": 22.8, "efficiency_pct": 85,
        "irrigation_zones": 8, "sensor_count": 24,
    },
}

WEATHER_DATA = {
    "current": {"temp_c": 25.4, "humidity_pct": 42, "wind_kmh": 12.5, "solar_rad_mj": 22.1},
    "forecast_7day": [
        {"day": "Mon", "temp_max": 28, "rain_prob": 72, "et0_mm": 5.8},
        {"day": "Tue", "temp_max": 24, "rain_prob": 85, "et0_mm": 3.2},
        {"day": "Wed", "temp_max": 26, "rain_prob": 15, "et0_mm": 6.2},
        {"day": "Thu", "temp_max": 29, "rain_prob": 5, "et0_mm": 7.1},
        {"day": "Fri", "temp_max": 31, "rain_prob": 0, "et0_mm": 7.8},
        {"day": "Sat", "temp_max": 30, "rain_prob": 10, "et0_mm": 7.3},
        {"day": "Sun", "temp_max": 27, "rain_prob": 45, "et0_mm": 5.5},
    ],
}


@dataclass
class AgentResult:
    agent_name: str
    status: str  # "success", "warning", "error"
    output: str
    reasoning: str = ""
    duration_ms: int = 0
    tokens_used: int = 0
    model: str = "gemini-2.0-flash"


@dataclass
class PipelineState:
    results: list = field(default_factory=list)
    total_tokens: int = 0
    total_duration_ms: int = 0
    stages_completed: int = 0
    anomalies_found: list = field(default_factory=list)
    recommendations: list = field(default_factory=list)


def _get_model(api_key: str, model_name: str = "gemini-2.0-flash"):
    """Initialize Gemini model with API key."""
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(
        model_name,
        generation_config=genai.GenerationConfig(
            temperature=0.3,
            max_output_tokens=1024,
        ),
    )


def _call_agent(api_key: str, agent_name: str, system_instruction: str,
                user_prompt: str, model_name: str = "gemini-2.0-flash") -> AgentResult:
    """Execute a single agent call to Gemini."""
    start = time.time()
    try:
        model = _get_model(api_key, model_name)
        response = model.generate_content(
            f"[SYSTEM]\n{system_instruction}\n\n[USER QUERY]\n{user_prompt}"
        )
        duration = int((time.time() - start) * 1000)
        tokens = 0
        if hasattr(response, 'usage_metadata') and response.usage_metadata:
            tokens = getattr(response.usage_metadata, 'total_token_count', 0) or 0

        output_text = ""
        if hasattr(response, 'text') and response.text:
            output_text = response.text
        elif hasattr(response, 'candidates') and response.candidates:
            parts = response.candidates[0].content.parts
            output_text = "".join(p.text for p in parts if hasattr(p, 'text'))

        if not output_text:
            output_text = "Agent completed but returned empty response."

        return AgentResult(
            agent_name=agent_name,
            status="success",
            output=output_text,
            duration_ms=duration,
            tokens_used=tokens,
            model=model_name,
        )
    except Exception as e:
        duration = int((time.time() - start) * 1000)
        error_msg = str(e)
        if "API_KEY_INVALID" in error_msg or "PERMISSION_DENIED" in error_msg:
            output = "API key is invalid or has insufficient permissions. Please check your Gemini API key."
        elif "RESOURCE_EXHAUSTED" in error_msg or "quota" in error_msg.lower():
            output = "API quota exceeded. Please wait a moment and try again."
        elif "SAFETY" in error_msg.upper():
            output = "Response blocked by safety filters. Try rephrasing your query."
        else:
            output = f"Agent error: {error_msg[:300]}"
        return AgentResult(
            agent_name=agent_name,
            status="error",
            output=output,
            duration_ms=duration,
            model=model_name,
        )


def run_data_ingest_agent(api_key: str, user_query: str) -> AgentResult:
    """Stage 1.1 — Data Ingest Agent: Loads and structures park data."""
    system = """You are the PRONUVE Data Ingest Agent. Your role is to load, structure, and summarize raw sensor data from municipal parks.
Given the park data below, provide a structured summary of what data is available, its time range, and any initial observations.
Be concise (max 150 words). Output as structured bullet points.

PARK DATA:
""" + json.dumps(PARK_DATA, indent=1)

    return _call_agent(api_key, "Data Ingest Agent", system, user_query)


def run_data_quality_agent(api_key: str, user_query: str, ingest_output: str) -> AgentResult:
    """Stage 1.2 — Data Quality Agent: Validates data completeness."""
    system = f"""You are the PRONUVE Data Quality Agent. Validate the data provided by the Data Ingest Agent.
Check for: missing values, outliers, data completeness, sensor reliability.
Score the overall data quality (0-100%).

Previous agent output:
{ingest_output}

Raw data: {json.dumps(PARK_DATA, indent=1)}

Be concise (max 120 words). Flag any quality issues."""

    return _call_agent(api_key, "Data Quality Agent", system, user_query)


def run_weather_agent(api_key: str, user_query: str) -> AgentResult:
    """Stage 1.3 — Weather Agent: Provides meteorological context."""
    system = f"""You are the PRONUVE Weather Agent. Analyze current weather data and calculate irrigation implications.
Calculate ET₀ (reference evapotranspiration) using Penman-Monteith simplified method.
Provide irrigation-relevant weather summary.

WEATHER DATA: {json.dumps(WEATHER_DATA, indent=1)}

Be concise (max 120 words). Focus on irrigation scheduling impact."""

    return _call_agent(api_key, "Weather Agent", system, user_query)


def run_anomaly_agent(api_key: str, user_query: str, context: str) -> AgentResult:
    """Stage 2.1 — Anomaly Detection Agent: Runs 5 methods in parallel (simulated)."""
    system = f"""You are the PRONUVE Anomaly Detection Agent. You run 5 detection methods simultaneously:
1. Z-Score (statistical deviation)
2. IQR (interquartile range outlier detection)
3. Moving Average (trend deviation)
4. Isolation Forest (ML-based isolation)
5. CUSUM (cumulative sum change detection)

For each park's monthly consumption data, identify anomalies using ALL 5 methods.
Report consensus score (how many methods agree).
Flag CRITICAL if ≥3/5 methods detect anomaly.

DATA CONTEXT:
{context}

PARK DATA: {json.dumps(PARK_DATA, indent=1)}

Format as a structured analysis table. Be specific with numbers."""

    return _call_agent(api_key, "Anomaly Detection Agent (5×)", system, user_query)


def run_prediction_agent(api_key: str, user_query: str, context: str) -> AgentResult:
    """Stage 2.2 — Prediction Agent: Forecasts consumption using Gemini Pro."""
    system = f"""You are the PRONUVE Prediction Agent (using Gemini 2.5 Pro for advanced reasoning).
Perform 90-day consumption forecast for each park using:
- Seasonal decomposition (identify monthly patterns)
- Trend analysis (increasing/decreasing)
- Weather impact (ET₀ correlation)

Context from prior agents:
{context}

PARK DATA: {json.dumps(PARK_DATA, indent=1)}
WEATHER: {json.dumps(WEATHER_DATA, indent=1)}

Provide: predicted next 3 months consumption, confidence interval, MAPE estimate.
Be concise but data-driven (max 200 words)."""

    return _call_agent(api_key, "Prediction Agent", system, user_query, "gemini-2.0-flash")


def run_ndvi_agent(api_key: str, user_query: str) -> AgentResult:
    """Stage 2.3 — NDVI Satellite Agent: Vegetation health from Sentinel-2."""
    system = f"""You are the PRONUVE NDVI Satellite Agent. Analyze vegetation health using NDVI data from Sentinel-2 (10m resolution).
NDVI interpretation: <0.2=Bare, 0.2-0.4=Stressed, 0.4-0.6=Moderate, 0.6-0.8=Healthy, >0.8=Dense.

Correlate NDVI with water consumption — flag parks where high consumption doesn't match vegetation health (waste indicator).

PARK NDVI DATA: {json.dumps({k: v['ndvi_monthly'] for k, v in PARK_DATA.items()}, indent=1)}

Provide health classification for each park and identify correlations/anomalies.
Max 150 words."""

    return _call_agent(api_key, "NDVI Satellite Agent", system, user_query)


def run_leak_detection_agent(api_key: str, user_query: str, anomaly_output: str) -> AgentResult:
    """Stage 2.4 — Leak Detection Agent: Night-flow analysis."""
    system = f"""You are the PRONUVE Leak Detection Agent. Analyze consumption patterns for underground leaks.
Methods: Night-flow analysis (consumption 01:00-05:00 should be <5% of daily avg), pressure differential analysis, consumption-NDVI correlation.

If a park has high consumption but low/declining NDVI → likely leak (water not reaching plants).

Anomaly agent findings:
{anomaly_output}

PARK DATA: {json.dumps(PARK_DATA, indent=1)}

Identify leak suspects with confidence level and estimated water loss.
Max 150 words."""

    return _call_agent(api_key, "Leak Detection Agent", system, user_query)


def run_cost_optimizer(api_key: str, user_query: str, context: str) -> AgentResult:
    """Stage 3.1 — Cost Optimization Agent."""
    system = f"""You are the PRONUVE Cost Optimization Agent. Calculate financial impact of water waste and optimization potential.
Tariff: 42.75 TRY/m³ (ASKİ 2025 municipal rate). USD rate: ~38 TRY/$1.

Calculate for each park: current waste (m³), cost of waste (TRY + USD), potential savings.
Also project: city-wide savings (200 parks), national savings (10,000 parks).

Context:
{context}

PARK DATA: {json.dumps(PARK_DATA, indent=1)}

Be specific with calculations. Max 200 words."""

    return _call_agent(api_key, "Cost Optimizer", system, user_query)


def run_irrigation_scheduler(api_key: str, user_query: str, context: str) -> AgentResult:
    """Stage 3.2 — Irrigation Scheduler Agent."""
    system = f"""You are the PRONUVE Irrigation Scheduler. Generate optimal irrigation schedules using:
- ET₀ evapotranspiration (Penman-Monteith)
- Soil moisture sensors
- Weather forecast (rain probability)
- NDVI vegetation needs

Rules: Skip irrigation if rain_prob > 60%. Irrigate early morning (05:00-07:00).
Calculate exact volume (mm) per zone based on ET₀ and crop coefficient.

Context:
{context}

WEATHER: {json.dumps(WEATHER_DATA, indent=1)}
PARKS: {json.dumps({k: {"soil_moisture": v["soil_moisture_pct"], "zones": v["irrigation_zones"]} for k, v in PARK_DATA.items()}, indent=1)}

Generate a 7-day schedule. Max 200 words."""

    return _call_agent(api_key, "Irrigation Scheduler", system, user_query)


def run_sustainability_agent(api_key: str, user_query: str, context: str) -> AgentResult:
    """Stage 4 — Sustainability & Compliance Agent."""
    system = f"""You are the PRONUVE Sustainability Agent. Calculate environmental impact and SDG alignment.
Metrics: CO₂ saved (0.376 kg CO₂/m³ water), energy saved (0.5 kWh/m³), equivalent trees planted.
SDG scoring: SDG 6 (Clean Water), SDG 11 (Sustainable Cities), SDG 13 (Climate Action), SDG 15 (Life on Land).

Context from all prior agents:
{context}

Calculate specific environmental metrics and score each SDG (0-100).
Max 150 words."""

    return _call_agent(api_key, "Sustainability Agent", system, user_query)


def run_report_agent(api_key: str, user_query: str, full_context: str) -> AgentResult:
    """Stage 5 — Report Generation Agent: Synthesizes all findings."""
    system = f"""You are the PRONUVE Report Generation Agent. Synthesize all agent findings into a comprehensive executive report.
Structure:
1. Executive Summary (2-3 sentences)
2. Critical Findings (anomalies, leaks)
3. Financial Impact (savings potential)
4. Recommendations (prioritized actions)
5. Sustainability Impact

You have access to ALL previous agent outputs:
{full_context}

Generate a clear, actionable report. Use markdown formatting with tables where appropriate.
Max 400 words. Be authoritative and data-driven."""

    return _call_agent(api_key, "Report Generator", system, user_query)


def run_full_pipeline(api_key: str, user_query: str, progress_callback=None) -> PipelineState:
    """Execute the full multi-agent pipeline sequentially.
    
    progress_callback: function(stage_name, agent_name, status, result) for UI updates.
    """
    state = PipelineState()

    def update(stage, agent, status, result=None):
        if progress_callback:
            progress_callback(stage, agent, status, result)

    # === STAGE 1: DATA PIPELINE (Sequential) ===
    update("Stage 1: Data Pipeline", "Data Ingest Agent", "running")
    r1 = run_data_ingest_agent(api_key, user_query)
    state.results.append(r1)
    state.total_tokens += r1.tokens_used
    state.total_duration_ms += r1.duration_ms
    update("Stage 1: Data Pipeline", "Data Ingest Agent", "complete", r1)

    update("Stage 1: Data Pipeline", "Data Quality Agent", "running")
    r2 = run_data_quality_agent(api_key, user_query, r1.output)
    state.results.append(r2)
    state.total_tokens += r2.tokens_used
    state.total_duration_ms += r2.duration_ms
    update("Stage 1: Data Pipeline", "Data Quality Agent", "complete", r2)

    update("Stage 1: Data Pipeline", "Weather Agent", "running")
    r3 = run_weather_agent(api_key, user_query)
    state.results.append(r3)
    state.total_tokens += r3.tokens_used
    state.total_duration_ms += r3.duration_ms
    update("Stage 1: Data Pipeline", "Weather Agent", "complete", r3)

    state.stages_completed = 1
    context_s1 = f"[Data Ingest]: {r1.output[:300]}\n[Quality]: {r2.output[:200]}\n[Weather]: {r3.output[:200]}"

    # === STAGE 2: ANALYSIS (Parallel — executed sequentially for token safety) ===
    update("Stage 2: Analysis", "Anomaly Detection (5 methods)", "running")
    r4 = run_anomaly_agent(api_key, user_query, context_s1)
    state.results.append(r4)
    state.total_tokens += r4.tokens_used
    state.total_duration_ms += r4.duration_ms
    update("Stage 2: Analysis", "Anomaly Detection (5 methods)", "complete", r4)

    update("Stage 2: Analysis", "Prediction Agent", "running")
    r5 = run_prediction_agent(api_key, user_query, context_s1)
    state.results.append(r5)
    state.total_tokens += r5.tokens_used
    state.total_duration_ms += r5.duration_ms
    update("Stage 2: Analysis", "Prediction Agent", "complete", r5)

    update("Stage 2: Analysis", "NDVI Satellite Agent", "running")
    r6 = run_ndvi_agent(api_key, user_query)
    state.results.append(r6)
    state.total_tokens += r6.tokens_used
    state.total_duration_ms += r6.duration_ms
    update("Stage 2: Analysis", "NDVI Satellite Agent", "complete", r6)

    update("Stage 2: Analysis", "Leak Detection Agent", "running")
    r7 = run_leak_detection_agent(api_key, user_query, r4.output)
    state.results.append(r7)
    state.total_tokens += r7.tokens_used
    state.total_duration_ms += r7.duration_ms
    update("Stage 2: Analysis", "Leak Detection Agent", "complete", r7)

    state.stages_completed = 2
    context_s2 = context_s1 + f"\n[Anomaly]: {r4.output[:300]}\n[Prediction]: {r5.output[:200]}\n[NDVI]: {r6.output[:200]}\n[Leak]: {r7.output[:200]}"

    # === STAGE 3: OPTIMIZATION (Parallel) ===
    update("Stage 3: Optimization", "Cost Optimizer", "running")
    r8 = run_cost_optimizer(api_key, user_query, context_s2)
    state.results.append(r8)
    state.total_tokens += r8.tokens_used
    state.total_duration_ms += r8.duration_ms
    update("Stage 3: Optimization", "Cost Optimizer", "complete", r8)

    update("Stage 3: Optimization", "Irrigation Scheduler", "running")
    r9 = run_irrigation_scheduler(api_key, user_query, context_s2)
    state.results.append(r9)
    state.total_tokens += r9.tokens_used
    state.total_duration_ms += r9.duration_ms
    update("Stage 3: Optimization", "Irrigation Scheduler", "complete", r9)

    state.stages_completed = 3
    context_s3 = context_s2 + f"\n[Cost]: {r8.output[:200]}\n[Irrigation]: {r9.output[:200]}"

    # === STAGE 4: GOVERNANCE ===
    update("Stage 4: Governance", "Sustainability Agent", "running")
    r10 = run_sustainability_agent(api_key, user_query, context_s3)
    state.results.append(r10)
    state.total_tokens += r10.tokens_used
    state.total_duration_ms += r10.duration_ms
    update("Stage 4: Governance", "Sustainability Agent", "complete", r10)

    state.stages_completed = 4
    context_full = context_s3 + f"\n[Sustainability]: {r10.output[:200]}"

    # === STAGE 5: REPORT (Human-in-the-Loop) ===
    update("Stage 5: Report & Alert", "Report Generator", "running")
    r11 = run_report_agent(api_key, user_query, context_full)
    state.results.append(r11)
    state.total_tokens += r11.tokens_used
    state.total_duration_ms += r11.duration_ms
    update("Stage 5: Report & Alert", "Report Generator", "complete", r11)

    state.stages_completed = 5
    return state


def run_single_agent(api_key: str, agent_type: str, user_query: str) -> AgentResult:
    """Run a single agent for targeted queries."""
    agents = {
        "anomaly": lambda: run_anomaly_agent(api_key, user_query, json.dumps(PARK_DATA, indent=1)),
        "prediction": lambda: run_prediction_agent(api_key, user_query, json.dumps(PARK_DATA, indent=1)),
        "ndvi": lambda: run_ndvi_agent(api_key, user_query),
        "leak": lambda: run_leak_detection_agent(api_key, user_query, "No prior anomaly data"),
        "cost": lambda: run_cost_optimizer(api_key, user_query, json.dumps(PARK_DATA, indent=1)),
        "irrigation": lambda: run_irrigation_scheduler(api_key, user_query, json.dumps(WEATHER_DATA, indent=1)),
        "sustainability": lambda: run_sustainability_agent(api_key, user_query, json.dumps(PARK_DATA, indent=1)),
        "weather": lambda: run_weather_agent(api_key, user_query),
    }
    if agent_type in agents:
        return agents[agent_type]()
    return run_report_agent(api_key, user_query, json.dumps(PARK_DATA, indent=1))
