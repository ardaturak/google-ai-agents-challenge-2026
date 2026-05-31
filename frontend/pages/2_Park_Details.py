"""Park Details — Per-park deep dive analysis."""

import streamlit as st
import plotly.graph_objects as go
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from styles import GLOBAL_CSS
from components import render_sidebar, render_footer

st.set_page_config(page_title="Park Details | PRONUVE", page_icon="🌳", layout="wide", initial_sidebar_state="expanded")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
render_sidebar()

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
PARKS = {
    "Park Alpha — Çankaya (Recreation)": {
        "area": 35200, "efficiency": 78, "compliance": 92, "leak": "Low", "ndvi_avg": 0.58,
        "consumption": [420, 385, 510, 890, 1450, 2100, 2380, 2250, 1520, 780, 410, 350],
        "ndvi": [0.42, 0.38, 0.45, 0.55, 0.62, 0.58, 0.55, 0.52, 0.50, 0.45, 0.40, 0.38],
        "icon": "🏞️", "type": "Recreation",
    },
    "Park Beta — Yenimahalle (Sports)": {
        "area": 16500, "efficiency": 45, "compliance": 58, "leak": "HIGH", "ndvi_avg": 0.31,
        "consumption": [180, 165, 230, 420, 680, 950, 4200, 980, 620, 340, 175, 150],
        "ndvi": [0.40, 0.36, 0.42, 0.50, 0.55, 0.48, 0.31, 0.35, 0.38, 0.36, 0.34, 0.32],
        "icon": "⚽", "type": "Sports Complex",
    },
    "Park Gamma — Çankaya (Botanical)": {
        "area": 58000, "efficiency": 85, "compliance": 96, "leak": "Low", "ndvi_avg": 0.67,
        "consumption": [680, 620, 850, 1450, 2380, 3400, 3850, 3620, 2450, 1280, 670, 560],
        "ndvi": [0.55, 0.52, 0.58, 0.65, 0.72, 0.70, 0.67, 0.64, 0.60, 0.55, 0.52, 0.50],
        "icon": "🌿", "type": "Botanical Garden",
    },
}

st.markdown("""
<div class="main-header">
    <h1>🌳 Park Details</h1>
    <p>Individual Park Deep-Dive Analysis</p>
    <div class="badge-row">
        <span class="hbadge">Consumption vs Optimal</span>
        <span class="hbadge">NDVI Health</span>
        <span class="hbadge">Cost Impact</span>
    </div>
</div>
""", unsafe_allow_html=True)

selected = st.selectbox("Select Park", list(PARKS.keys()), label_visibility="collapsed")
park = PARKS[selected]

# KPI row for selected park
eff_color = "up" if park["efficiency"] >= 70 else "down"
comp_color = "up" if park["compliance"] >= 80 else "down"
leak_badge = "up" if park["leak"] == "Low" else "down"
st.markdown(f"""
<div class="kpi-row">
    <div class="kpi-card"><div class="kpi-value">{park['icon']}</div><div class="kpi-label">{park['type']}</div></div>
    <div class="kpi-card"><div class="kpi-value">{park['area']:,}</div><div class="kpi-label">Area (m²)</div></div>
    <div class="kpi-card"><div class="kpi-value">{park['efficiency']}%</div><div class="kpi-label">Efficiency</div><div class="kpi-delta {eff_color}">{'Good' if park['efficiency']>=70 else 'Low'}</div></div>
    <div class="kpi-card"><div class="kpi-value">{park['compliance']}%</div><div class="kpi-label">Compliance</div><div class="kpi-delta {comp_color}">{'Passing' if park['compliance']>=80 else 'Failing'}</div></div>
    <div class="kpi-card"><div class="kpi-value">{park['ndvi_avg']}</div><div class="kpi-label">Avg NDVI</div><div class="kpi-delta {'up' if park['ndvi_avg']>0.5 else 'down'}">{'Healthy' if park['ndvi_avg']>0.5 else 'Stressed'}</div></div>
    <div class="kpi-card"><div class="kpi-value">{park['leak']}</div><div class="kpi-label">Leak Risk</div><div class="kpi-delta {leak_badge}">{'Safe' if park['leak']=='Low' else 'Alert'}</div></div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📊 Consumption vs Optimal", "🛰️ Vegetation Health", "💰 Cost Impact"])

with tab1:
    st.markdown('<div class="section-title">Monthly Consumption vs ET₀-Optimal</div>', unsafe_allow_html=True)
    fig = go.Figure()
    optimal = [int(c * 0.65) for c in park["consumption"]]

    fig.add_trace(go.Bar(x=MONTHS, y=park["consumption"], name="Actual Consumption",
                         marker=dict(color="#3b82f6", opacity=0.8, line=dict(width=0)),
                         hovertemplate="<b>%{x}</b><br>Actual: %{y:,} m³<extra></extra>"))
    fig.add_trace(go.Bar(x=MONTHS, y=optimal, name="Optimal (ET₀)",
                         marker=dict(color="#10b981", opacity=0.6, line=dict(width=0)),
                         hovertemplate="<b>%{x}</b><br>Optimal: %{y:,} m³<extra></extra>"))
    fig.add_trace(go.Scatter(x=MONTHS, y=[c - o for c, o in zip(park["consumption"], optimal)],
                             name="Waste", mode="lines+markers",
                             line=dict(color="#ef4444", width=2, dash="dot"),
                             marker=dict(size=5), yaxis="y2",
                             hovertemplate="<b>%{x}</b><br>Waste: %{y:,} m³<extra></extra>"))

    fig.update_layout(
        height=400, template="plotly_dark", barmode="group",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(10,14,26,0.6)",
        yaxis=dict(title="Volume (m³)", gridcolor="rgba(30,48,72,0.5)", tickformat=","),
        yaxis2=dict(title="Waste (m³)", overlaying="y", side="right", gridcolor="rgba(30,48,72,0.3)", tickformat=","),
        xaxis=dict(gridcolor="rgba(30,48,72,0.3)"),
        legend=dict(orientation="h", y=-0.15, x=0.5, xanchor="center", font=dict(size=11)),
        margin=dict(t=15, b=55, l=60, r=60), font=dict(family="Inter"),
        hovermode="x unified",
        hoverlabel=dict(bgcolor="#1e293b", bordercolor="#3b82f6", font_size=12)
    )
    st.plotly_chart(fig, use_container_width=True)

    waste_pct = round((1 - sum(optimal) / sum(park["consumption"])) * 100)
    total_waste = sum(park["consumption"]) - sum(optimal)
    st.markdown(f"""
    <div class="sensor-card" style="border-left: 3px solid #f59e0b;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <div style="font-size:13px; font-weight:700; color:#fbbf24;">Over-Irrigation Detected</div>
                <div style="font-size:12px; color:#94a3b8; margin-top:4px;">{waste_pct}% above ET₀-calculated optimal • {total_waste:,} m³/year wasted</div>
            </div>
            <div style="font-size:24px; font-weight:800; color:#f59e0b;">{waste_pct}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="section-title">NDVI Vegetation Index — Sentinel-2 Satellite</div>', unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=MONTHS, y=park["ndvi"], mode="lines+markers", name="NDVI",
                             line=dict(color="#22c55e", width=3, shape="spline"),
                             fill="tozeroy", fillcolor="rgba(34,197,94,0.08)",
                             marker=dict(size=7, color="#22c55e", line=dict(width=2, color="#0a0e1a")),
                             hovertemplate="<b>%{x}</b><br>NDVI: %{y:.2f}<extra></extra>"))
    fig.add_hline(y=0.5, line_dash="dash", line_color="#eab308", line_width=1.5,
                  annotation_text="Healthy (0.5)", annotation_font_color="#eab308", annotation_font_size=10)
    fig.add_hline(y=0.35, line_dash="dot", line_color="#ef4444", line_width=1.5,
                  annotation_text="Stressed (0.35)", annotation_font_color="#ef4444", annotation_font_size=10)
    fig.update_layout(
        height=380, template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(10,14,26,0.6)",
        yaxis=dict(title="NDVI (0–1)", range=[0, 1], gridcolor="rgba(30,48,72,0.5)"),
        xaxis=dict(gridcolor="rgba(30,48,72,0.3)"),
        margin=dict(t=15, b=40, l=55, r=15), font=dict(family="Inter"),
        hovermode="x unified",
        hoverlabel=dict(bgcolor="#1e293b", bordercolor="#22c55e", font_size=12)
    )
    st.plotly_chart(fig, use_container_width=True)

    avg = park["ndvi_avg"]
    status = "Healthy" if avg > 0.5 else "Stressed" if avg < 0.35 else "Moderate"
    color = "#4ade80" if avg > 0.5 else "#f87171" if avg < 0.35 else "#fbbf24"
    st.markdown(f"""
    <div class="sensor-card" style="border-left: 3px solid {color};">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <div style="font-size:13px; font-weight:700; color:{color};">Vegetation Status: {status}</div>
                <div style="font-size:12px; color:#94a3b8; margin-top:4px;">Annual average NDVI: {avg} • Source: Sentinel-2 (10m resolution)</div>
            </div>
            <div style="font-size:24px; font-weight:800; color:{color};">{avg}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="section-title">Financial Impact Analysis</div>', unsafe_allow_html=True)
    total = sum(park["consumption"])
    optimal_total = int(total * 0.65)
    waste = total - optimal_total
    cost_total = total * 42.75
    cost_waste = waste * 42.75
    co2 = total * 0.376
    energy = waste * 0.8

    st.markdown(f"""
    <div class="kpi-row">
        <div class="kpi-card"><div class="kpi-value">{total:,}</div><div class="kpi-label">Annual (m³)</div></div>
        <div class="kpi-card"><div class="kpi-value">{cost_total:,.0f}</div><div class="kpi-label">Cost (TRY)</div></div>
        <div class="kpi-card"><div class="kpi-value" style="color:#ef4444;">{cost_waste:,.0f}</div><div class="kpi-label">Savings Potential (TRY)</div></div>
        <div class="kpi-card"><div class="kpi-value">{co2:,.0f}</div><div class="kpi-label">CO₂ (kg/yr)</div></div>
        <div class="kpi-card"><div class="kpi-value">{energy:,.0f}</div><div class="kpi-label">Energy Waste (kWh)</div></div>
        <div class="kpi-card"><div class="kpi-value">{cost_total / park['area']:.1f}</div><div class="kpi-label">TRY/m²/year</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sensor-card">
        <div style="font-size:11px; font-weight:700; color:#3b82f6; margin-bottom:10px; letter-spacing:0.5px;">CALCULATION BASIS</div>
        <div class="sensor-row"><span class="sensor-key">ASKİ Water Tariff</span><span class="sensor-val">42.75 TRY/m³ (2025)</span></div>
        <div class="sensor-row"><span class="sensor-key">CO₂ per m³</span><span class="sensor-val">0.376 kg (Turkey avg)</span></div>
        <div class="sensor-row"><span class="sensor-key">Energy per m³</span><span class="sensor-val">0.8 kWh (pump + treatment)</span></div>
        <div class="sensor-row"><span class="sensor-key">Target Reduction</span><span class="sensor-val">35% via AI optimization</span></div>
        <div class="sensor-row"><span class="sensor-key">Tree Offset</span><span class="sensor-val">22 kg CO₂/year per tree</span></div>
    </div>
    """, unsafe_allow_html=True)

render_footer()
