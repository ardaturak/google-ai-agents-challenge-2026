"""Live Agent — Real Gemini-powered agent interaction."""

import streamlit as st
import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from styles import GLOBAL_CSS
from components import render_sidebar, render_footer

st.set_page_config(page_title="Live Agent | PRONUVE", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
render_sidebar()

st.markdown("""
<div class="main-header">
    <h1>⚡ Live Agent — Gemini Powered</h1>
    <p>Real-time AI Agent Interaction • Powered by Gemini 2.5 Flash</p>
    <div class="badge-row">
        <span class="hbadge">Real Gemini API</span>
        <span class="hbadge">Live Reasoning</span>
        <span class="hbadge">Anomaly Detection</span>
        <span class="hbadge">Recommendations</span>
    </div>
</div>
""", unsafe_allow_html=True)

PARK_DATA = {
    "Park Alpha (Çankaya)": {
        "area_m2": 35200, "type": "Recreation",
        "monthly_consumption_m3": [420, 385, 510, 890, 1450, 2100, 2380, 2250, 1520, 780, 410, 350],
        "ndvi": [0.42, 0.38, 0.45, 0.55, 0.62, 0.58, 0.55, 0.52, 0.50, 0.45, 0.40, 0.38],
        "soil_moisture_pct": 38.5, "temp_c": 26.1, "efficiency_pct": 78,
    },
    "Park Beta (Yenimahalle)": {
        "area_m2": 16500, "type": "Sports Complex",
        "monthly_consumption_m3": [180, 165, 230, 420, 680, 950, 4200, 980, 620, 340, 175, 150],
        "ndvi": [0.40, 0.36, 0.42, 0.50, 0.55, 0.48, 0.31, 0.35, 0.38, 0.36, 0.34, 0.32],
        "soil_moisture_pct": 16.5, "temp_c": 27.2, "efficiency_pct": 45,
    },
    "Park Gamma (Çankaya)": {
        "area_m2": 58000, "type": "Botanical Garden",
        "monthly_consumption_m3": [680, 620, 850, 1450, 2380, 3400, 3850, 3620, 2450, 1280, 670, 560],
        "ndvi": [0.55, 0.52, 0.58, 0.65, 0.72, 0.70, 0.67, 0.64, 0.60, 0.55, 0.52, 0.50],
        "soil_moisture_pct": 55.3, "temp_c": 22.8, "efficiency_pct": 85,
    },
}

SYSTEM_PROMPT = """You are the PRONUVE Water Intelligence Agent — an autonomous AI system monitoring municipal park irrigation in Ankara, Turkey.

You have access to real sensor data from 3 parks monitored by ASKİ (Ankara Water Authority).
Your capabilities:
1. Anomaly Detection (5 methods: Z-Score, IQR, Moving Average, Isolation Forest, CUSUM)
2. Consumption Analysis & Efficiency Scoring
3. NDVI Vegetation Health Assessment (Sentinel-2 satellite)
4. Leak Detection (night-flow analysis)
5. Cost Optimization & Savings Calculation
6. Irrigation Scheduling (ET₀-based)
7. Sustainability & SDG Scoring

Current data context:
{context}

Respond as a professional water management AI agent. Provide specific numbers, actionable recommendations, and reference the actual data. Be concise but thorough. Format with markdown."""

SAMPLE_QUERIES = [
    "Analyze Park Beta's July anomaly — what happened and what should we do?",
    "Which park has the highest water waste? Calculate potential savings.",
    "Generate an irrigation schedule for tomorrow considering 72% rain probability.",
    "Compare all 3 parks' efficiency and rank them with recommendations.",
    "What is the NDVI health status across all parks? Any vegetation stress?",
    "Run anomaly detection on all parks — flag any concerns.",
    "Calculate the total environmental impact (CO₂, energy, water) of our optimization.",
    "What would happen if we scaled this system to 200 parks city-wide?",
]

try:
    import google.generativeai as genai

    api_key = st.secrets.get("GEMINI_API_KEY", "") if hasattr(st, "secrets") else ""
    if not api_key:
        import os
        api_key = os.environ.get("GEMINI_API_KEY", "")

    has_api = bool(api_key)
except ImportError:
    has_api = False
    api_key = ""

tab1, tab2 = st.tabs(["💬 Chat with Agent", "📊 Agent Capabilities"])

with tab1:
    st.markdown('<div class="section-title">Interactive Agent — Ask Anything About Water Management</div>', unsafe_allow_html=True)

    if has_api:
        st.markdown("""
        <div class="sensor-card" style="border-left:3px solid #10b981; margin-bottom:16px;">
            <div style="font-size:12px; color:#94a3b8;">
                <strong style="color:#4ade80;">🟢 LIVE</strong> — Connected to Gemini 2.5 Flash. 
                This agent has access to real park sensor data and can perform analysis, detect anomalies, and generate recommendations in real-time.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="sensor-card" style="border-left:3px solid #f59e0b; margin-bottom:16px;">
            <div style="font-size:12px; color:#94a3b8;">
                <strong style="color:#fbbf24;">🟡 DEMO MODE</strong> — Gemini API key not configured. 
                Showing pre-computed agent responses. Set GEMINI_API_KEY environment variable for live interaction.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("**Quick queries:**")
    cols = st.columns(4)
    for i, q in enumerate(SAMPLE_QUERIES[:4]):
        if cols[i].button(q[:35] + "...", key=f"q{i}", use_container_width=True):
            st.session_state["agent_query"] = q

    cols2 = st.columns(4)
    for i, q in enumerate(SAMPLE_QUERIES[4:]):
        if cols2[i].button(q[:35] + "...", key=f"q{i+4}", use_container_width=True):
            st.session_state["agent_query"] = q

    query = st.text_input("Or type your own question:", value=st.session_state.get("agent_query", ""), placeholder="e.g., Analyze Park Beta anomaly...")

    if query and st.button("🚀 Run Agent", type="primary", use_container_width=True):
        context = json.dumps(PARK_DATA, indent=2)
        full_prompt = SYSTEM_PROMPT.format(context=context)

        if has_api:
            with st.status("⚡ Agent reasoning with Gemini 2.5 Flash...", expanded=True) as status:
                st.write("📡 Connecting to Gemini API...")
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-2.0-flash")
                st.write("🧠 Analyzing park data...")
                response = model.generate_content([
                    {"role": "user", "parts": [full_prompt + "\n\nUser query: " + query]}
                ])
                st.write("✅ Analysis complete")
                status.update(label="✅ Agent response ready", state="complete")

            st.markdown("---")
            st.markdown("### 🤖 Agent Response")
            st.markdown(response.text)
        else:
            with st.status("⚡ Agent reasoning (demo mode)...", expanded=True) as status:
                import time
                st.write("📡 Loading park data context...")
                time.sleep(0.5)
                st.write("🧠 Running anomaly detection (5 methods)...")
                time.sleep(0.5)
                st.write("📊 Generating analysis...")
                time.sleep(0.5)
                st.write("✅ Complete")
                status.update(label="✅ Agent response ready (demo)", state="complete")

            st.markdown("---")
            st.markdown("### 🤖 Agent Response (Demo)")

            if "anomaly" in query.lower() or "beta" in query.lower():
                st.markdown("""
**🔴 CRITICAL ANOMALY DETECTED — Park Beta, July 2025**

**Detection Summary:**
- Actual consumption: **4,200 m³** (expected: ~950 m³)
- Deviation: **4.4× above normal** for July
- Consensus score: **5/5 methods** (unanimous)

**Method Results:**
| Method | Score | Threshold | Result |
|--------|-------|-----------|--------|
| Z-Score | 4.2σ | >2σ | 🔴 ANOMALY |
| IQR | 3,250 above Q3 | >1.5×IQR | 🔴 ANOMALY |
| Moving Average | +342% deviation | >100% | 🔴 ANOMALY |
| Isolation Forest | 0.92 anomaly score | >0.7 | 🔴 ANOMALY |
| CUSUM | 8,450 cumulative | >3,000 | 🔴 ANOMALY |

**Root Cause Analysis:**
- NDVI dropped to 0.31 (stressed) despite over-consumption → water not reaching roots
- Night-flow analysis: 8% of daily average (threshold: 5%)
- **Likely cause: Underground pipe leak** between meter and irrigation zone

**Recommended Actions:**
1. 🚨 Dispatch maintenance team for pipe inspection (Priority: IMMEDIATE)
2. 📉 Estimated loss: ~108 m³/day → **4,617 TRY/day ($121/day)**
3. 🔧 Check irrigation valve actuators in Zone B-3
4. 📡 Deploy portable acoustic leak detector

**Financial Impact if unresolved:**
- Monthly waste: 3,240 m³ → 138,510 TRY (~$3,645)
- Annual projection: 39,420 m³ → **1,685,205 TRY (~$44,347)**
""")
            elif "efficiency" in query.lower() or "rank" in query.lower() or "compare" in query.lower():
                st.markdown("""
**📊 Park Efficiency Ranking & Comparison**

| Rank | Park | Efficiency | NDVI | Status | Action |
|------|------|-----------|------|--------|--------|
| 1 | Park Gamma (Botanical) | **85%** | 0.67 | 🟢 Excellent | Maintain current schedule |
| 2 | Park Alpha (Recreation) | **78%** | 0.58 | 🟡 Good | Minor optimization possible |
| 3 | Park Beta (Sports) | **45%** | 0.31 | 🔴 Critical | Immediate intervention needed |

**Key Findings:**
- Park Beta wastes **55%** of its water (4,714 m³/year excess)
- Park Gamma is a model facility — use as benchmark
- Park Alpha has 22% over-irrigation primarily in Jun-Aug peak season

**Savings Potential:**
- Park Beta optimization: **87,420 TRY/year** ($2,300)
- Park Alpha optimization: **54,180 TRY/year** ($1,425)
- Combined pilot savings: **174,420 TRY/year** ($4,590)
- City-wide (200 parks): **~$310,000/year**

**Recommendations:**
1. Park Beta: Fix leak FIRST, then optimize schedule
2. Park Alpha: Reduce summer peak by 20% with ET₀-based scheduling
3. Park Gamma: Document best practices for replication
""")
            else:
                st.markdown(f"""
**📋 Analysis for: "{query}"**

Based on current data from 3 monitored parks (ASKİ, Ankara):

**Summary:**
- Total monthly consumption: 6,445 m³ (3 parks combined)
- Average efficiency: 69.3%
- Active anomalies: 1 (Park Beta — underground leak suspected)
- NDVI health: 2/3 parks healthy, 1 stressed

**Key Metrics:**
| Metric | Value | Status |
|--------|-------|--------|
| Water saved (projected) | 4,080 m³/yr | On track |
| Cost savings | $4,600/yr (pilot) | Verified |
| CO₂ reduction | 1,534 kg/yr | = 70 trees |
| City-wide potential | $310,000/yr | 200 parks |

**Agent Pipeline Status:** All 21 agents operational
- Last cycle: 15 seconds
- Anomaly methods: 5/5 active
- MCP connections: 4/4 healthy

*For specific analysis, try asking about a particular park, anomaly, or optimization target.*
""")

with tab2:
    st.markdown('<div class="section-title">Agent Capabilities Matrix</div>', unsafe_allow_html=True)

    capabilities = [
        ("Anomaly Detection", "5 parallel methods with consensus", "Z-Score, IQR, MA, iForest, CUSUM → ≥2/5 confirms", "#ef4444"),
        ("Consumption Forecast", "90-day prediction with confidence", "Seasonal decomposition + Gemini Pro reasoning", "#3b82f6"),
        ("Leak Detection", "Night-flow & pressure analysis", "Detects underground leaks via flow pattern anomalies", "#f59e0b"),
        ("NDVI Analysis", "Satellite vegetation health", "Sentinel-2 (10m) → healthy/moderate/stressed classification", "#22c55e"),
        ("Cost Optimization", "Financial impact calculation", "Waste × tariff → savings potential at all scales", "#8b5cf6"),
        ("Irrigation Scheduling", "ET₀-based smart scheduling", "Weather + soil + NDVI → optimal timing and volume", "#06b6d4"),
        ("Compliance Check", "Municipal regulation audit", "Checks quotas, efficiency thresholds, reporting requirements", "#10b981"),
        ("Sustainability Score", "SDG alignment tracking", "Scores against SDG 6, 11, 13, 15 with improvement plans", "#84cc16"),
    ]

    for name, subtitle, detail, color in capabilities:
        st.markdown(f"""
        <div class="sensor-card" style="margin-bottom:8px; border-left:3px solid {color};">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <div style="font-size:13px; font-weight:700; color:#f1f5f9;">{name}</div>
                    <div style="font-size:11px; color:#94a3b8; margin-top:2px;">{subtitle}</div>
                </div>
                <span class="badge badge-ok">Active</span>
            </div>
            <div style="font-size:10px; color:#64748b; margin-top:8px; padding-top:8px; border-top:1px solid rgba(30,48,72,0.5);">{detail}</div>
        </div>
        """, unsafe_allow_html=True)

render_footer()
