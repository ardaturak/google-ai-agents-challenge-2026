"""PRONUVE Water Intelligence — Root Orchestrator Agent.

This is the main agent that coordinates all sub-agents using ADK patterns:
- SequentialAgent: Main analysis pipeline
- ParallelAgent: Anomaly detection (5 methods) + independent analyses
- LoopAgent: Continuous monitoring cycle
- Human-in-the-Loop: Alert approval
"""

from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent, LoopAgent

from agents.data_ingest_agent import data_ingest_agent
from agents.data_quality_agent import data_quality_agent
from agents.water_analysis_agent import water_analysis_agent
from agents.anomaly_agent import anomaly_detection_agent
from agents.prediction_agent import prediction_agent
from agents.ndvi_agent import ndvi_agent
from agents.leak_detection_agent import leak_detection_agent
from agents.weather_agent import weather_agent
from agents.cost_optimization_agent import cost_optimization_agent
from agents.irrigation_scheduler_agent import irrigation_scheduler_agent
from agents.comparative_agent import comparative_agent
from agents.compliance_agent import compliance_agent
from agents.sustainability_agent import sustainability_agent
from agents.report_agent import report_agent
from agents.alert_agent import alert_agent


# Stage 1: Data Collection & Validation (Sequential)
data_pipeline = SequentialAgent(
    name="data_pipeline",
    description="Collects data, validates quality, then enriches with weather",
    sub_agents=[
        data_ingest_agent,
        data_quality_agent,
        weather_agent,
    ],
)

# Stage 2: Analysis (Parallel — all independent analyses run simultaneously)
parallel_analysis = ParallelAgent(
    name="parallel_analysis",
    description="Runs water analysis, anomaly detection, predictions, NDVI, and leak detection in parallel",
    sub_agents=[
        water_analysis_agent,
        anomaly_detection_agent,
        prediction_agent,
        ndvi_agent,
        leak_detection_agent,
    ],
)

# Stage 3: Optimization (Parallel — independent optimization tasks)
optimization_layer = ParallelAgent(
    name="optimization_layer",
    description="Runs cost optimization, irrigation scheduling, and comparative analysis in parallel",
    sub_agents=[
        cost_optimization_agent,
        irrigation_scheduler_agent,
        comparative_agent,
    ],
)

# Stage 4: Governance (Sequential — compliance, then sustainability scoring)
governance_pipeline = SequentialAgent(
    name="governance_pipeline",
    description="Runs compliance checks and sustainability scoring",
    sub_agents=[
        compliance_agent,
        sustainability_agent,
    ],
)

# Full Pipeline: Stages 1-4 + Report + Alert
full_pipeline = SequentialAgent(
    name="full_pipeline",
    description="Runs the complete PRONUVE analysis pipeline: data → analysis → optimization → governance → report → alert",
    sub_agents=[
        data_pipeline,
        parallel_analysis,
        optimization_layer,
        governance_pipeline,
        report_agent,
        alert_agent,
    ],
)

# Monitoring Loop: Repeats the full pipeline every cycle
monitoring_loop = LoopAgent(
    name="monitoring_loop",
    description="Continuous monitoring — repeats the full pipeline at configured intervals (daily/weekly)",
    sub_agents=[full_pipeline],
    max_iterations=30,
)

# Root Orchestrator
root_agent = LlmAgent(
    name="pronuve_orchestrator",
    model="gemini-2.5-flash",
    description="PRONUVE Water Intelligence orchestrator — coordinates 15+ specialized agents for municipal water monitoring.",
    instruction="""You are the PRONUVE Water Intelligence Orchestrator.

You coordinate a multi-agent system for municipal water quality monitoring and optimization.

Your system includes:
1. DATA PIPELINE: Ingest → Quality Check → Weather Integration
2. ANALYSIS (Parallel): Water Analysis | Anomaly Detection (5 methods) | Prediction | NDVI | Leak Detection
3. OPTIMIZATION (Parallel): Cost Optimization | Irrigation Scheduling | Comparative Benchmarks
4. GOVERNANCE: Compliance | Sustainability Scoring
5. OUTPUT: Report Generation → Alert & Human Approval

When a user asks for analysis:
- Run the full_pipeline for complete assessment
- Or delegate to specific sub-agents for targeted queries

When monitoring is requested:
- Activate monitoring_loop for continuous daily/weekly checks

Important rules:
- All data is sourced from BigQuery (ASKİ water data + IoT sensors)
- All alerts require human approval before external dispatch
- Reports must include compliance and sustainability scores
- Anomaly detection uses 5-method consensus (Z-Score, IQR, MA, Isolation Forest, CUSUM)
- Park data is anonymized by default; real identifiers only shared with authorized users
""",
    sub_agents=[full_pipeline, monitoring_loop],
)
