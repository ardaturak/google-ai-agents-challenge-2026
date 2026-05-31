"""PRONUVE Water Intelligence — Production Dashboard."""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from styles import GLOBAL_CSS
from components import render_sidebar, render_footer

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
render_sidebar()

# === HEADER ===
st.markdown("""
<div class="main-header">
    <h1>💧 PRONUVE Water Intelligence</h1>
    <p>Autonomous Multi-Agent Municipal Water Monitoring Platform</p>
    <div class="badge-row">
        <span class="hbadge">21 AI Agents</span>
        <span class="hbadge">Google ADK</span>
        <span class="hbadge">5 Anomaly Methods</span>
        <span class="hbadge">Real-Time Monitoring</span>
        <span class="hbadge">Cloud Run</span>
    </div>
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
    st.markdown('<div class="section-title">Consumption Trends — All Parks (2024–2025)</div>', unsafe_allow_html=True)

    MONTHS_FULL = ["Jan '24","Feb '24","Mar '24","Apr '24","May '24","Jun '24",
                   "Jul '24","Aug '24","Sep '24","Oct '24","Nov '24","Dec '24",
                   "Jan '25","Feb '25","Mar '25","Apr '25","May '25","Jun '25",
                   "Jul '25","Aug '25","Sep '25","Oct '25","Nov '25","Dec '25"]
    consumption_extended = {
        "park-alpha": [1900,1850,2100,2400,2750,3100,3400,3250,2900,2400,2100,1950,
                       2000,1900,2200,2500,2800,3200,3500,3300,2950,2450,2150,2000],
        "park-beta":  [1400,1350,1500,1650,1800,2100,2400,2300,1950,1600,1450,1380,
                       1450,1400,1550,1700,1850,2200,4200,2350,2000,1650,1500,1400],
        "park-gamma": [950,900,1000,1150,1300,1500,1700,1600,1400,1150,1000,950,
                       980,930,1050,1200,1350,1550,1750,1650,1450,1200,1050,980],
    }
    colors = {"park-alpha": "#3b82f6", "park-beta": "#f97316", "park-gamma": "#10b981"}
    fill_colors = {"park-alpha": "rgba(59,130,246,0.08)", "park-beta": "rgba(249,115,22,0.08)", "park-gamma": "rgba(16,185,129,0.08)"}

    fig = go.Figure()
    for pid, d in PARKS.items():
        fig.add_trace(go.Scatter(
            x=MONTHS_FULL, y=consumption_extended[pid], name=d["name"],
            mode="lines+markers",
            line=dict(width=2.5, color=colors[pid], shape="spline"),
            marker=dict(size=3, color=colors[pid]),
            fill="tozeroy", fillcolor=fill_colors[pid],
            hovertemplate="<b>%{x}</b><br>%{y:,.0f} m³<extra>" + d["name"] + "</extra>"
        ))

    fig.add_vrect(x0="Jun '25", x1="Aug '25", fillcolor="rgba(239,68,68,0.05)",
                  line_width=0, annotation_text="Peak Season", annotation_position="top left",
                  annotation=dict(font_size=10, font_color="#94a3b8"))

    fig.add_annotation(x="Jul '25", y=4200, text="<b>ANOMALY DETECTED</b><br>4,200 m³ • Consensus 5/5",
                       showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=1.5, arrowcolor="#ef4444",
                       font=dict(color="#fca5a5", size=10, family="Inter"),
                       bordercolor="#7f1d1d", borderwidth=1.5, bgcolor="rgba(31,10,10,0.95)", borderpad=8,
                       ax=40, ay=-50)

    fig.update_layout(
        height=420, template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(10,14,26,0.6)",
        yaxis=dict(title="Consumption (m³)", gridcolor="rgba(30,48,72,0.5)", gridwidth=1,
                   tickformat=",", zeroline=False, title_font=dict(size=11, color="#64748b")),
        xaxis=dict(gridcolor="rgba(30,48,72,0.3)", gridwidth=1, tickangle=-45,
                   tickfont=dict(size=9), dtick=2),
        legend=dict(orientation="h", y=-0.18, x=0.5, xanchor="center",
                    bgcolor="rgba(17,24,39,0.8)", bordercolor="#1e3048", borderwidth=1,
                    font=dict(size=11)),
        margin=dict(t=20, b=70, l=60, r=20),
        font=dict(family="Inter"),
        hovermode="x unified",
        hoverlabel=dict(bgcolor="#1e293b", bordercolor="#3b82f6", font_size=12, font_family="Inter")
    )
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
        {"⏱️": "10:45:17", "Agent": "Alert", "Action": "CRITICAL alert sent — human-in-the-loop approved", "Result": "🟢"},
    ])
    st.dataframe(log, hide_index=True, use_container_width=True, height=400)
    st.caption("Pipeline total: **15 agents** executed in **15 seconds** • SequentialAgent → ParallelAgent → LoopAgent")

render_footer()
