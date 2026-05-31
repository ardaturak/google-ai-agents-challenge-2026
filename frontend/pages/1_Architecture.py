"""Architecture — Agent topology and system design."""

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
    <p>Multi-Agent Orchestration Platform</p>
    <div class="badge-row">
        <span class="hbadge">21 Agents</span>
        <span class="hbadge">5 ADK Patterns</span>
        <span class="hbadge">4 MCP Servers</span>
        <span class="hbadge">2 A2A Connections</span>
    </div>
</div>
""", unsafe_allow_html=True)

# === KPIs ===
st.markdown("""
<div class="kpi-row">
    <div class="kpi-card"><div class="kpi-value">21</div><div class="kpi-label">Total Agents</div></div>
    <div class="kpi-card"><div class="kpi-value">5</div><div class="kpi-label">ADK Patterns</div></div>
    <div class="kpi-card"><div class="kpi-value">4</div><div class="kpi-label">MCP Servers</div></div>
    <div class="kpi-card"><div class="kpi-value">6</div><div class="kpi-label">Pipeline Stages</div></div>
    <div class="kpi-card"><div class="kpi-value">30</div><div class="kpi-label">Loop Iterations</div></div>
    <div class="kpi-card"><div class="kpi-value">15s</div><div class="kpi-label">Cycle Time</div></div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🔀 Agent Topology", "🔌 MCP & A2A", "🛠️ Tech Stack"])

with tab1:
    st.markdown('<div class="section-title">Pipeline Flow — 6-Stage Architecture</div>', unsafe_allow_html=True)

    fig = go.Figure()

    stages = [
        {"name": "DATA PIPELINE", "agents": "Ingest → Quality → Weather", "pattern": "SequentialAgent", "y": 5, "color": "#3b82f6"},
        {"name": "ANALYSIS LAYER", "agents": "Water · Anomaly(5×) · Predict · NDVI · Leak", "pattern": "ParallelAgent", "y": 4, "color": "#8b5cf6"},
        {"name": "OPTIMIZATION", "agents": "Cost · Irrigation · Comparative", "pattern": "ParallelAgent", "y": 3, "color": "#f59e0b"},
        {"name": "GOVERNANCE", "agents": "Compliance · Sustainability", "pattern": "SequentialAgent", "y": 2, "color": "#10b981"},
        {"name": "OUTPUT", "agents": "Report Generator → Alert Agent", "pattern": "Human-in-Loop", "y": 1, "color": "#ef4444"},
    ]

    for i, s in enumerate(stages):
        fig.add_trace(go.Scatter(
            x=[0.5], y=[s["y"]], mode="markers+text",
            marker=dict(size=50, color=s["color"], opacity=0.15, line=dict(width=2, color=s["color"])),
            text=f"<b>{s['name']}</b><br><span style='font-size:10px'>{s['agents']}</span><br><span style='font-size:9px; color:#94a3b8'>{s['pattern']}</span>",
            textposition="middle center", textfont=dict(size=11, color="#f1f5f9"),
            showlegend=False, hoverinfo="skip"
        ))
        if i < len(stages) - 1:
            fig.add_annotation(x=0.5, y=s["y"] - 0.35, ax=0, ay=25,
                             showarrow=True, arrowhead=3, arrowsize=1.5,
                             arrowwidth=2, arrowcolor="#475569")

    fig.add_trace(go.Scatter(
        x=[0.9], y=[5.3], mode="text",
        text=["<b>MONITORING LOOP</b><br><span style='font-size:9px'>LoopAgent ×30 iterations</span>"],
        textfont=dict(size=10, color="#fbbf24"), showlegend=False, hoverinfo="skip"
    ))
    fig.add_shape(type="rect", x0=0.1, x1=0.9, y0=0.6, y1=5.5,
                  line=dict(color="#fbbf24", width=1, dash="dash"), fillcolor="rgba(245,158,11,0.03)")

    fig.update_layout(
        height=500, template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(10,14,26,0.4)",
        xaxis=dict(visible=False, range=[0, 1.2]),
        yaxis=dict(visible=False, range=[0.3, 5.8]),
        margin=dict(t=10, b=10, l=10, r=10),
        font=dict(family="Inter")
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-title">ADK Pattern Usage</div>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    patterns = [
        ("SequentialAgent", "3", "Ordered pipeline stages", "#4ade80"),
        ("ParallelAgent", "3", "Concurrent analysis & optimization", "#fbbf24"),
        ("LoopAgent", "1", "Continuous monitoring (30 cycles)", "#f87171"),
        ("Human-in-Loop", "1", "Alert approval gate", "#d8b4fe"),
    ]
    for col, (name, count, desc, color) in zip([col1, col2, col3, col4], patterns):
        col.markdown(f"""
        <div class="sensor-card" style="text-align:center;">
            <div style="font-size:28px; font-weight:800; color:{color};">{count}×</div>
            <div style="font-size:12px; font-weight:700; color:#f1f5f9; margin:6px 0 4px;">{name}</div>
            <div style="font-size:10px; color:#64748b;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="section-title">Model Context Protocol (MCP) Connections</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        mcp_servers = [
            ("📦", "BigQuery", "Consumption + sensor time-series data", "Active", "#3b82f6"),
            ("🛰️", "Earth Engine", "Sentinel-2 NDVI satellite imagery", "Active", "#22c55e"),
            ("🌤️", "Weather API", "Forecast + ET₀ evapotranspiration", "Active", "#f59e0b"),
            ("📧", "Gmail API", "Critical alert email dispatch", "Active", "#ef4444"),
        ]
        for icon, name, desc, status, color in mcp_servers:
            st.markdown(f"""
            <div class="sensor-card" style="margin-bottom:10px;">
                <div style="display:flex; align-items:center; gap:12px;">
                    <span style="font-size:24px;">{icon}</span>
                    <div style="flex:1;">
                        <div style="font-size:13px; font-weight:700; color:#f1f5f9;">{name}</div>
                        <div style="font-size:11px; color:#64748b;">{desc}</div>
                    </div>
                    <span class="badge badge-ok">{status}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-title" style="margin-top:0;">Agent-to-Agent (A2A) Protocol</div>', unsafe_allow_html=True)
        a2a = [
            ("🏛️", "Municipal System", "Automated work order dispatch", "Configured"),
            ("📡", "IoT Gateway", "Remote valve control commands", "Configured"),
        ]
        for icon, name, desc, status in a2a:
            st.markdown(f"""
            <div class="sensor-card" style="margin-bottom:10px;">
                <div style="display:flex; align-items:center; gap:12px;">
                    <span style="font-size:24px;">{icon}</span>
                    <div style="flex:1;">
                        <div style="font-size:13px; font-weight:700; color:#f1f5f9;">{name}</div>
                        <div style="font-size:11px; color:#64748b;">{desc}</div>
                    </div>
                    <span class="badge badge-warn">{status}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="section-title">Data Flow Summary</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="sensor-card">
            <div class="sensor-row"><span class="sensor-key">Input Sources</span><span class="sensor-val">4 MCP servers</span></div>
            <div class="sensor-row"><span class="sensor-key">Processing</span><span class="sensor-val">21 agents × 30 loops</span></div>
            <div class="sensor-row"><span class="sensor-key">Output Channels</span><span class="sensor-val">2 A2A + Email + Dashboard</span></div>
            <div class="sensor-row"><span class="sensor-key">Cycle Frequency</span><span class="sensor-val">Every 15 seconds</span></div>
            <div class="sensor-row"><span class="sensor-key">Data Points/Day</span><span class="sensor-val">~180,000</span></div>
        </div>
        """, unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="section-title">Technology Stack</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="sensor-card">
            <div style="font-size:11px; font-weight:700; color:#3b82f6; margin-bottom:10px; letter-spacing:0.5px;">AI & AGENTS</div>
            <div class="sensor-row"><span class="sensor-key">Framework</span><span class="sensor-val">Google ADK</span></div>
            <div class="sensor-row"><span class="sensor-key">Models</span><span class="sensor-val">Gemini 2.5 Flash/Pro</span></div>
            <div class="sensor-row"><span class="sensor-key">Protocol</span><span class="sensor-val">MCP + A2A</span></div>
            <div class="sensor-row"><span class="sensor-key">Orchestration</span><span class="sensor-val">Multi-agent hierarchy</span></div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="sensor-card">
            <div style="font-size:11px; font-weight:700; color:#10b981; margin-bottom:10px; letter-spacing:0.5px;">CLOUD & INFRA</div>
            <div class="sensor-row"><span class="sensor-key">Compute</span><span class="sensor-val">Cloud Run</span></div>
            <div class="sensor-row"><span class="sensor-key">Data</span><span class="sensor-val">BigQuery</span></div>
            <div class="sensor-row"><span class="sensor-key">Satellite</span><span class="sensor-val">Earth Engine</span></div>
            <div class="sensor-row"><span class="sensor-key">Container</span><span class="sensor-val">Docker</span></div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="sensor-card">
            <div style="font-size:11px; font-weight:700; color:#f59e0b; margin-bottom:10px; letter-spacing:0.5px;">DATA SOURCES</div>
            <div class="sensor-row"><span class="sensor-key">Water</span><span class="sensor-val">ASKİ Authority</span></div>
            <div class="sensor-row"><span class="sensor-key">IoT</span><span class="sensor-val">ESP32 Sensors</span></div>
            <div class="sensor-row"><span class="sensor-key">Satellite</span><span class="sensor-val">Sentinel-2</span></div>
            <div class="sensor-row"><span class="sensor-key">Weather</span><span class="sensor-val">OpenMeteo API</span></div>
        </div>
        """, unsafe_allow_html=True)

render_footer()
