"""Agent Demo — Interactive agent pipeline simulation."""

import streamlit as st
import time
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from styles import GLOBAL_CSS
from components import render_sidebar, render_footer

st.set_page_config(page_title="Agent Demo | PRONUVE", page_icon="🤖", layout="wide", initial_sidebar_state="expanded")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
render_sidebar()

st.markdown("""
<div class="main-header">
    <h1>🤖 Agent Pipeline Demo</h1>
    <p>Interactive Simulation of the 21-Agent Monitoring Pipeline</p>
    <div class="badge-row">
        <span class="hbadge">Live Simulation</span>
        <span class="hbadge">SequentialAgent</span>
        <span class="hbadge">ParallelAgent</span>
        <span class="hbadge">LoopAgent</span>
    </div>
</div>
""", unsafe_allow_html=True)

PIPELINE_STEPS = [
    {"stage": "STAGE 1: DATA PIPELINE", "pattern": "SequentialAgent", "agents": [
        {"name": "Data Ingest Agent", "action": "Querying BigQuery for 36 monthly records across 3 parks...", "result": "108 records fetched (12 months × 3 parks × 3 metrics)", "duration": 0.4},
        {"name": "Data Quality Agent", "action": "Validating completeness, checking for nulls and outliers...", "result": "Score: 94% — 2 minor gaps interpolated", "duration": 0.3},
        {"name": "Weather Agent", "action": "Fetching 7-day forecast + calculating ET₀ evapotranspiration...", "result": "ET₀ = 6.2 mm/day | Rain probability: 72% tomorrow", "duration": 0.2},
    ]},
    {"stage": "STAGE 2: ANALYSIS", "pattern": "ParallelAgent", "agents": [
        {"name": "Water Analysis Agent", "action": "Computing efficiency ratios for each park...", "result": "Alpha: 78% | Beta: 45% ⚠️ | Gamma: 85%", "duration": 0.2},
        {"name": "Anomaly Detection (5×)", "action": "Running Z-Score, IQR, Moving Average, Isolation Forest, CUSUM in parallel...", "result": "Park Beta Jul: CONSENSUS 5/5 — 4,200 m³ (4.4× expected)", "duration": 0.5},
        {"name": "Prediction Agent", "action": "Seasonal decomposition + Gemini Pro trend analysis...", "result": "90-day forecast generated | MAPE: 3.9% | Seasonal peak: Aug", "duration": 0.3},
        {"name": "NDVI Satellite Agent", "action": "Processing Sentinel-2 imagery (10m resolution)...", "result": "Alpha: 0.58 (Healthy) | Beta: 0.31 (Stressed) | Gamma: 0.67 (Healthy)", "duration": 0.3},
        {"name": "Leak Detection Agent", "action": "Analyzing night-flow patterns and pressure differentials...", "result": "Park Beta: Night flow 8% (threshold: 5%) → Underground leak suspected", "duration": 0.2},
    ]},
    {"stage": "STAGE 3: OPTIMIZATION", "pattern": "ParallelAgent", "agents": [
        {"name": "Cost Optimizer", "action": "Calculating waste costs and savings potential...", "result": "Potential savings: 174,420 TRY/year across 3 parks", "duration": 0.2},
        {"name": "Irrigation Scheduler", "action": "Generating ET₀-based schedule considering weather...", "result": "SKIP tomorrow (rain 72%) | Next: Wednesday 06:00 (12mm)", "duration": 0.2},
        {"name": "Comparative Benchmark", "action": "Ranking parks by efficiency and improvement trajectory...", "result": "Rankings: 1. Gamma (85%) 2. Alpha (78%) 3. Beta (45%)", "duration": 0.2},
    ]},
    {"stage": "STAGE 4: GOVERNANCE", "pattern": "SequentialAgent", "agents": [
        {"name": "Compliance Agent", "action": "Checking municipal water regulations and quotas...", "result": "Score: 87% | Park Beta below minimum efficiency threshold", "duration": 0.2},
        {"name": "Sustainability Agent", "action": "Calculating SDG alignment and environmental impact...", "result": "SDG 6: 82 | SDG 11: 76 | SDG 13: 68 | SDG 15: 71", "duration": 0.2},
    ]},
    {"stage": "STAGE 5: OUTPUT", "pattern": "Human-in-the-Loop", "agents": [
        {"name": "Report Generator", "action": "Compiling analysis into structured monthly report...", "result": "Report generated: 3 sections, 12 charts, executive summary", "duration": 0.3},
        {"name": "Alert Agent (HITL)", "action": "CRITICAL: Park Beta anomaly → Requesting human approval...", "result": "✓ APPROVED — Alert dispatched to maintenance team via Gmail", "duration": 0.4},
    ]},
]

tab1, tab2 = st.tabs(["▶️ Run Pipeline", "📊 Agent Details"])

with tab1:
    st.markdown('<div class="section-title">Pipeline Execution Simulator</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="sensor-card" style="margin-bottom:16px; border-left:3px solid #3b82f6;">
        <div style="font-size:12px; color:#94a3b8;">
            This simulates one full monitoring cycle of the PRONUVE multi-agent pipeline.
            In production, the <strong>LoopAgent</strong> repeats this cycle continuously (30 iterations/session).
            Each agent uses <strong>Gemini 2.5 Flash</strong> for reasoning and <strong>MCP tools</strong> for data access.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("▶️  Run Full Pipeline", type="primary", use_container_width=True):
        total_start = time.time()
        for stage in PIPELINE_STEPS:
            st.markdown(f"""
            <div style="background:#111827; border:1px solid #1e3048; border-radius:10px; padding:14px 18px; margin:12px 0 8px;">
                <span style="font-size:12px; font-weight:700; color:#f1f5f9;">{stage['stage']}</span>
                <span style="float:right; font-size:10px; color:#64748b; background:#1e293b; padding:3px 10px; border-radius:12px;">{stage['pattern']}</span>
            </div>
            """, unsafe_allow_html=True)

            for agent in stage["agents"]:
                with st.status(f"🔄 {agent['name']}", expanded=False) as status:
                    st.write(f"⚡ {agent['action']}")
                    time.sleep(agent["duration"])
                    st.write(f"✅ {agent['result']}")
                    status.update(label=f"✅ {agent['name']} — {agent['duration']}s", state="complete")

        elapsed = time.time() - total_start
        st.markdown(f"""
        <div class="sensor-card" style="border-left:3px solid #10b981; margin-top:16px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <div style="font-size:14px; font-weight:700; color:#4ade80;">Pipeline Complete</div>
                    <div style="font-size:12px; color:#94a3b8; margin-top:4px;">15 agents executed across 5 stages • All systems nominal</div>
                </div>
                <div style="font-size:22px; font-weight:800; color:#10b981;">{elapsed:.1f}s</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align:center; padding:60px 20px; color:#64748b;">
            <div style="font-size:48px; margin-bottom:16px;">▶️</div>
            <div style="font-size:14px;">Press the button above to simulate a full pipeline run</div>
            <div style="font-size:11px; margin-top:8px; color:#475569;">15 pipeline agents • 5 stages • ~4 seconds simulation</div>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="section-title">All 21 Agents — Configuration</div>', unsafe_allow_html=True)

    agents_info = [
        ("Root Orchestrator", "LlmAgent", "gemini-2.5-flash", "Routes queries, manages sub-agents", "#3b82f6"),
        ("Data Ingest", "LlmAgent", "gemini-2.5-flash", "BigQuery MCP → consumption data", "#3b82f6"),
        ("Data Quality", "LlmAgent", "gemini-2.5-flash", "Validates completeness, interpolates gaps", "#3b82f6"),
        ("Weather", "LlmAgent", "gemini-2.5-flash", "Weather API MCP → ET₀ calculation", "#3b82f6"),
        ("Water Analysis", "LlmAgent", "gemini-2.5-flash", "Efficiency ratios and consumption patterns", "#8b5cf6"),
        ("Z-Score Detector", "LlmAgent", "gemini-2.5-flash", "Statistical z-score anomaly method", "#8b5cf6"),
        ("IQR Detector", "LlmAgent", "gemini-2.5-flash", "Interquartile range outlier detection", "#8b5cf6"),
        ("Moving Avg Detector", "LlmAgent", "gemini-2.5-flash", "Moving average deviation check", "#8b5cf6"),
        ("Isolation Forest", "LlmAgent", "gemini-2.5-flash", "ML-based isolation forest method", "#8b5cf6"),
        ("CUSUM Detector", "LlmAgent", "gemini-2.5-flash", "Cumulative sum change detection", "#8b5cf6"),
        ("Anomaly Consensus", "LlmAgent", "gemini-2.5-flash", "Aggregates 5 methods → final verdict", "#8b5cf6"),
        ("Prediction", "LlmAgent", "gemini-2.5-pro", "90-day forecast with seasonal decomposition", "#8b5cf6"),
        ("NDVI Satellite", "LlmAgent", "gemini-2.5-flash", "Earth Engine MCP → vegetation index", "#8b5cf6"),
        ("Leak Detection", "LlmAgent", "gemini-2.5-flash", "Night-flow analysis, pressure patterns", "#8b5cf6"),
        ("Cost Optimizer", "LlmAgent", "gemini-2.5-flash", "Financial waste calculations", "#f59e0b"),
        ("Irrigation Scheduler", "LlmAgent", "gemini-2.5-flash", "ET₀-based optimal schedule", "#f59e0b"),
        ("Comparative Benchmark", "LlmAgent", "gemini-2.5-flash", "Cross-park ranking and trends", "#f59e0b"),
        ("Compliance", "LlmAgent", "gemini-2.5-flash", "Municipal regulation checks", "#10b981"),
        ("Sustainability", "LlmAgent", "gemini-2.5-flash", "SDG scoring and CO₂ tracking", "#10b981"),
        ("Report Generator", "LlmAgent", "gemini-2.5-flash", "Structured report compilation", "#ef4444"),
        ("Alert Agent", "LlmAgent", "gemini-2.5-flash", "Gmail MCP → human-approved alerts", "#ef4444"),
    ]

    for i, (name, atype, model, desc, color) in enumerate(agents_info):
        st.markdown(f"""
        <div class="sensor-card" style="margin-bottom:6px; padding:12px 16px;">
            <div style="display:flex; align-items:center; gap:12px;">
                <div style="width:28px; height:28px; border-radius:8px; background:{color}22; border:1px solid {color}44; display:flex; align-items:center; justify-content:center; font-size:11px; font-weight:800; color:{color};">{i+1}</div>
                <div style="flex:1;">
                    <span style="font-size:12px; font-weight:700; color:#f1f5f9;">{name}</span>
                    <span style="font-size:10px; color:#64748b; margin-left:8px;">{desc}</span>
                </div>
                <span style="font-size:9px; color:#94a3b8; background:#1e293b; padding:3px 8px; border-radius:8px;">{model}</span>
                <span style="font-size:9px; color:{color}; background:{color}11; border:1px solid {color}33; padding:3px 8px; border-radius:8px;">{atype}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

render_footer()
