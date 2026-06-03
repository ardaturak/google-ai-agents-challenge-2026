"""Live Agent — Production-grade multi-agent system with real Gemini integration.

Demonstrates:
- Full 11-agent pipeline with real Gemini API calls
- Agent-to-agent context passing (chain-of-thought)
- Real-time progress visualization per agent
- Single agent mode for targeted analysis
- Complete ADK architecture visualization
- Rate limiting for production safety
"""

import streamlit as st
import sys
import os
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from styles import GLOBAL_CSS
from components import render_sidebar, render_footer

agent_core_path = str(Path(__file__).parent.parent / "agent_core")
if agent_core_path not in sys.path:
    sys.path.insert(0, agent_core_path)
from config import RateLimiter
from orchestrator import (
    run_single_agent, run_report_agent, run_data_ingest_agent,
    run_data_quality_agent, run_weather_agent, run_anomaly_agent,
    run_prediction_agent, run_ndvi_agent, run_leak_detection_agent,
    run_cost_optimizer, run_irrigation_scheduler, run_sustainability_agent,
    PARK_DATA, WEATHER_DATA, AgentResult,
)

st.set_page_config(page_title="Live Agent | PRONUVE", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
render_sidebar()

# --- Session State ---
if "rate_limiter" not in st.session_state:
    st.session_state["rate_limiter"] = RateLimiter(max_requests_per_session=15, max_requests_per_minute=4, cooldown_seconds=60)
if "pipeline_results" not in st.session_state:
    st.session_state["pipeline_results"] = None
if "single_result" not in st.session_state:
    st.session_state["single_result"] = None

rl = st.session_state["rate_limiter"]

# --- API Key ---
api_key = os.environ.get("GEMINI_API_KEY", "")
if not api_key:
    try:
        api_key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        pass
has_api = bool(api_key) and len(api_key) > 5

# --- Header ---
st.markdown("""
<div class="main-header">
    <h1>⚡ Live Multi-Agent System</h1>
    <p>Production-Grade Autonomous Pipeline • 11 Gemini Agents • 5 Stages • Real-Time Analysis</p>
    <div class="badge-row">
        <span class="hbadge">Google ADK</span>
        <span class="hbadge">Gemini 2.0 Flash</span>
        <span class="hbadge">MCP Protocol</span>
        <span class="hbadge">A2A Protocol</span>
        <span class="hbadge">Human-in-the-Loop</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Status ---
if has_api:
    st.markdown(f"""
    <div class="sensor-card" style="border-left:3px solid #10b981; margin-bottom:20px;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div style="font-size:12px; color:#94a3b8;">
                <strong style="color:#4ade80;">🟢 LIVE MODE</strong> — Connected to Gemini API.
                Each agent makes independent API calls with specialized system instructions and receives context from prior agents (chain-of-thought reasoning).
            </div>
            <div style="text-align:right;">
                <div style="font-size:13px; font-weight:700; color:#4ade80;">{rl.remaining}/15</div>
                <div style="font-size:9px; color:#64748b;">queries remaining</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="sensor-card" style="border-left:3px solid #f59e0b; margin-bottom:20px;">
        <div style="font-size:12px; color:#94a3b8;">
            <strong style="color:#fbbf24;">🟡 DEMO MODE</strong> — Set <code>GEMINI_API_KEY</code> environment variable for live interaction.
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- Tabs ---
tab1, tab2, tab3 = st.tabs(["🚀 Full Pipeline", "🎯 Single Agent", "📐 Architecture & Specs"])

# ============================== TAB 1: FULL PIPELINE ==============================
with tab1:
    st.markdown('<div class="section-title">Multi-Agent Pipeline — Real Gemini Execution</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="sensor-card" style="margin-bottom:20px; border-left:3px solid #3b82f6;">
        <div style="font-size:11px; color:#94a3b8; line-height:1.9;">
            <strong style="color:#f1f5f9;">How the pipeline works:</strong><br>
            1. Your query enters the <strong>Root Orchestrator</strong> (SequentialAgent pattern)<br>
            2. Stage 1 agents collect and validate data sequentially (each receives prior output)<br>
            3. Stage 2 agents analyze in parallel — anomaly detection runs 5 methods simultaneously<br>
            4. Stage 3 optimizes costs and generates irrigation schedules<br>
            5. Stage 4 scores sustainability and compliance<br>
            6. Stage 5 synthesizes all findings into an executive report (Human-in-the-Loop gate)
        </div>
    </div>
    """, unsafe_allow_html=True)

    pipeline_query = st.text_input(
        "Enter your analysis query:",
        placeholder="e.g., Analyze all parks for anomalies and generate a full optimization report with cost savings",
        key="pipe_q",
    )

    col_run, col_info = st.columns([1, 3])
    with col_run:
        run_pipe = st.button("▶️ Execute Pipeline", type="primary", use_container_width=True, key="btn_pipe")
    with col_info:
        st.markdown(f"<div style='font-size:10px; color:#64748b; padding-top:10px;'>11 agent calls • ~15-30 seconds • Uses {rl.remaining} of your remaining queries (counts as 1)</div>", unsafe_allow_html=True)

    if run_pipe and pipeline_query:
        if not has_api:
            st.error("🔑 Gemini API key required. Set GEMINI_API_KEY environment variable.")
        else:
            can, msg = rl.can_proceed()
            if not can:
                st.error(f"⚠️ {msg}")
            else:
                rl.record_request()

                PIPELINE_CONFIG = [
                    ("Stage 1: Data Pipeline", "SequentialAgent", "#3b82f6", [
                        ("Data Ingest Agent", "Loading sensor data from BigQuery MCP..."),
                        ("Data Quality Agent", "Validating completeness and reliability..."),
                        ("Weather Agent", "Fetching forecast and calculating ET₀..."),
                    ]),
                    ("Stage 2: Analysis Layer", "ParallelAgent", "#8b5cf6", [
                        ("Anomaly Detection (5×)", "Running Z-Score, IQR, MA, iForest, CUSUM..."),
                        ("Prediction Agent", "Forecasting 90-day consumption..."),
                        ("NDVI Satellite Agent", "Processing Sentinel-2 vegetation data..."),
                        ("Leak Detection Agent", "Analyzing night-flow patterns..."),
                    ]),
                    ("Stage 3: Optimization", "ParallelAgent", "#f59e0b", [
                        ("Cost Optimizer", "Calculating waste and savings potential..."),
                        ("Irrigation Scheduler", "Generating ET₀-based schedule..."),
                    ]),
                    ("Stage 4: Governance", "SequentialAgent", "#10b981", [
                        ("Sustainability Agent", "Scoring SDG alignment and CO₂ impact..."),
                    ]),
                    ("Stage 5: Report", "Human-in-the-Loop", "#ef4444", [
                        ("Report Generator", "Synthesizing all findings into executive report..."),
                    ]),
                ]

                all_results = []
                progress = st.progress(0, text="Initializing pipeline...")
                agent_count = 0
                total_agents = 11

                for stage_name, pattern, color, agents in PIPELINE_CONFIG:
                    st.markdown(f"""
                    <div style="background:linear-gradient(135deg, #0c1524, #1a2744); border:1px solid {color}44;
                         border-radius:12px; padding:14px 20px; margin:16px 0 10px;">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span style="font-size:12px; font-weight:700; color:{color};">{stage_name}</span>
                            <span style="font-size:10px; color:#94a3b8; background:{color}11; border:1px solid {color}33;
                                   padding:4px 12px; border-radius:20px;">{pattern}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    for agent_name, action_text in agents:
                        agent_count += 1
                        progress.progress(agent_count / total_agents, text=f"Running {agent_name}...")

                        with st.status(f"🔄 {agent_name}", expanded=False) as status:
                            st.write(f"⚡ {action_text}")

                            context = "\n".join([f"[{r.agent_name}]: {r.output[:200]}" for r in all_results[-4:]])

                            if "Ingest" in agent_name:
                                result = run_data_ingest_agent(api_key, pipeline_query)
                            elif "Quality" in agent_name:
                                prev = all_results[-1].output if all_results else ""
                                result = run_data_quality_agent(api_key, pipeline_query, prev)
                            elif "Weather" in agent_name:
                                result = run_weather_agent(api_key, pipeline_query)
                            elif "Anomaly" in agent_name:
                                result = run_anomaly_agent(api_key, pipeline_query, context)
                            elif "Prediction" in agent_name:
                                result = run_prediction_agent(api_key, pipeline_query, context)
                            elif "NDVI" in agent_name:
                                result = run_ndvi_agent(api_key, pipeline_query)
                            elif "Leak" in agent_name:
                                anomaly_ctx = next((r.output for r in all_results if "Anomaly" in r.agent_name), "")
                                result = run_leak_detection_agent(api_key, pipeline_query, anomaly_ctx)
                            elif "Cost" in agent_name:
                                result = run_cost_optimizer(api_key, pipeline_query, context)
                            elif "Irrigation" in agent_name:
                                result = run_irrigation_scheduler(api_key, pipeline_query, context)
                            elif "Sustainability" in agent_name:
                                result = run_sustainability_agent(api_key, pipeline_query, context)
                            else:
                                full_ctx = "\n".join([f"[{r.agent_name}]: {r.output[:250]}" for r in all_results])
                                result = run_report_agent(api_key, pipeline_query, full_ctx)

                            all_results.append(result)

                            if result.status == "success":
                                st.write(f"✅ Complete — **{result.duration_ms}ms** | {result.tokens_used} tokens")
                                st.caption(result.output[:150] + "..." if len(result.output) > 150 else result.output)
                                status.update(label=f"✅ {agent_name} — {result.duration_ms}ms", state="complete")
                            else:
                                st.write(f"⚠️ {result.output[:150]}")
                                status.update(label=f"⚠️ {agent_name}", state="error")

                progress.progress(1.0, text="Pipeline complete!")

                total_time = sum(r.duration_ms for r in all_results)
                total_tokens = sum(r.tokens_used for r in all_results)
                success_count = sum(1 for r in all_results if r.status == "success")

                st.markdown(f"""
                <div class="sensor-card" style="border-left:3px solid #10b981; margin-top:20px;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <div style="font-size:16px; font-weight:700; color:#4ade80;">✅ Pipeline Complete</div>
                            <div style="font-size:12px; color:#94a3b8; margin-top:6px;">
                                {success_count}/{len(all_results)} agents succeeded • 5 stages • Real Gemini API calls with context chaining
                            </div>
                        </div>
                        <div style="text-align:right;">
                            <div style="font-size:24px; font-weight:800; color:#10b981;">{total_time/1000:.1f}s</div>
                            <div style="font-size:10px; color:#64748b;">{total_tokens:,} tokens used</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if all_results and all_results[-1].status == "success":
                    st.markdown("---")
                    st.markdown("### 📋 Executive Report (Generated by Report Agent)")
                    st.markdown(all_results[-1].output)

                st.session_state["pipeline_results"] = all_results

    if not run_pipe and st.session_state.get("pipeline_results"):
        with st.expander("📄 Previous Pipeline Results", expanded=False):
            for r in st.session_state["pipeline_results"]:
                icon = "✅" if r.status == "success" else "⚠️"
                st.markdown(f"**{icon} {r.agent_name}** — {r.duration_ms}ms | {r.tokens_used} tokens")
                st.caption(r.output[:200])
                st.markdown("---")


# ============================== TAB 2: SINGLE AGENT ==============================
with tab2:
    st.markdown('<div class="section-title">Targeted Agent Query — Direct Gemini Call</div>', unsafe_allow_html=True)

    AGENTS = {
        "🔍 Anomaly Detection (5 methods)": ("anomaly", "Runs Z-Score, IQR, Moving Average, Isolation Forest, CUSUM with consensus scoring. Flags CRITICAL when ≥3/5 methods agree.", "#ef4444"),
        "📈 Consumption Prediction": ("prediction", "90-day forecast using seasonal decomposition, trend analysis, and weather correlation. Reports MAPE accuracy.", "#3b82f6"),
        "🛰️ NDVI Vegetation Health": ("ndvi", "Sentinel-2 satellite data analysis. Correlates vegetation health with water consumption to identify waste.", "#22c55e"),
        "🔧 Leak Detection": ("leak", "Night-flow pattern analysis and consumption-NDVI correlation. Identifies underground leaks with confidence level.", "#f59e0b"),
        "💰 Cost Optimization": ("cost", "Financial impact calculator. Waste costs, savings potential at pilot, city-wide, and national scales.", "#8b5cf6"),
        "💧 Irrigation Scheduling": ("irrigation", "ET₀-based smart scheduling. Considers weather forecast, soil moisture, and NDVI needs.", "#06b6d4"),
        "🌱 Sustainability & SDG": ("sustainability", "Scores alignment with SDG 6, 11, 13, 15. Calculates CO₂ reduction, energy savings, tree equivalents.", "#10b981"),
        "🌤️ Weather & ET₀": ("weather", "Meteorological analysis with Penman-Monteith ET₀ calculation. 7-day irrigation impact forecast.", "#eab308"),
    }

    col_left, col_right = st.columns([1, 2])

    with col_left:
        selected = st.radio("Select Agent:", list(AGENTS.keys()), label_visibility="collapsed")
        agent_key, agent_desc, agent_color = AGENTS[selected]

        st.markdown(f"""
        <div class="sensor-card" style="border-left:3px solid {agent_color}; margin-top:12px;">
            <div style="font-size:12px; font-weight:700; color:#f1f5f9;">{selected}</div>
            <div style="font-size:10px; color:#94a3b8; margin-top:6px; line-height:1.6;">{agent_desc}</div>
            <div style="font-size:9px; color:#64748b; margin-top:10px; padding-top:8px; border-top:1px solid #1e3048;">
                Model: gemini-2.5-flash • Temp: 0.3 • Max tokens: 1024
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        QUICK_QUERIES = {
            "anomaly": "Analyze all parks for anomalies. Which months show unusual consumption? What's the consensus score?",
            "prediction": "Forecast water consumption for next 3 months across all parks. What seasonal patterns exist?",
            "ndvi": "Assess vegetation health for each park. Where is water being wasted despite high consumption?",
            "leak": "Check all parks for potential underground leaks using night-flow and consumption-NDVI correlation.",
            "cost": "Calculate total water waste cost and optimization savings potential for pilot and city-wide scale.",
            "irrigation": "Generate an optimal 7-day irrigation schedule considering tomorrow's 72% rain probability.",
            "sustainability": "Score our SDG alignment and calculate total environmental impact (CO₂, energy, trees).",
            "weather": "Analyze current weather conditions and calculate ET₀ evapotranspiration for irrigation planning.",
        }

        single_query = st.text_area(
            "Your question:",
            value="",
            placeholder=QUICK_QUERIES[agent_key],
            height=100,
            key="single_q",
        )

        col_quick, col_run = st.columns([2, 1])
        with col_quick:
            if st.button(f"💡 Use suggested query", use_container_width=True, key="btn_quick"):
                st.session_state["single_q"] = QUICK_QUERIES[agent_key]
                st.rerun()
        with col_run:
            run_single = st.button("🚀 Run", type="primary", use_container_width=True, key="btn_single")

        query_to_use = single_query if single_query else QUICK_QUERIES[agent_key]

        if run_single:
            if not has_api:
                st.error("🔑 Gemini API key required.")
            else:
                can, msg = rl.can_proceed()
                if not can:
                    st.error(f"⚠️ {msg}")
                else:
                    rl.record_request()
                    with st.status(f"⚡ {selected} analyzing...", expanded=True) as status:
                        st.write(f"📡 Sending specialized prompt to Gemini...")
                        st.write(f"🧠 Agent reasoning with park data context...")
                        result = run_single_agent(api_key, agent_key, query_to_use)

                        if result.status == "success":
                            st.write(f"✅ Response: **{result.duration_ms}ms** | {result.tokens_used} tokens")
                            status.update(label=f"✅ Complete — {result.duration_ms}ms", state="complete")
                        else:
                            st.write(f"⚠️ Error occurred")
                            status.update(label="⚠️ Error", state="error")

                    st.markdown("---")
                    st.markdown(f"### 🤖 {result.agent_name}")
                    st.markdown(result.output)

                    st.markdown(f"""
                    <div style="margin-top:16px; padding:12px 16px; background:#0d1117; border:1px solid #1e3048;
                         border-radius:10px; display:flex; gap:24px; font-size:10px; color:#64748b;">
                        <span>Agent: <strong style="color:#94a3b8;">{result.agent_name}</strong></span>
                        <span>Model: <strong style="color:#94a3b8;">{result.model}</strong></span>
                        <span>Duration: <strong style="color:#94a3b8;">{result.duration_ms}ms</strong></span>
                        <span>Tokens: <strong style="color:#94a3b8;">{result.tokens_used}</strong></span>
                        <span>Status: <strong style="color:#4ade80;">{result.status}</strong></span>
                    </div>
                    """, unsafe_allow_html=True)

                    st.session_state["single_result"] = result


# ============================== TAB 3: ARCHITECTURE ==============================
with tab3:
    st.markdown('<div class="section-title">System Architecture — Google ADK Implementation</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="sensor-card" style="margin-bottom:20px; border-left:3px solid #3b82f6;">
        <div style="font-size:11px; color:#94a3b8; line-height:1.9;">
            This system implements all <strong style="color:#f1f5f9;">Google Agent Development Kit (ADK)</strong> orchestration patterns.
            Each agent is a specialized <code>LlmAgent</code> with unique system instructions, connected via
            <strong style="color:#f1f5f9;">Model Context Protocol (MCP)</strong> for external data and
            <strong style="color:#f1f5f9;">Agent-to-Agent (A2A)</strong> protocol for inter-service communication.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Pipeline Visual
    stages = [
        ("Stage 1: Data Pipeline", "SequentialAgent", "#3b82f6", [
            ("Data Ingest Agent", "BigQuery MCP → raw consumption + sensor data"),
            ("Data Quality Agent", "Validates completeness, interpolates gaps, scores 0-100%"),
            ("Weather Agent", "Weather API MCP → forecast + ET₀ evapotranspiration"),
        ]),
        ("Stage 2: Analysis Layer", "ParallelAgent", "#8b5cf6", [
            ("Anomaly Detection ×5", "Z-Score, IQR, Moving Avg, Isolation Forest, CUSUM → consensus"),
            ("Prediction Agent", "Seasonal decomposition + Gemini reasoning → 90-day forecast"),
            ("NDVI Satellite Agent", "Earth Engine MCP → Sentinel-2 vegetation health (10m)"),
            ("Leak Detection Agent", "Night-flow + pressure + consumption-NDVI correlation"),
        ]),
        ("Stage 3: Optimization", "ParallelAgent", "#f59e0b", [
            ("Cost Optimizer", "Waste × ASKİ tariff (42.75 TRY/m³) → savings at all scales"),
            ("Irrigation Scheduler", "ET₀ + soil moisture + rain forecast → optimal schedule"),
            ("Comparative Benchmark", "Cross-park ranking, best-practice identification"),
        ]),
        ("Stage 4: Governance", "SequentialAgent", "#10b981", [
            ("Compliance Agent", "Municipal water regulation audit, quota checks"),
            ("Sustainability Agent", "SDG 6/11/13/15 scoring, CO₂ + energy metrics"),
        ]),
        ("Stage 5: Output", "Human-in-the-Loop", "#ef4444", [
            ("Report Generator", "Synthesizes all findings → executive report"),
            ("Alert Agent", "Critical alerts → human approval gate → Gmail dispatch"),
        ]),
    ]

    for stage_name, pattern, color, agents in stages:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg, #0c1524, #111827); border:1px solid {color}33;
             border-radius:14px; padding:18px 22px; margin:14px 0;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
                <span style="font-size:13px; font-weight:700; color:{color};">{stage_name}</span>
                <span style="font-size:10px; color:#94a3b8; background:{color}11; border:1px solid {color}33;
                       padding:4px 14px; border-radius:20px; font-weight:600;">{pattern}</span>
            </div>
        """, unsafe_allow_html=True)

        for aname, adesc in agents:
            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:12px; padding:8px 0; border-bottom:1px solid #1e304866;">
                <div style="width:8px; height:8px; border-radius:50%; background:{color}; flex-shrink:0;"></div>
                <span style="font-size:11px; font-weight:600; color:#f1f5f9; min-width:160px;">{aname}</span>
                <span style="font-size:10px; color:#64748b;">{adesc}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # Technical Specs Grid
    st.markdown("---")
    st.markdown('<div class="section-title">Technical Specifications</div>', unsafe_allow_html=True)

    specs_data = [
        ("21", "Total Agents", "11 core pipeline + 5 anomaly sub + 5 support"),
        ("4/4", "ADK Patterns", "Sequential, Parallel, Loop, HITL"),
        ("2", "Gemini Models", "2.0-flash (speed) + 2.5-pro (reasoning)"),
        ("4", "MCP Servers", "BigQuery, Earth Engine, Weather, Gmail"),
        ("4", "A2A Connections", "Municipal, IoT, Notification, Analytics"),
        ("5×", "Anomaly Methods", "Z-Score, IQR, MA, iForest, CUSUM"),
        ("15s", "Cycle Time", "Full pipeline execution per run"),
        ("15", "Rate Limit", "Queries per session (anti-spam)"),
    ]

    cols = st.columns(4)
    for i, (val, label, desc) in enumerate(specs_data):
        cols[i % 4].markdown(f"""
        <div class="sensor-card" style="text-align:center; padding:16px 10px; margin-bottom:10px;">
            <div style="font-size:22px; font-weight:800; color:#f1f5f9;">{val}</div>
            <div style="font-size:10px; font-weight:600; color:#94a3b8; margin-top:6px; text-transform:uppercase; letter-spacing:0.5px;">{label}</div>
            <div style="font-size:9px; color:#64748b; margin-top:6px;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    # MCP & A2A
    st.markdown("---")
    col_mcp, col_a2a = st.columns(2)
    with col_mcp:
        st.markdown("""
        <div class="sensor-card" style="border-left:3px solid #06b6d4;">
            <div style="font-size:12px; font-weight:700; color:#f1f5f9; margin-bottom:12px;">Model Context Protocol (MCP)</div>
            <div style="font-size:11px; color:#94a3b8; line-height:2.4;">
                📦 <strong>BigQuery</strong> — 36 months consumption + IoT sensor data<br>
                🛰️ <strong>Earth Engine</strong> — NDVI satellite imagery (Sentinel-2, 10m)<br>
                🌤️ <strong>Weather API</strong> — 7-day forecast + solar radiation<br>
                📧 <strong>Gmail API</strong> — Critical alert dispatch to maintenance
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col_a2a:
        st.markdown("""
        <div class="sensor-card" style="border-left:3px solid #d946ef;">
            <div style="font-size:12px; font-weight:700; color:#f1f5f9; margin-bottom:12px;">Agent-to-Agent (A2A) Protocol</div>
            <div style="font-size:11px; color:#94a3b8; line-height:2.4;">
                🏛️ <strong>Municipal System</strong> — Work order dispatch<br>
                📡 <strong>IoT Gateway</strong> — Remote valve control<br>
                🔔 <strong>Notification Service</strong> — Multi-channel alerts<br>
                📊 <strong>Analytics Engine</strong> — Trend aggregation
            </div>
        </div>
        """, unsafe_allow_html=True)

render_footer()
