"""Sustainability — SDG alignment and environmental impact."""

import streamlit as st
import plotly.graph_objects as go
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from styles import GLOBAL_CSS
from components import render_sidebar, render_footer

st.set_page_config(page_title="Sustainability | PRONUVE", page_icon="🌍", layout="wide", initial_sidebar_state="expanded")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
render_sidebar()

st.markdown("""
<div class="main-header">
    <h1>🌍 Sustainability & SDG Alignment</h1>
    <p>Environmental Impact • UN Sustainable Development Goals • CO₂ Tracking</p>
    <div class="badge-row">
        <span class="hbadge">SDG 6</span>
        <span class="hbadge">SDG 11</span>
        <span class="hbadge">SDG 13</span>
        <span class="hbadge">SDG 15</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="kpi-row">
    <div class="kpi-card"><div class="kpi-value">4,080</div><div class="kpi-label">Water Saved (m³/yr)</div><div class="kpi-delta up">3 pilot parks</div></div>
    <div class="kpi-card"><div class="kpi-value">$4.6K</div><div class="kpi-label">Cost Saved/yr</div><div class="kpi-delta up">174,420 TRY</div></div>
    <div class="kpi-card"><div class="kpi-value">1,534</div><div class="kpi-label">CO₂ Avoided (kg/yr)</div><div class="kpi-delta up">= 70 trees</div></div>
    <div class="kpi-card"><div class="kpi-value">$310K</div><div class="kpi-label">City-Wide Potential</div><div class="kpi-delta up">200 parks</div></div>
    <div class="kpi-card"><div class="kpi-value">$50M+</div><div class="kpi-label">National TAM</div><div class="kpi-delta up">1,400 municipalities</div></div>
    <div class="kpi-card"><div class="kpi-value">4</div><div class="kpi-label">SDGs Addressed</div><div class="kpi-delta up">Direct impact</div></div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🎯 SDG Scores", "📈 Monthly Impact", "📋 Methodology"])

with tab1:
    st.markdown('<div class="section-title">UN Sustainable Development Goal Alignment</div>', unsafe_allow_html=True)

    sdgs = [
        ("SDG 6", "Clean Water & Sanitation", 82, "#3b82f6", "Reducing water waste through AI-optimized irrigation and leak detection"),
        ("SDG 11", "Sustainable Cities", 76, "#22c55e", "Smart municipal park management with data-driven decisions"),
        ("SDG 13", "Climate Action", 68, "#eab308", "Reducing energy consumption and CO₂ emissions from water pumping"),
        ("SDG 15", "Life on Land", 71, "#a855f7", "Maintaining green spaces with optimal NDVI-guided watering"),
    ]

    cols = st.columns(4)
    for col, (name, title, score, color, desc) in zip(cols, sdgs):
        fig = go.Figure(go.Indicator(
            mode="gauge+number", value=score,
            gauge={"axis": {"range": [0, 100], "tickcolor": "#334155", "tickfont": {"size": 9}},
                   "bar": {"color": color, "thickness": 0.7},
                   "bgcolor": "#1e293b", "borderwidth": 0,
                   "steps": [{"range": [0, 50], "color": "#0f172a"}, {"range": [50, 100], "color": "#1e293b"}]},
            number={"suffix": "/100", "font": {"size": 28, "color": "#f1f5f9", "family": "Inter"}},
        ))
        fig.update_layout(height=140, margin=dict(t=20, b=0, l=15, r=15),
                          paper_bgcolor="rgba(0,0,0,0)", font=dict(family="Inter"))
        col.markdown(f"<div style='text-align:center; font-size:12px; font-weight:700; color:{color};'>{name}</div>", unsafe_allow_html=True)
        col.markdown(f"<div style='text-align:center; font-size:10px; color:#94a3b8;'>{title}</div>", unsafe_allow_html=True)
        col.plotly_chart(fig, use_container_width=True)
        col.markdown(f"<div style='font-size:10px; color:#64748b; text-align:center; margin-top:-10px;'>{desc}</div>", unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="section-title">Environmental Impact Trend (2025)</div>', unsafe_allow_html=True)

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    water_saved = [120, 95, 180, 320, 480, 560, 620, 590, 420, 280, 150, 130]
    co2_avoided = [45, 36, 68, 120, 180, 211, 233, 222, 158, 105, 56, 49]
    energy_saved = [96, 76, 144, 256, 384, 448, 496, 472, 336, 224, 120, 104]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=months, y=water_saved, name="Water Saved (m³)",
                         marker=dict(color="#3b82f6", opacity=0.8),
                         hovertemplate="<b>%{x}</b><br>Water: %{y} m³<extra></extra>"))
    fig.add_trace(go.Scatter(x=months, y=co2_avoided, name="CO₂ Avoided (kg)",
                             yaxis="y2", line=dict(color="#22c55e", width=3, shape="spline"),
                             marker=dict(size=6),
                             hovertemplate="<b>%{x}</b><br>CO₂: %{y} kg<extra></extra>"))
    fig.add_trace(go.Scatter(x=months, y=energy_saved, name="Energy Saved (kWh)",
                             yaxis="y2", line=dict(color="#f59e0b", width=2, dash="dash", shape="spline"),
                             marker=dict(size=4),
                             hovertemplate="<b>%{x}</b><br>Energy: %{y} kWh<extra></extra>"))
    fig.update_layout(
        height=400, template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(10,14,26,0.6)",
        yaxis=dict(title="Water (m³)", gridcolor="rgba(30,48,72,0.5)", tickformat=","),
        yaxis2=dict(title="CO₂ (kg) / Energy (kWh)", overlaying="y", side="right", gridcolor="rgba(30,48,72,0.3)"),
        legend=dict(orientation="h", y=-0.15, x=0.5, xanchor="center", font=dict(size=11)),
        margin=dict(t=15, b=55, l=60, r=60), font=dict(family="Inter"),
        hovermode="x unified",
        hoverlabel=dict(bgcolor="#1e293b", bordercolor="#3b82f6", font_size=12)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""
    <div class="sensor-card" style="border-left: 3px solid #10b981;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <div style="font-size:13px; font-weight:700; color:#4ade80;">Cumulative Annual Impact</div>
                <div style="font-size:12px; color:#94a3b8; margin-top:4px;">Total: {sum(water_saved):,} m³ water • {sum(co2_avoided):,} kg CO₂ • {sum(energy_saved):,} kWh energy</div>
            </div>
            <div style="font-size:18px; font-weight:800; color:#10b981;">= 70 🌳</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="section-title">Calculation Methodology</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="sensor-card">
            <div style="font-size:11px; font-weight:700; color:#3b82f6; margin-bottom:10px; letter-spacing:0.5px;">CONVERSION FACTORS</div>
            <div class="sensor-row"><span class="sensor-key">CO₂ per m³ water</span><span class="sensor-val">0.376 kg</span></div>
            <div class="sensor-row"><span class="sensor-key">Source</span><span class="sensor-val">Turkey avg (pumping + treatment)</span></div>
            <div class="sensor-row"><span class="sensor-key">Energy per m³</span><span class="sensor-val">0.8 kWh</span></div>
            <div class="sensor-row"><span class="sensor-key">Breakdown</span><span class="sensor-val">0.5 pump + 0.3 treatment</span></div>
            <div class="sensor-row"><span class="sensor-key">ASKİ tariff</span><span class="sensor-val">42.75 TRY/m³ (2025)</span></div>
            <div class="sensor-row"><span class="sensor-key">Tree absorption</span><span class="sensor-val">22 kg CO₂/year</span></div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="sensor-card">
            <div style="font-size:11px; font-weight:700; color:#10b981; margin-bottom:10px; letter-spacing:0.5px;">OPTIMIZATION TARGET</div>
            <div class="sensor-row"><span class="sensor-key">Reduction target</span><span class="sensor-val">35%</span></div>
            <div class="sensor-row"><span class="sensor-key">Method</span><span class="sensor-val">AI vs fixed-timer irrigation</span></div>
            <div class="sensor-row"><span class="sensor-key">Baseline</span><span class="sensor-val">Current consumption (ASKİ)</span></div>
            <div class="sensor-row"><span class="sensor-key">Optimal</span><span class="sensor-val">ET₀-calculated needs</span></div>
            <div class="sensor-row"><span class="sensor-key">Validation</span><span class="sensor-val">NDVI satellite correlation</span></div>
            <div class="sensor-row"><span class="sensor-key">Pilot scope</span><span class="sensor-val">3 parks, Ankara municipality</span></div>
        </div>
        """, unsafe_allow_html=True)

render_footer()
