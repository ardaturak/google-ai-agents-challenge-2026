"""Park Details — Per-park deep dive analysis."""

import streamlit as st
import plotly.graph_objects as go
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from styles import GLOBAL_CSS

st.set_page_config(page_title="Park Details | PRONUVE", page_icon="🌳", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
PARKS = {
    "Park Alpha — Çankaya (Recreation)": {
        "area": 35200, "efficiency": 78, "compliance": 92, "leak": "Low", "ndvi_avg": 0.58,
        "consumption": [420, 385, 510, 890, 1450, 2100, 2380, 2250, 1520, 780, 410, 350],
        "ndvi": [0.42, 0.38, 0.45, 0.55, 0.62, 0.58, 0.55, 0.52, 0.50, 0.45, 0.40, 0.38],
    },
    "Park Beta — Yenimahalle (Sports)": {
        "area": 16500, "efficiency": 45, "compliance": 58, "leak": "HIGH ⚠️", "ndvi_avg": 0.31,
        "consumption": [180, 165, 230, 420, 680, 950, 4200, 980, 620, 340, 175, 150],
        "ndvi": [0.40, 0.36, 0.42, 0.50, 0.55, 0.48, 0.31, 0.35, 0.38, 0.36, 0.34, 0.32],
    },
    "Park Gamma — Çankaya (Botanical)": {
        "area": 58000, "efficiency": 85, "compliance": 96, "leak": "Low", "ndvi_avg": 0.67,
        "consumption": [680, 620, 850, 1450, 2380, 3400, 3850, 3620, 2450, 1280, 670, 560],
        "ndvi": [0.55, 0.52, 0.58, 0.65, 0.72, 0.70, 0.67, 0.64, 0.60, 0.55, 0.52, 0.50],
    },
}

st.markdown("""
<div class="main-header">
    <h1>🌳 Park Details</h1>
    <p>Individual park analysis • Consumption vs Optimal • NDVI Health • Cost Impact</p>
</div>
""", unsafe_allow_html=True)

selected = st.selectbox("Select Park", list(PARKS.keys()), label_visibility="collapsed")
park = PARKS[selected]

cols = st.columns(5)
cols[0].metric("Area", f"{park['area']:,} m²")
cols[1].metric("Efficiency", f"{park['efficiency']}%")
cols[2].metric("Compliance", f"{park['compliance']}%")
cols[3].metric("Leak Risk", park["leak"])
cols[4].metric("Avg NDVI", f"{park['ndvi_avg']}")

st.markdown("---")
tab1, tab2, tab3 = st.tabs(["📊 Consumption vs Optimal", "🛰️ Vegetation Health", "💰 Cost Impact"])

with tab1:
    fig = go.Figure()
    fig.add_trace(go.Bar(x=MONTHS, y=park["consumption"], name="Actual Consumption",
                         marker_color="#3b82f6", opacity=0.85))
    optimal = [int(c * 0.65) for c in park["consumption"]]
    fig.add_trace(go.Scatter(x=MONTHS, y=optimal, name="Optimal (ET₀ based)",
                             line=dict(color="#22c55e", dash="dash", width=2.5)))
    fig.update_layout(height=360, template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(15,23,42,0.5)", yaxis_title="m³",
                      legend=dict(orientation="h", y=-0.15), margin=dict(t=15, b=50, l=55, r=15),
                      xaxis=dict(gridcolor="#1e293b"), yaxis=dict(gridcolor="#1e293b"),
                      font=dict(family="Inter"))
    st.plotly_chart(fig, use_container_width=True)
    waste_pct = round((1 - sum(optimal) / sum(park["consumption"])) * 100)
    st.info(f"**{waste_pct}% over-irrigation** detected relative to ET₀-calculated optimal needs.")

with tab2:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=MONTHS, y=park["ndvi"], mode="lines+markers", name="NDVI",
                             line=dict(color="#22c55e", width=2.5), fill="tozeroy",
                             fillcolor="rgba(34,197,94,0.06)", marker=dict(size=6)))
    fig.add_hline(y=0.5, line_dash="dash", line_color="#eab308",
                  annotation_text="Healthy Threshold (0.5)", annotation_font_color="#eab308")
    fig.add_hline(y=0.35, line_dash="dot", line_color="#ef4444",
                  annotation_text="Stressed (<0.35)", annotation_font_color="#ef4444")
    fig.update_layout(height=320, template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(15,23,42,0.5)", yaxis=dict(title="NDVI (0–1)", range=[0, 1], gridcolor="#1e293b"),
                      xaxis=dict(gridcolor="#1e293b"), margin=dict(t=15, b=40, l=55, r=15),
                      font=dict(family="Inter"))
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    total = sum(park["consumption"])
    optimal_total = int(total * 0.65)
    waste = total - optimal_total
    cost_total = total * 42.75
    cost_waste = waste * 42.75
    co2 = total * 0.376

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Annual Total", f"{total:,} m³")
    c2.metric("Annual Cost", f"{cost_total:,.0f} TRY")
    c3.metric("Potential Savings", f"{cost_waste:,.0f} TRY/yr")
    c4.metric("CO₂ Footprint", f"{co2:,.0f} kg/yr")

    st.markdown(f"""
    ---
    **ASKİ Tariff:** 42.75 TRY/m³ (water + wastewater surcharge)

    | Metric | Value |
    |--------|-------|
    | Cost per m² | {cost_total / park['area']:.2f} TRY/m²/year |
    | Waste volume | {waste:,} m³/year ({waste_pct}%) |
    | CO₂ equivalent | {co2 / 22:.0f} trees needed to offset |
    | Energy waste | {waste * 0.8:,.0f} kWh/year |
    """)
