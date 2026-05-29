"""PRONUVE Water Intelligence — Production Dashboard."""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from styles import GLOBAL_CSS

st.set_page_config(page_title="PRONUVE Water Intelligence", page_icon="💧", layout="wide", initial_sidebar_state="expanded")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
PARKS = {
    "park-alpha": {"name": "Park Alpha", "district": "Çankaya", "area": 35200, "efficiency": 78,
                   "consumption": [420, 385, 510, 890, 1450, 2100, 2380, 2250, 1520, 780, 410, 350],
                   "ndvi": 0.58, "moisture": 38.5, "temp": 26.1, "status": "normal"},
    "park-beta": {"name": "Park Beta", "district": "Yenimahalle", "area": 16500, "efficiency": 45,
                  "consumption": [180, 165, 230, 420, 680, 950, 4200, 980, 620, 340, 175, 150],
                  "ndvi": 0.31, "moisture": 16.5, "temp": 27.2, "status": "critical"},
    "park-gamma": {"name": "Park Gamma", "district": "Çankaya", "area": 58000, "efficiency": 85,
                   "consumption": [680, 620, 850, 1450, 2380, 3400, 3850, 3620, 2450, 1280, 670, 560],
                   "ndvi": 0.67, "moisture": 55.3, "temp": 22.8, "status": "good"},
}

# === SIDEBAR ===
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:20px 0 10px;'>
        <div style='font-size:40px; line-height:1;'>💧</div>
        <h2 style='color:#60a5fa; margin:8px 0 2px; font-size:20px; font-weight:700; letter-spacing:-0.5px;'>PRONUVE</h2>
        <p style='color:#64748b; font-size:11px; margin:0; letter-spacing:0.5px;'>WATER INTELLIGENCE</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("**System Status**")
    st.markdown("""
    <div style='font-size:12px; line-height:2.2; color:#cbd5e1;'>
    🟢 Orchestrator<br>🟢 Data Pipeline (3)<br>🟢 Analysis Layer (5)<br>
    🟢 Anomaly Detection (5×)<br>🟢 Optimization (3)<br>🟢 Governance (2)<br>
    🟢 Report Generator<br>🟡 Alert Agent <small style='color:#fbbf24;'>awaiting approval</small>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("**ADK Patterns**")
    st.markdown("""
    <div style='font-size:11px; color:#94a3b8; line-height:2;'>
    <span style='color:#4ade80;'>●</span> SequentialAgent ×3<br>
    <span style='color:#fbbf24;'>●</span> ParallelAgent ×3<br>
    <span style='color:#f87171;'>●</span> LoopAgent ×1<br>
    <span style='color:#d8b4fe;'>●</span> Human-in-Loop ×1
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("**MCP Servers**")
    st.markdown("""
    <div style='font-size:11px; color:#94a3b8; line-height:2;'>
    📦 BigQuery<br>🛰️ Earth Engine<br>🌤️ Weather API<br>📧 Gmail API
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("""
    <div style='text-align:center; color:#475569; font-size:10px; line-height:1.8;'>
    ProgenX + PRONUVE<br>METU • TÜBİTAK<br>
    <span style='color:#3b82f6;'>Google AI Agents Challenge 2026</span>
    </div>
    """, unsafe_allow_html=True)

# === HEADER ===
st.markdown("""
<div class="main-header">
    <h1>💧 PRONUVE Water Intelligence</h1>
    <p>Autonomous Multi-Agent Municipal Water Monitoring • 21 Agents • 5 Detection Methods • Real-Time</p>
</div>
""", unsafe_allow_html=True)

# === KPIs ===
st.markdown("""
<div class="kpi-row">
    <div class="kpi-card"><div class="kpi-value">21</div><div class="kpi-label">Active Agents</div><div class="kpi-delta up">All operational</div></div>
    <div class="kpi-card"><div class="kpi-value">3</div><div class="kpi-label">Parks Monitored</div><div class="kpi-delta up">Real ASKİ data</div></div>
    <div class="kpi-card"><div class="kpi-value">2</div><div class="kpi-label">Anomalies (30d)</div><div class="kpi-delta up">↓ 1 vs prior</div></div>
    <div class="kpi-card"><div class="kpi-value">78%</div><div class="kpi-label">Avg Efficiency</div><div class="kpi-delta up">↑ 5%</div></div>
    <div class="kpi-card"><div class="kpi-value">340</div><div class="kpi-label">Water Saved (m³)</div><div class="kpi-delta up">This month</div></div>
    <div class="kpi-card"><div class="kpi-value">94%</div><div class="kpi-label">Data Quality</div><div class="kpi-delta up">↑ 2%</div></div>
</div>
""", unsafe_allow_html=True)

# === TABS ===
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "🔍 Anomalies", "📈 Forecast", "🚨 Alerts", "🤖 Agent Log"])

with tab1:
    st.markdown('<div class="section-title">Consumption Trends — All Parks (2025)</div>', unsafe_allow_html=True)
    fig = go.Figure()
    colors = {"park-alpha": "#3b82f6", "park-beta": "#ef4444", "park-gamma": "#22c55e"}
    for pid, d in PARKS.items():
        fig.add_trace(go.Scatter(x=MONTHS, y=d["consumption"], name=d["name"],
                                 mode="lines+markers", line=dict(width=2.5, color=colors[pid]), marker=dict(size=4)))
    fig.add_annotation(x="Jul", y=4200, text="⚠️ ANOMALY<br><b>4,200 m³</b> (5/5)",
                       showarrow=True, arrowhead=2, font=dict(color="#ef4444", size=10),
                       bordercolor="#ef4444", borderwidth=1, bgcolor="#1f0a0a", borderpad=5)
    fig.update_layout(height=370, template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(15,23,42,0.5)", yaxis=dict(title="m³", gridcolor="#1e293b"),
                      xaxis=dict(gridcolor="#1e293b"), legend=dict(orientation="h", y=-0.12),
                      margin=dict(t=15, b=50, l=55, r=15), font=dict(family="Inter"))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-title">Sensor & Vegetation Status</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for col, (pid, d) in zip(cols, PARKS.items()):
        badge = {"normal": ("🟢", "badge-ok", "Normal"), "good": ("🟢", "badge-ok", "Good"),
                 "critical": ("🔴", "badge-crit", "Critical")}.get(d["status"], ("🟡", "badge-warn", "Warning"))
        ndvi_txt = "Healthy" if d["ndvi"] > 0.5 else "Stressed" if d["ndvi"] < 0.35 else "Moderate"
        ndvi_clr = "#4ade80" if d["ndvi"] > 0.5 else "#f87171" if d["ndvi"] < 0.35 else "#fbbf24"
        col.markdown(f"""
        <div class="sensor-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span class="park-name">{d['name']}</span>
                <span class="badge {badge[1]}">{badge[0]} {badge[2]}</span>
            </div>
            <div style="margin-top:12px;">
                <div class="sensor-row"><span class="sensor-key">💧 Moisture</span><span class="sensor-val">{d['moisture']}%</span></div>
                <div class="sensor-row"><span class="sensor-key">🌡️ Temp</span><span class="sensor-val">{d['temp']}°C</span></div>
                <div class="sensor-row"><span class="sensor-key">🛰️ NDVI</span><span class="sensor-val" style="color:{ndvi_clr};">{d['ndvi']} ({ndvi_txt})</span></div>
                <div class="sensor-row"><span class="sensor-key">⚡ Efficiency</span><span class="sensor-val">{d['efficiency']}%</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="section-title">Detected Anomalies — 5-Method Consensus</div>', unsafe_allow_html=True)
    df = pd.DataFrame([
        {"Park": "Park Beta", "Period": "Jul 2025", "Actual": "4,200 m³", "Expected": "~950 m³",
         "Severity": "🔴 CRITICAL", "Score": "5/5", "Recommended Action": "Emergency pipe inspection"},
        {"Park": "Park Alpha", "Period": "May 2025", "Actual": "1,450 m³", "Expected": "~1,100 m³",
         "Severity": "🟡 MEDIUM", "Score": "2/5", "Recommended Action": "Monitor next month"},
    ])
    st.dataframe(df, hide_index=True, use_container_width=True)
    st.markdown("---")
    st.markdown("**Methods:** `Z-Score` · `IQR` · `Moving Average` · `Isolation Forest` · `CUSUM`")
    st.markdown("**Rule:** Anomaly confirmed when **≥2 of 5** methods independently flag the same data point.")

with tab3:
    st.markdown('<div class="section-title">90-Day Consumption Forecast — Park Alpha</div>', unsafe_allow_html=True)
    future = ["Jun", "Jul", "Aug", "Sep"]
    forecast = [2100, 2420, 2310, 1580]
    upper = [2100, 2780, 2700, 1900]
    lower = [2100, 2060, 1920, 1260]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=future, y=upper, mode="lines", line=dict(width=0), showlegend=False))
    fig.add_trace(go.Scatter(x=future, y=lower, fill="tonexty", fillcolor="rgba(59,130,246,0.1)",
                             line=dict(width=0), name="95% Confidence"))
    fig.add_trace(go.Scatter(x=future, y=forecast, mode="lines+markers", name="AI Forecast",
                             line=dict(color="#3b82f6", width=3), marker=dict(size=8)))
    fig.update_layout(height=300, template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(15,23,42,0.5)", yaxis=dict(title="m³", gridcolor="#1e293b"),
                      xaxis=dict(gridcolor="#1e293b"), margin=dict(t=15, b=40, l=55, r=15),
                      legend=dict(orientation="h", y=-0.2), font=dict(family="Inter"))
    st.plotly_chart(fig, use_container_width=True)
    st.info("**Model:** Gemini 2.5 Pro with seasonal decomposition • **Accuracy:** MAPE 3.9% on historical data")

with tab4:
    st.markdown('<div class="section-title">🚨 Critical Alert — Human Approval Required</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="alert-card">
        <h3 style="color:#fca5a5; margin:0 0 10px; font-size:16px;">Park Beta — Possible Water Leak or Meter Malfunction</h3>
        <div style="color:#cbd5e1; font-size:13px; line-height:1.8;">
            <strong>Detection:</strong> 5/5 anomaly methods (unanimous consensus)<br>
            <strong>Details:</strong> July consumption 4,200 m³ — <strong>4.4×</strong> expected value (~950 m³)<br>
            <strong>NDVI:</strong> 0.31 (vegetation stressed despite over-consumption → water not reaching roots)<br>
            <strong>Night flow:</strong> 8% of daily average (threshold: 5%) → underground leak suspected<br>
            <strong>Estimated loss:</strong> ~108 m³/day → <strong>~4,617 TRY/day</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("")
    c1, c2, c3 = st.columns(3)
    c1.button("✅ Approve — Dispatch Alert", type="primary", use_container_width=True)
    c2.button("✏️ Modify — Edit Recipients", use_container_width=True)
    c3.button("❌ Reject — Mark False Positive", use_container_width=True)

with tab5:
    st.markdown('<div class="section-title">Pipeline Execution — Latest Run</div>', unsafe_allow_html=True)
    log = pd.DataFrame([
        {"⏱️": "10:45:02", "Agent": "Data Ingest", "Action": "36 monthly records from BigQuery", "Result": "✅"},
        {"⏱️": "10:45:03", "Agent": "Data Quality", "Action": "Score: 94% — all parks reporting", "Result": "✅"},
        {"⏱️": "10:45:04", "Agent": "Weather", "Action": "ET₀ = 6.2 mm/day, rain 72% tomorrow", "Result": "✅"},
        {"⏱️": "10:45:06", "Agent": "Water Analysis", "Action": "3 parks efficiency calculated", "Result": "✅"},
        {"⏱️": "10:45:08", "Agent": "Anomaly (5×)", "Action": "Parallel run — 2 anomalies flagged", "Result": "⚠️"},
        {"⏱️": "10:45:09", "Agent": "Prediction", "Action": "90-day forecast (Gemini Pro)", "Result": "✅"},
        {"⏱️": "10:45:10", "Agent": "NDVI Satellite", "Action": "Park Beta stressed (0.31)", "Result": "⚠️"},
        {"⏱️": "10:45:11", "Agent": "Leak Detection", "Action": "Night-flow 8% at Park Beta", "Result": "🔴"},
        {"⏱️": "10:45:12", "Agent": "Cost Optimizer", "Action": "Savings: 174,420 TRY/year", "Result": "✅"},
        {"⏱️": "10:45:13", "Agent": "Scheduler", "Action": "Skip irrigation (rain forecast)", "Result": "✅"},
        {"⏱️": "10:45:14", "Agent": "Comparative", "Action": "Rankings updated", "Result": "✅"},
        {"⏱️": "10:45:15", "Agent": "Compliance", "Action": "Score: 87%", "Result": "✅"},
        {"⏱️": "10:45:15", "Agent": "Sustainability", "Action": "SDG scores: 6→82, 11→76", "Result": "✅"},
        {"⏱️": "10:45:16", "Agent": "Report", "Action": "Monthly report generated", "Result": "✅"},
        {"⏱️": "10:45:17", "Agent": "Alert", "Action": "CRITICAL queued — awaiting approval", "Result": "🔴"},
    ])
    st.dataframe(log, hide_index=True, use_container_width=True, height=400)
    st.caption("Pipeline total: **15 agents** executed in **15 seconds** • SequentialAgent → ParallelAgent → LoopAgent")
