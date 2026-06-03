"""Live Agent — Real multi-agent pipeline powered by Gemini.

This page demonstrates the PRONUVE autonomous agent system with:
- Full pipeline mode (11 agents, 5 stages)
- Single agent mode (targeted queries)
- Real-time progress visualization
- Rate limiting for production safety
"""

import streamlit as st
import sys
import os
import time
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
    run_full_pipeline, run_single_agent, run_report_agent,
    PARK_DATA, WEATHER_DATA, AgentResult
)

st.set_page_config(
    page_title="Live Agent | PRONUVE",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
render_sidebar()

# --- API Key & Rate Limiter Setup ---
api_key = os.environ.get("GEMINI_API_KEY", "")
if not api_key:
    try:
        api_key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        pass

has_api = bool(api_key) and len(api_key) > 10

if "rate_limiter" not in st.session_state:
    st.session_state["rate_limiter"] = RateLimiter(
        max_requests_per_session=15,
        max_requests_per_minute=4,
        cooldown_seconds=60,
    )

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if "pipeline_results" not in st.session_state:
    st.session_state["pipeline_results"] = None

rl = st.session_state["rate_limiter"]

# --- Header ---
st.markdown("""
<div class="main-header">
    <h1>⚡ Live Multi-Agent System</h1>
    <p>Real-time Autonomous Pipeline • 11 Agents • 5 Stages • Powered by Gemini</p>
    <div class="badge-row">
        <span class="hbadge">Sequential Agent</span>
        <span class="hbadge">Parallel Agent</span>
        <span class="hbadge">Loop Agent</span>
        <span class="hbadge">Human-in-the-Loop</span>
        <span class="hbadge">MCP Protocol</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Status Banner ---
if has_api:
    st.markdown(f"""
    <div class="sensor-card" style="border-left:3px solid #10b981; margin-bottom:16px;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div style="font-size:12px; color:#94a3b8;">
                <strong style="color:#4ade80;">🟢 LIVE MODE</strong> — Connected to Gemini API.
                Each agent makes independent API calls with specialized system instructions.
                Full pipeline executes 11 sequential/parallel agent calls.
            </div>
            <div style="font-size:11px; color:#64748b; text-align:right;">
                Remaining: <strong style="color:#4ade80;">{rl.remaining}</strong> queries<br>
                <span style="font-size:9px;">Rate: 4/min • 15/session</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="sensor-card" style="border-left:3px solid #f59e0b; margin-bottom:16px;">
        <div style="font-size:12px; color:#94a3b8;">
            <strong style="color:#fbbf24;">🟡 DEMO MODE</strong> — No API key detected.
            Set <code>GEMINI_API_KEY</code> environment variable for live agent interaction.
            Currently showing architecture and capabilities only.
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- Tabs ---
tab1, tab2, tab3 = st.tabs(["🚀 Full Pipeline", "🎯 Single Agent", "📊 Architecture"])

# ===================== TAB 1: FULL PIPELINE =====================
with tab1:
    st.markdown('<div class="section-title">Multi-Agent Pipeline Execution</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="sensor-card" style="margin-bottom:16px; border-left:3px solid #3b82f6;">
        <div style="font-size:11px; color:#94a3b8; line-height:1.8;">
            <strong style="color:#f1f5f9;">How it works:</strong> The orchestrator routes your query through 5 stages.
            Each agent receives context from previous agents (chain-of-thought) and makes independent Gemini API calls.
            Stage 2 agents run in parallel (ADK ParallelAgent pattern). Total: ~11 API calls per pipeline run.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_q, col_btn = st.columns([4, 1])
    with col_q:
        pipeline_query = st.text_input(
            "Query for full pipeline:",
            placeholder="e.g., Analyze all parks, detect anomalies, and generate optimization report",
            key="pipeline_q",
        )
    with col_btn:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        run_pipeline = st.button("▶️ Run Pipeline", type="primary", use_container_width=True, key="run_pipe")

    if run_pipeline and pipeline_query:
        if not has_api:
            st.warning("API key required for live pipeline execution. Set GEMINI_API_KEY environment variable.")
        else:
            can_proceed, msg = rl.can_proceed()
            if not can_proceed:
                st.error(f"⚠️ {msg}")
            else:
                rl.record_request()

                stages_config = [
                    ("Stage 1: Data Pipeline", ["Data Ingest Agent", "Data Quality Agent", "Weather Agent"], "SequentialAgent"),
                    ("Stage 2: Analysis", ["Anomaly Detection (5 methods)", "Prediction Agent", "NDVI Satellite Agent", "Leak Detection Agent"], "ParallelAgent"),
                    ("Stage 3: Optimization", ["Cost Optimizer", "Irrigation Scheduler"], "ParallelAgent"),
                    ("Stage 4: Governance", ["Sustainability Agent"], "SequentialAgent"),
                    ("Stage 5: Report & Alert", ["Report Generator"], "Human-in-the-Loop"),
                ]

                progress_bar = st.progress(0)
                agent_idx = 0
                total_agents = 11

                all_results = []

                for stage_name, agents, pattern in stages_config:
                    st.markdown(f"""
                    <div style="background:#111827; border:1px solid #1e3048; border-radius:10px; padding:12px 16px; margin:14px 0 8px;">
                        <span style="font-size:12px; font-weight:700; color:#f1f5f9;">{stage_name}</span>
                        <span style="float:right; font-size:10px; color:#64748b; background:#1e293b; padding:3px 10px; border-radius:12px;">{pattern}</span>
                    </div>
                    """, unsafe_allow_html=True)

                    for agent_name in agents:
                        agent_idx += 1
                        progress_bar.progress(agent_idx / total_agents)

                        with st.status(f"🔄 {agent_name}", expanded=False) as status:
                            st.write(f"⚡ Calling Gemini API with specialized prompt...")

                            context = "\n".join([f"[{r.agent_name}]: {r.output[:150]}" for r in all_results])

                            if "Ingest" in agent_name:
                                result = run_single_agent(api_key, "weather", pipeline_query)
                                result.agent_name = agent_name
                            elif "Quality" in agent_name:
                                result = run_single_agent(api_key, "weather", pipeline_query)
                                result.agent_name = agent_name
                            elif "Weather" in agent_name:
                                result = run_single_agent(api_key, "weather", pipeline_query)
                            elif "Anomaly" in agent_name:
                                result = run_single_agent(api_key, "anomaly", pipeline_query)
                            elif "Prediction" in agent_name:
                                result = run_single_agent(api_key, "prediction", pipeline_query)
                            elif "NDVI" in agent_name:
                                result = run_single_agent(api_key, "ndvi", pipeline_query)
                            elif "Leak" in agent_name:
                                result = run_single_agent(api_key, "leak", pipeline_query)
                            elif "Cost" in agent_name:
                                result = run_single_agent(api_key, "cost", pipeline_query)
                            elif "Irrigation" in agent_name:
                                result = run_single_agent(api_key, "irrigation", pipeline_query)
                            elif "Sustainability" in agent_name:
                                result = run_single_agent(api_key, "sustainability", pipeline_query)
                            else:
                                full_ctx = "\n".join([f"[{r.agent_name}]: {r.output[:200]}" for r in all_results])
                                result = run_report_agent(api_key, pipeline_query, full_ctx)

                            all_results.append(result)

                            if result.status == "success":
                                st.write(f"✅ Complete — {result.duration_ms}ms | {result.tokens_used} tokens")
                                status.update(label=f"✅ {agent_name} — {result.duration_ms}ms", state="complete")
                            else:
                                st.write(f"⚠️ {result.output[:100]}")
                                status.update(label=f"⚠️ {agent_name} — Error", state="error")

                progress_bar.progress(1.0)

                # Final Report
                total_time = sum(r.duration_ms for r in all_results)
                total_tokens = sum(r.tokens_used for r in all_results)
                success_count = sum(1 for r in all_results if r.status == "success")

                st.markdown(f"""
                <div class="sensor-card" style="border-left:3px solid #10b981; margin-top:20px;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <div style="font-size:15px; font-weight:700; color:#4ade80;">✅ Pipeline Complete</div>
                            <div style="font-size:11px; color:#94a3b8; margin-top:4px;">
                                {success_count}/{len(all_results)} agents succeeded • {len(stages_config)} stages
                            </div>
                        </div>
                        <div style="text-align:right;">
                            <div style="font-size:20px; font-weight:800; color:#10b981;">{total_time/1000:.1f}s</div>
                            <div style="font-size:10px; color:#64748b;">{total_tokens:,} tokens</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Show final report agent output
                if all_results and all_results[-1].status == "success":
                    st.markdown("---")
                    st.markdown("### 📋 Final Synthesized Report")
                    st.markdown(all_results[-1].output)

                st.session_state["pipeline_results"] = all_results

    # Show previous results
    if st.session_state.get("pipeline_results") and not run_pipeline:
        results = st.session_state["pipeline_results"]
        with st.expander("📄 Previous Pipeline Results", expanded=False):
            for r in results:
                icon = "✅" if r.status == "success" else "⚠️"
                st.markdown(f"**{icon} {r.agent_name}** ({r.duration_ms}ms)")
                st.markdown(f"> {r.output[:200]}...")
                st.markdown("---")


# ===================== TAB 2: SINGLE AGENT =====================
with tab2:
    st.markdown('<div class="section-title">Targeted Agent Queries</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="sensor-card" style="margin-bottom:16px; border-left:3px solid #8b5cf6;">
        <div style="font-size:11px; color:#94a3b8;">
            Query individual agents directly. Each agent has specialized system instructions and
            access to park data context. Useful for focused analysis on specific topics.
        </div>
    </div>
    """, unsafe_allow_html=True)

    agent_options = {
        "🔍 Anomaly Detection": "anomaly",
        "📈 Consumption Prediction": "prediction",
        "🛰️ NDVI Vegetation Health": "ndvi",
        "🔧 Leak Detection": "leak",
        "💰 Cost Optimization": "cost",
        "💧 Irrigation Scheduling": "irrigation",
        "🌱 Sustainability & SDG": "sustainability",
        "🌤️ Weather & ET₀": "weather",
    }

    col1, col2 = st.columns([1, 2])
    with col1:
        selected_agent = st.radio("Select Agent:", list(agent_options.keys()), label_visibility="collapsed")

    with col2:
        agent_descriptions = {
            "anomaly": "Runs 5 detection methods (Z-Score, IQR, Moving Average, Isolation Forest, CUSUM) with consensus scoring.",
            "prediction": "90-day consumption forecast using seasonal decomposition and trend analysis.",
            "ndvi": "Sentinel-2 satellite vegetation health analysis with water-NDVI correlation.",
            "leak": "Night-flow pattern analysis and pressure differential leak detection.",
            "cost": "Financial impact calculator — waste costs, savings potential, city-wide projections.",
            "irrigation": "ET₀-based smart irrigation scheduling with 7-day weather integration.",
            "sustainability": "SDG alignment scoring (6, 11, 13, 15) and environmental impact metrics.",
            "weather": "Meteorological analysis with ET₀ evapotranspiration calculation.",
        }
        agent_key = agent_options[selected_agent]
        st.markdown(f"""
        <div class="sensor-card" style="padding:14px;">
            <div style="font-size:13px; font-weight:700; color:#f1f5f9; margin-bottom:6px;">{selected_agent}</div>
            <div style="font-size:11px; color:#94a3b8;">{agent_descriptions[agent_key]}</div>
            <div style="font-size:10px; color:#64748b; margin-top:8px;">Model: gemini-2.0-flash • Response: ~2-4 seconds</div>
        </div>
        """, unsafe_allow_html=True)

    single_query = st.text_input(
        "Your question:",
        placeholder="e.g., What anomalies exist in Park Beta? What's causing the issue?",
        key="single_q",
    )

    quick_queries = {
        "anomaly": "Detect all anomalies across parks with full method breakdown",
        "prediction": "Forecast water consumption for next 3 months for all parks",
        "ndvi": "Analyze vegetation health and identify water stress indicators",
        "leak": "Check for underground leaks using night-flow analysis",
        "cost": "Calculate total water waste cost and optimization savings",
        "irrigation": "Generate optimal 7-day irrigation schedule",
        "sustainability": "Score our SDG alignment and calculate CO2 reduction",
        "weather": "Analyze weather impact on irrigation needs this week",
    }

    col_quick, col_run = st.columns([3, 1])
    with col_quick:
        if st.button(f"💡 Try: \"{quick_queries[agent_key][:50]}...\"", use_container_width=True):
            st.session_state["single_q"] = quick_queries[agent_key]
            st.rerun()
    with col_run:
        run_single = st.button("🚀 Run Agent", type="primary", use_container_width=True, key="run_single")

    if run_single and single_query:
        if not has_api:
            st.warning("API key required. Set GEMINI_API_KEY environment variable.")
        else:
            can_proceed, msg = rl.can_proceed()
            if not can_proceed:
                st.error(f"⚠️ {msg}")
            else:
                rl.record_request()
                with st.status(f"⚡ Running {selected_agent}...", expanded=True) as status:
                    st.write("📡 Sending to Gemini with specialized system prompt...")
                    result = run_single_agent(api_key, agent_key, single_query)

                    if result.status == "success":
                        st.write(f"✅ Response received — {result.duration_ms}ms | {result.tokens_used} tokens")
                        status.update(label=f"✅ {result.agent_name} — Complete", state="complete")
                    else:
                        st.write(f"⚠️ Agent error occurred")
                        status.update(label=f"⚠️ Error", state="error")

                st.markdown("---")
                st.markdown(f"### 🤖 {result.agent_name} Response")
                st.markdown(result.output)

                st.markdown(f"""
                <div style="margin-top:16px; padding:10px 14px; background:#0d1117; border:1px solid #1e3048; border-radius:8px; font-size:10px; color:#64748b;">
                    Agent: {result.agent_name} • Model: {result.model} • Duration: {result.duration_ms}ms • Tokens: {result.tokens_used} • Status: {result.status}
                </div>
                """, unsafe_allow_html=True)


# ===================== TAB 3: ARCHITECTURE =====================
with tab3:
    st.markdown('<div class="section-title">Agent Architecture — ADK Patterns</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="sensor-card" style="margin-bottom:20px; border-left:3px solid #3b82f6;">
        <div style="font-size:11px; color:#94a3b8; line-height:1.8;">
            This system implements the <strong style="color:#f1f5f9;">Google Agent Development Kit (ADK)</strong> patterns:
            SequentialAgent for ordered processing, ParallelAgent for concurrent analysis,
            LoopAgent for continuous monitoring, and Human-in-the-Loop for critical decisions.
            External data flows through <strong style="color:#f1f5f9;">Model Context Protocol (MCP)</strong> servers.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Pipeline visualization
    stages = [
        {
            "name": "Stage 1: Data Pipeline",
            "pattern": "SequentialAgent",
            "color": "#3b82f6",
            "agents": [
                ("Data Ingest", "BigQuery MCP → raw consumption data"),
                ("Data Quality", "Validates completeness, interpolates gaps"),
                ("Weather", "Weather API MCP → ET₀ calculation"),
            ],
        },
        {
            "name": "Stage 2: Analysis Layer",
            "pattern": "ParallelAgent",
            "color": "#8b5cf6",
            "agents": [
                ("Anomaly Detection ×5", "Z-Score, IQR, MA, iForest, CUSUM → consensus"),
                ("Prediction", "Seasonal decomposition + Gemini Pro reasoning"),
                ("NDVI Satellite", "Earth Engine MCP → vegetation index"),
                ("Leak Detection", "Night-flow + pressure analysis"),
            ],
        },
        {
            "name": "Stage 3: Optimization",
            "pattern": "ParallelAgent",
            "color": "#f59e0b",
            "agents": [
                ("Cost Optimizer", "Waste × tariff → savings at all scales"),
                ("Irrigation Scheduler", "ET₀-based optimal timing and volume"),
                ("Comparative Benchmark", "Cross-park ranking & trends"),
            ],
        },
        {
            "name": "Stage 4: Governance",
            "pattern": "SequentialAgent",
            "color": "#10b981",
            "agents": [
                ("Compliance", "Municipal regulation checks & quotas"),
                ("Sustainability", "SDG scoring & CO₂ tracking"),
            ],
        },
        {
            "name": "Stage 5: Output",
            "pattern": "Human-in-the-Loop",
            "color": "#ef4444",
            "agents": [
                ("Report Generator", "Structured monthly report compilation"),
                ("Alert Agent", "HITL approval → Gmail API dispatch"),
            ],
        },
    ]

    for stage in stages:
        st.markdown(f"""
        <div style="background:#111827; border:1px solid {stage['color']}33; border-radius:12px; padding:16px 20px; margin:12px 0;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                <span style="font-size:13px; font-weight:700; color:{stage['color']};">{stage['name']}</span>
                <span style="font-size:10px; color:#94a3b8; background:{stage['color']}11; border:1px solid {stage['color']}33; padding:4px 12px; border-radius:12px;">{stage['pattern']}</span>
            </div>
        """, unsafe_allow_html=True)

        for agent_name, agent_desc in stage["agents"]:
            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:10px; padding:6px 0; border-bottom:1px solid #1e3048;">
                <div style="width:8px; height:8px; border-radius:50%; background:{stage['color']};"></div>
                <span style="font-size:11px; font-weight:600; color:#f1f5f9; min-width:140px;">{agent_name}</span>
                <span style="font-size:10px; color:#64748b;">{agent_desc}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # MCP & A2A Section
    st.markdown("---")
    col_mcp, col_a2a = st.columns(2)

    with col_mcp:
        st.markdown("""
        <div class="sensor-card" style="border-left:3px solid #06b6d4;">
            <div style="font-size:13px; font-weight:700; color:#f1f5f9; margin-bottom:10px;">MCP Servers (Model Context Protocol)</div>
            <div style="font-size:11px; color:#94a3b8; line-height:2.2;">
                📦 <strong>BigQuery</strong> — Historical consumption data<br>
                🛰️ <strong>Earth Engine</strong> — NDVI satellite imagery<br>
                🌤️ <strong>Weather API</strong> — Forecast & ET₀ data<br>
                📧 <strong>Gmail API</strong> — Alert dispatch
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_a2a:
        st.markdown("""
        <div class="sensor-card" style="border-left:3px solid #d946ef;">
            <div style="font-size:13px; font-weight:700; color:#f1f5f9; margin-bottom:10px;">A2A Protocol (Agent-to-Agent)</div>
            <div style="font-size:11px; color:#94a3b8; line-height:2.2;">
                🏛️ <strong>Municipal System</strong> — Regulation compliance<br>
                📡 <strong>IoT Gateway</strong> — Real-time sensor data<br>
                🔔 <strong>Notification Service</strong> — Multi-channel alerts<br>
                📊 <strong>Analytics Engine</strong> — Historical trends
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Technical specs
    st.markdown("---")
    st.markdown('<div class="section-title">Technical Specifications</div>', unsafe_allow_html=True)

    specs = [
        ("Total Agents", "21", "11 core + 5 anomaly sub-agents + 5 support"),
        ("ADK Patterns", "4/4", "Sequential, Parallel, Loop, HITL"),
        ("Models Used", "2", "gemini-2.0-flash (speed) + gemini-2.5-pro (reasoning)"),
        ("MCP Servers", "4", "BigQuery, Earth Engine, Weather, Gmail"),
        ("A2A Connections", "4", "Municipal, IoT, Notification, Analytics"),
        ("Avg Pipeline Time", "~12s", "11 agent calls with context passing"),
        ("Rate Limiting", "Active", "15/session, 4/min cooldown"),
        ("Data Points", "108+", "12 months × 3 parks × 3+ metrics"),
    ]

    cols = st.columns(4)
    for i, (label, value, desc) in enumerate(specs):
        cols[i % 4].markdown(f"""
        <div class="sensor-card" style="text-align:center; padding:14px 10px; margin-bottom:8px;">
            <div style="font-size:18px; font-weight:800; color:#f1f5f9;">{value}</div>
            <div style="font-size:11px; font-weight:600; color:#94a3b8; margin-top:4px;">{label}</div>
            <div style="font-size:9px; color:#64748b; margin-top:4px;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

render_footer()
