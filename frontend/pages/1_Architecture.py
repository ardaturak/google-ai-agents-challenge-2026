"""Architecture — Complete system architecture diagram for competition judges."""

import streamlit as st
import plotly.graph_objects as go
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from styles import GLOBAL_CSS
from components import render_sidebar, render_footer

st.set_page_config(page_title="Architecture | PRONUVE", page_icon="🏗️", layout="wide", initial_sidebar_state="expanded")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
render_sidebar()

st.markdown("""
<div class="main-header">
    <h1>🏗️ System Architecture</h1>
    <p>Multi-Agent Orchestration Platform — Google ADK Implementation</p>
    <div class="badge-row">
        <span class="hbadge">21 Agents</span>
        <span class="hbadge">5 ADK Patterns</span>
        <span class="hbadge">4 MCP Servers</span>
        <span class="hbadge">4 A2A Connections</span>
        <span class="hbadge">Gemini 2.5 Flash</span>
    </div>
</div>
""", unsafe_allow_html=True)

# === KPIs ===
st.markdown("""
<div class="kpi-row">
    <div class="kpi-card"><div class="kpi-value">21</div><div class="kpi-label">Total Agents</div></div>
    <div class="kpi-card"><div class="kpi-value">5</div><div class="kpi-label">ADK Patterns</div></div>
    <div class="kpi-card"><div class="kpi-value">4</div><div class="kpi-label">MCP Servers</div></div>
    <div class="kpi-card"><div class="kpi-value">5</div><div class="kpi-label">Pipeline Stages</div></div>
    <div class="kpi-card"><div class="kpi-value">30</div><div class="kpi-label">Loop Iterations</div></div>
    <div class="kpi-card"><div class="kpi-value">15s</div><div class="kpi-label">Cycle Time</div></div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📐 Architecture Diagram", "🤖 All 21 Agents", "🔌 MCP & A2A", "🛠️ Tech Stack"])

# ============================== TAB 1: ARCHITECTURE DIAGRAM ==============================
with tab1:
    st.markdown('<div class="section-title">Root Orchestrator — Full Pipeline Architecture</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="sensor-card" style="border-left:3px solid #3b82f6; margin-bottom:20px;">
        <div style="font-size:11px; color:#94a3b8; line-height:1.8;">
            The Root Orchestrator coordinates all 21 agents using Google ADK patterns.
            Each stage processes data sequentially or in parallel, passing context to the next stage.
            The entire pipeline completes in <strong style="color:#4ade80;">under 15 seconds</strong> with real Gemini API calls.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Visual Pipeline
    pipeline_stages = [
        ("STAGE 1", "Data Pipeline", "SequentialAgent", "#3b82f6", [
            ("Data Ingest Agent", "BigQuery MCP → raw consumption + IoT sensor data"),
            ("Data Quality Agent", "Validates completeness, interpolates gaps, scores 0-100%"),
            ("Weather Agent", "Weather API MCP → 7-day forecast + ET₀ evapotranspiration"),
        ]),
        ("STAGE 2", "Analysis Layer", "ParallelAgent", "#8b5cf6", [
            ("Anomaly Detection ×5", "Z-Score, IQR, Moving Avg, Isolation Forest, CUSUM → consensus"),
            ("Prediction Agent", "Seasonal decomposition + Gemini reasoning → 90-day forecast"),
            ("NDVI Satellite Agent", "Earth Engine MCP → Sentinel-2 vegetation health (10m resolution)"),
            ("Leak Detection Agent", "Night-flow + pressure + consumption-NDVI correlation"),
        ]),
        ("STAGE 3", "Optimization", "ParallelAgent", "#f59e0b", [
            ("Cost Optimizer", "Waste × ASKİ tariff (42.75 TRY/m³) → pilot/city/national savings"),
            ("Irrigation Scheduler", "ET₀ + soil moisture + rain forecast → 7-day optimal schedule"),
            ("Comparative Benchmark", "Cross-park ranking, best-practice identification"),
        ]),
        ("STAGE 4", "Governance", "SequentialAgent", "#10b981", [
            ("Compliance Agent", "Municipal water regulation audit, quota verification"),
            ("Sustainability Agent", "SDG 6/11/13/15 scoring, CO₂ + energy metrics"),
        ]),
        ("STAGE 5", "Output & Alert", "Human-in-the-Loop", "#ef4444", [
            ("Report Generator", "Synthesizes all findings → structured executive report"),
            ("Alert Agent", "Critical alerts → human approval gate → Gmail API dispatch"),
        ]),
    ]

    for stage_id, stage_name, pattern, color, agents in pipeline_stages:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg, #0c1524, #111827); border:1px solid {color}44;
             border-radius:14px; padding:18px 24px; margin:12px 0;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
                <div>
                    <span style="font-size:10px; color:{color}; font-weight:800; letter-spacing:1px;">{stage_id}</span>
                    <span style="font-size:14px; font-weight:700; color:#f1f5f9; margin-left:12px;">{stage_name}</span>
                </div>
                <span style="font-size:10px; color:#94a3b8; background:{color}15; border:1px solid {color}44;
                       padding:5px 14px; border-radius:20px; font-weight:600;">{pattern}</span>
            </div>
        """, unsafe_allow_html=True)

        for aname, adesc in agents:
            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:14px; padding:9px 0; border-bottom:1px solid #1e304855;">
                <div style="width:9px; height:9px; border-radius:50%; background:{color}; flex-shrink:0;"></div>
                <span style="font-size:12px; font-weight:600; color:#e2e8f0; min-width:180px;">{aname}</span>
                <span style="font-size:11px; color:#64748b;">{adesc}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        if stage_id != "STAGE 5":
            st.markdown(f"""
            <div style="text-align:center; padding:4px 0;">
                <span style="color:#475569; font-size:18px;">⬇</span>
                <span style="font-size:9px; color:#475569; margin-left:8px;">context passed to next stage</span>
            </div>
            """, unsafe_allow_html=True)

    # Monitoring Loop indicator
    st.markdown("""
    <div style="margin-top:20px; padding:14px 20px; background:#1a1a2e; border:1px dashed #fbbf24; border-radius:12px; text-align:center;">
        <span style="font-size:11px; color:#fbbf24; font-weight:700;">🔄 MONITORING LOOP (LoopAgent)</span>
        <span style="font-size:10px; color:#94a3b8; margin-left:16px;">Repeats full pipeline × 30 iterations per session | Continuous 24/7 monitoring</span>
    </div>
    """, unsafe_allow_html=True)

# ============================== TAB 2: ALL 21 AGENTS ==============================
with tab2:
    st.markdown('<div class="section-title">Complete Agent Registry — 21 Specialized Agents</div>', unsafe_allow_html=True)

    agents_data = [
        ("Root Orchestrator", "LlmAgent", "gemini-2.5-flash", "Routes queries, manages full pipeline", "#f1f5f9"),
        ("Data Ingest Agent", "LlmAgent", "gemini-2.5-flash", "BigQuery MCP → structures consumption data", "#3b82f6"),
        ("Data Quality Agent", "LlmAgent", "gemini-2.5-flash", "Validates completeness, interpolates gaps", "#3b82f6"),
        ("Weather Agent", "LlmAgent", "gemini-2.5-flash", "Weather API → ET₀ calculation (Penman-Monteith)", "#3b82f6"),
        ("Water Analysis Agent", "LlmAgent", "gemini-2.5-flash", "Efficiency ratios and consumption patterns", "#8b5cf6"),
        ("Z-Score Detector", "LlmAgent", "gemini-2.5-flash", "Statistical z-score anomaly detection", "#8b5cf6"),
        ("IQR Detector", "LlmAgent", "gemini-2.5-flash", "Interquartile range outlier detection", "#8b5cf6"),
        ("Moving Avg Detector", "LlmAgent", "gemini-2.5-flash", "Moving average deviation analysis", "#8b5cf6"),
        ("Isolation Forest Agent", "LlmAgent", "gemini-2.5-flash", "ML-based isolation forest method", "#8b5cf6"),
        ("CUSUM Detector", "LlmAgent", "gemini-2.5-flash", "Cumulative sum change detection", "#8b5cf6"),
        ("Anomaly Consensus", "LlmAgent", "gemini-2.5-flash", "Aggregates 5 methods → consensus score", "#8b5cf6"),
        ("Prediction Agent", "LlmAgent", "gemini-2.5-pro", "90-day forecast with seasonal decomposition", "#8b5cf6"),
        ("NDVI Satellite Agent", "LlmAgent", "gemini-2.5-flash", "Earth Engine → Sentinel-2 vegetation index", "#8b5cf6"),
        ("Leak Detection Agent", "LlmAgent", "gemini-2.5-flash", "Night-flow analysis + pressure patterns", "#8b5cf6"),
        ("Cost Optimizer", "LlmAgent", "gemini-2.5-flash", "Financial waste calculations (TRY/m³)", "#f59e0b"),
        ("Irrigation Scheduler", "LlmAgent", "gemini-2.5-flash", "ET₀-based optimal 7-day schedule", "#f59e0b"),
        ("Comparative Benchmark", "LlmAgent", "gemini-2.5-flash", "Cross-park ranking and trends", "#f59e0b"),
        ("Compliance Agent", "LlmAgent", "gemini-2.5-flash", "Municipal regulation verification", "#10b981"),
        ("Sustainability Agent", "LlmAgent", "gemini-2.5-flash", "SDG scoring + CO₂/energy metrics", "#10b981"),
        ("Report Generator", "LlmAgent", "gemini-2.5-flash", "Executive report synthesis", "#ef4444"),
        ("Alert Agent", "LlmAgent", "gemini-2.5-flash", "Gmail MCP → human-approved alert dispatch", "#ef4444"),
    ]

    st.markdown("""
    <div style="display:grid; grid-template-columns: 40px 1fr 120px 130px 1fr; gap:0; padding:10px 16px;
         background:#111827; border-radius:10px 10px 0 0; border:1px solid #1e3048; border-bottom:none;">
        <span style="font-size:9px; color:#64748b; font-weight:700;">#</span>
        <span style="font-size:9px; color:#64748b; font-weight:700;">AGENT NAME</span>
        <span style="font-size:9px; color:#64748b; font-weight:700;">TYPE</span>
        <span style="font-size:9px; color:#64748b; font-weight:700;">MODEL</span>
        <span style="font-size:9px; color:#64748b; font-weight:700;">FUNCTION</span>
    </div>
    """, unsafe_allow_html=True)

    for i, (name, atype, model, function, color) in enumerate(agents_data, 1):
        bg = "#0d111799" if i % 2 == 0 else "#0a0e1a99"
        border_bottom = "border-bottom:1px solid #1e304844;" if i < len(agents_data) else ""
        st.markdown(f"""
        <div style="display:grid; grid-template-columns: 40px 1fr 120px 130px 1fr; gap:0; padding:10px 16px;
             background:{bg}; {border_bottom} border-left:1px solid #1e3048; border-right:1px solid #1e3048;
             {'border-radius:0 0 10px 10px; border-bottom:1px solid #1e3048;' if i == len(agents_data) else ''}">
            <span style="font-size:11px; color:#475569; font-weight:600;">{i}</span>
            <span style="font-size:11px; color:{color}; font-weight:600;">{name}</span>
            <span style="font-size:10px; color:#94a3b8;">{atype}</span>
            <span style="font-size:10px; color:#64748b;">{model}</span>
            <span style="font-size:10px; color:#64748b;">{function}</span>
        </div>
        """, unsafe_allow_html=True)

    # ADK Patterns
    st.markdown("---")
    st.markdown('<div class="section-title">ADK Pattern Usage</div>', unsafe_allow_html=True)
    cols = st.columns(5)
    patterns = [
        ("Sequential\nAgent", "×3", "Ordered pipeline\nstages", "#4ade80"),
        ("Parallel\nAgent", "×3", "Concurrent\nanalysis", "#fbbf24"),
        ("Loop\nAgent", "×1", "30 iterations\nper session", "#f87171"),
        ("Human-in\n-the-Loop", "×1", "Alert approval\ngate", "#d8b4fe"),
        ("LlmAgent", "×21", "All specialized\nagents", "#38bdf8"),
    ]
    for col, (name, count, desc, color) in zip(cols, patterns):
        col.markdown(f"""
        <div class="sensor-card" style="text-align:center; padding:18px 8px;">
            <div style="font-size:26px; font-weight:800; color:{color};">{count}</div>
            <div style="font-size:11px; font-weight:700; color:#f1f5f9; margin:8px 0 6px; white-space:pre-line;">{name}</div>
            <div style="font-size:9px; color:#64748b; white-space:pre-line;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

# ============================== TAB 3: MCP & A2A ==============================
with tab3:
    st.markdown('<div class="section-title">Model Context Protocol (MCP) — External Data Access</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="sensor-card" style="border-left:3px solid #06b6d4; margin-bottom:20px;">
        <div style="font-size:11px; color:#94a3b8; line-height:1.8;">
            MCP provides a standardized protocol for agents to securely access external tools and data sources.
            Each MCP server exposes specific capabilities that agents can invoke autonomously during pipeline execution.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        mcp_servers = [
            ("📦", "BigQuery MCP", "36 months consumption data, IoT sensor readings, flow meter logs", "Active", "#3b82f6",
             "• Query: consumption by park/month\n• Query: sensor anomalies\n• Query: historical trends"),
            ("🛰️", "Earth Engine MCP", "Sentinel-2 satellite imagery, NDVI vegetation index (10m resolution)", "Active", "#22c55e",
             "• Tool: calculate_ndvi(park_boundary)\n• Tool: temporal_ndvi_series(12mo)\n• Tool: vegetation_classification()"),
            ("🌤️", "Weather API MCP", "7-day forecast, solar radiation, humidity, wind, ET₀ reference", "Active", "#f59e0b",
             "• Tool: get_forecast(lat, lon, days=7)\n• Tool: calculate_et0(penman_monteith)\n• Tool: rain_probability()"),
            ("📧", "Gmail API MCP", "Critical alert dispatch to maintenance teams with human approval", "Active", "#ef4444",
             "• Tool: send_alert(recipients, severity)\n• Tool: send_report(weekly_digest)\n• Requires: HITL approval"),
        ]
        for icon, name, desc, status, color, tools in mcp_servers:
            st.markdown(f"""
            <div class="sensor-card" style="margin-bottom:12px; border-left:3px solid {color};">
                <div style="display:flex; align-items:center; gap:12px; margin-bottom:10px;">
                    <span style="font-size:22px;">{icon}</span>
                    <div style="flex:1;">
                        <div style="font-size:13px; font-weight:700; color:#f1f5f9;">{name}</div>
                        <div style="font-size:10px; color:#64748b;">{desc}</div>
                    </div>
                    <span class="badge badge-ok">{status}</span>
                </div>
                <div style="font-size:10px; color:#475569; font-family:monospace; white-space:pre-line; padding:8px 12px; background:#0a0e1a; border-radius:8px;">{tools}</div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-title" style="margin-top:0;">Agent-to-Agent (A2A) Protocol</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="sensor-card" style="border-left:3px solid #d946ef; margin-bottom:16px;">
            <div style="font-size:11px; color:#94a3b8; line-height:1.8;">
                A2A enables inter-service communication between PRONUVE agents and external municipal systems.
                Agents can send structured messages, receive acknowledgments, and coordinate actions across services.
            </div>
        </div>
        """, unsafe_allow_html=True)

        a2a_connections = [
            ("🏛️", "Municipal System", "Automated work order dispatch for maintenance", "Configured", "#d946ef"),
            ("📡", "IoT Gateway", "Remote valve control + sensor commands", "Configured", "#d946ef"),
            ("🔔", "Notification Service", "Multi-channel alerts (SMS, push, email)", "Configured", "#d946ef"),
            ("📊", "Analytics Engine", "Trend aggregation for city dashboard", "Configured", "#d946ef"),
        ]
        for icon, name, desc, status, color in a2a_connections:
            st.markdown(f"""
            <div class="sensor-card" style="margin-bottom:10px;">
                <div style="display:flex; align-items:center; gap:12px;">
                    <span style="font-size:22px;">{icon}</span>
                    <div style="flex:1;">
                        <div style="font-size:12px; font-weight:700; color:#f1f5f9;">{name}</div>
                        <div style="font-size:10px; color:#64748b;">{desc}</div>
                    </div>
                    <span class="badge badge-warn">{status}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('<div class="section-title">Data Flow Metrics</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="sensor-card">
            <div class="sensor-row"><span class="sensor-key">Input Sources</span><span class="sensor-val">4 MCP servers</span></div>
            <div class="sensor-row"><span class="sensor-key">Processing</span><span class="sensor-val">21 agents × 30 loops</span></div>
            <div class="sensor-row"><span class="sensor-key">Output Channels</span><span class="sensor-val">4 A2A + Email + Dashboard</span></div>
            <div class="sensor-row"><span class="sensor-key">Cycle Frequency</span><span class="sensor-val">Every 15 seconds</span></div>
            <div class="sensor-row"><span class="sensor-key">Data Points/Day</span><span class="sensor-val">~180,000</span></div>
            <div class="sensor-row"><span class="sensor-key">Context Passed</span><span class="sensor-val">Agent-to-agent chaining</span></div>
        </div>
        """, unsafe_allow_html=True)

# ============================== TAB 4: TECH STACK ==============================
with tab3:
    pass

with tab4:
    st.markdown('<div class="section-title">Technology Stack</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="sensor-card">
            <div style="font-size:11px; font-weight:700; color:#3b82f6; margin-bottom:12px; letter-spacing:0.5px;">AI & AGENTS</div>
            <div class="sensor-row"><span class="sensor-key">Framework</span><span class="sensor-val">Google ADK</span></div>
            <div class="sensor-row"><span class="sensor-key">Primary Model</span><span class="sensor-val">Gemini 2.5 Flash</span></div>
            <div class="sensor-row"><span class="sensor-key">Reasoning Model</span><span class="sensor-val">Gemini 2.5 Pro</span></div>
            <div class="sensor-row"><span class="sensor-key">SDK</span><span class="sensor-val">google-genai (official)</span></div>
            <div class="sensor-row"><span class="sensor-key">Protocol</span><span class="sensor-val">MCP + A2A</span></div>
            <div class="sensor-row"><span class="sensor-key">Orchestration</span><span class="sensor-val">Multi-agent hierarchy</span></div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="sensor-card">
            <div style="font-size:11px; font-weight:700; color:#10b981; margin-bottom:12px; letter-spacing:0.5px;">CLOUD & INFRASTRUCTURE</div>
            <div class="sensor-row"><span class="sensor-key">Compute</span><span class="sensor-val">Cloud Run (serverless)</span></div>
            <div class="sensor-row"><span class="sensor-key">Data Warehouse</span><span class="sensor-val">BigQuery</span></div>
            <div class="sensor-row"><span class="sensor-key">Geospatial</span><span class="sensor-val">Earth Engine</span></div>
            <div class="sensor-row"><span class="sensor-key">Container</span><span class="sensor-val">Docker</span></div>
            <div class="sensor-row"><span class="sensor-key">Language</span><span class="sensor-val">Python 3.12</span></div>
            <div class="sensor-row"><span class="sensor-key">Region</span><span class="sensor-val">europe-west1</span></div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="sensor-card">
            <div style="font-size:11px; font-weight:700; color:#f59e0b; margin-bottom:12px; letter-spacing:0.5px;">DATA & FRONTEND</div>
            <div class="sensor-row"><span class="sensor-key">Water Data</span><span class="sensor-val">ASKİ Authority</span></div>
            <div class="sensor-row"><span class="sensor-key">IoT Sensors</span><span class="sensor-val">ESP32 (soil/flow)</span></div>
            <div class="sensor-row"><span class="sensor-key">Satellite</span><span class="sensor-val">Sentinel-2 (10m)</span></div>
            <div class="sensor-row"><span class="sensor-key">Weather</span><span class="sensor-val">OpenMeteo API</span></div>
            <div class="sensor-row"><span class="sensor-key">Dashboard</span><span class="sensor-val">Streamlit + Plotly</span></div>
            <div class="sensor-row"><span class="sensor-key">Visualization</span><span class="sensor-val">Interactive charts</span></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-title">Security & Production Features</div>', unsafe_allow_html=True)
    sec_cols = st.columns(4)
    security_items = [
        ("🔐", "API Key Security", "Server-side env vars only, never exposed to client"),
        ("⚡", "Rate Limiting", "15 queries/session, 4/min cooldown protection"),
        ("🛡️", "Error Recovery", "Graceful handling of API failures, quota limits, safety blocks"),
        ("📊", "Monitoring", "Cloud Run health checks, startup probes, auto-scaling"),
    ]
    for col, (icon, title, desc) in zip(sec_cols, security_items):
        col.markdown(f"""
        <div class="sensor-card" style="text-align:center; padding:16px 10px;">
            <div style="font-size:24px; margin-bottom:8px;">{icon}</div>
            <div style="font-size:11px; font-weight:700; color:#f1f5f9;">{title}</div>
            <div style="font-size:9px; color:#64748b; margin-top:6px;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

render_footer()
