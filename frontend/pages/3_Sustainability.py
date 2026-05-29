"""Sustainability — SDG alignment and environmental impact."""

import streamlit as st
import plotly.graph_objects as go
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from styles import GLOBAL_CSS

st.set_page_config(page_title="Sustainability | PRONUVE", page_icon="🌍", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🌍 Sustainability & SDG Alignment</h1>
    <p>Environmental Impact • UN Sustainable Development Goals • CO₂ Tracking</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="kpi-row">
    <div class="kpi-card"><div class="kpi-value">4,080</div><div class="kpi-label">Water Saved (m³/yr)</div><div class="kpi-delta up">Projected</div></div>
    <div class="kpi-card"><div class="kpi-value">1,534</div><div class="kpi-label">CO₂ Avoided (kg/yr)</div><div class="kpi-delta up">= 70 trees</div></div>
    <div class="kpi-card"><div class="kpi-value">3,264</div><div class="kpi-label">Energy Saved (kWh/yr)</div><div class="kpi-delta up">Pump reduction</div></div>
    <div class="kpi-card"><div class="kpi-value">174K</div><div class="kpi-label">Cost Saved (TRY/yr)</div><div class="kpi-delta up">Pilot parks</div></div>
    <div class="kpi-card"><div class="kpi-value">72</div><div class="kpi-label">Sustainability Score</div><div class="kpi-delta up">↑ improving</div></div>
    <div class="kpi-card"><div class="kpi-value">4</div><div class="kpi-label">SDGs Addressed</div><div class="kpi-delta up">6, 11, 13, 15</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-title">UN SDG Scores</div>', unsafe_allow_html=True)

sdgs = [
    ("SDG 6", "Clean Water & Sanitation", 82, "#3b82f6"),
    ("SDG 11", "Sustainable Cities", 76, "#22c55e"),
    ("SDG 13", "Climate Action", 68, "#eab308"),
    ("SDG 15", "Life on Land", 71, "#a855f7"),
]

cols = st.columns(4)
for col, (name, title, score, color) in zip(cols, sdgs):
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=score,
        gauge={"axis": {"range": [0, 100], "tickcolor": "#334155", "tickfont": {"size": 10}},
               "bar": {"color": color, "thickness": 0.7},
               "bgcolor": "#1e293b", "borderwidth": 0,
               "steps": [{"range": [0, 50], "color": "#0f172a"}, {"range": [50, 100], "color": "#1e293b"}]},
        number={"suffix": "", "font": {"size": 32, "color": "#f1f5f9", "family": "Inter"}},
    ))
    fig.update_layout(height=150, margin=dict(t=25, b=0, l=15, r=15),
                      paper_bgcolor="rgba(0,0,0,0)", font=dict(family="Inter"))
    col.markdown(f"**{name}:** {title}")
    col.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown('<div class="section-title">Monthly Environmental Impact (2025)</div>', unsafe_allow_html=True)

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
fig = go.Figure()
fig.add_trace(go.Bar(x=months, y=[120, 95, 180, 320, 480, 560], name="Water Saved (m³)",
                     marker_color="#3b82f6", opacity=0.8))
fig.add_trace(go.Scatter(x=months, y=[45, 36, 68, 120, 180, 211], name="CO₂ Avoided (kg)",
                         yaxis="y2", line=dict(color="#22c55e", width=2.5), marker=dict(size=6)))
fig.update_layout(
    height=320, template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(15,23,42,0.5)",
    yaxis=dict(title="Water (m³)", gridcolor="#1e293b"),
    yaxis2=dict(title="CO₂ (kg)", overlaying="y", side="right", gridcolor="#1e293b"),
    legend=dict(orientation="h", y=-0.15), margin=dict(t=15, b=50, l=55, r=55),
    font=dict(family="Inter"),
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown('<div class="section-title">Impact Calculations</div>', unsafe_allow_html=True)
st.markdown("""
| Factor | Value | Source |
|--------|-------|--------|
| CO₂ per m³ water | 0.376 kg | Turkey avg (pumping + treatment) |
| Energy per m³ | 0.8 kWh | 0.5 kWh pump + 0.3 kWh treatment |
| ASKİ water tariff | 42.75 TRY/m³ | 2025 municipal rate |
| Tree CO₂ absorption | 22 kg/year | Standard calculation |
| Target reduction | 35% | AI-optimized vs fixed-timer irrigation |
""")
