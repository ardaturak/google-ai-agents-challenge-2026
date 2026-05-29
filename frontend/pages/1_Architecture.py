"""Architecture — Agent topology and system design."""

import streamlit as st
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from styles import GLOBAL_CSS

st.set_page_config(page_title="Architecture | PRONUVE", page_icon="🏗️", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🏗️ System Architecture</h1>
    <p>21 Agents • 5 ADK Patterns • 4 MCP Servers • A2A Protocol</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-title">Agent Hierarchy & Data Flow</div>', unsafe_allow_html=True)

st.code("""
╔══════════════════════════════════════════════════════════════════════════╗
║                    PRONUVE ORCHESTRATOR (root)                          ║
║                    LlmAgent • gemini-2.5-flash                         ║
╚══════════════════════╦═══════════════════════════╦═══════════════════════╝
                       ▼                           ▼
        ┌──────────────────────────┐    ┌─────────────────────┐
        │   FULL PIPELINE          │    │   MONITORING LOOP   │
        │   SequentialAgent        │    │   LoopAgent (×30)   │
        └──────────┬───────────────┘    └─────────────────────┘
                   ▼
   ╔═══════════════════════════════════╗
   ║  STAGE 1: DATA PIPELINE          ║  SequentialAgent
   ║  ┌──────────┬──────────┬───────┐ ║
   ║  │  Ingest  │ Quality  │Weather│ ║  ← BigQuery MCP, Weather MCP
   ║  └──────────┴──────────┴───────┘ ║
   ╚═══════════════╦═══════════════════╝
                   ▼
   ╔═══════════════════════════════════════════════════════════╗
   ║  STAGE 2: ANALYSIS LAYER                ParallelAgent    ║
   ║  ┌─────────┬──────────────────┬────────┬──────┬──────┐  ║
   ║  │ Water   │ ANOMALY (5×Para) │Predict │ NDVI │ Leak │  ║
   ║  │Analysis │ ┌───┬───┬───┬──┐ │(Pro)   │(EE)  │Detect│  ║
   ║  │         │ │Z  │IQR│MA │IF│ │        │      │      │  ║
   ║  │         │ │   │   │   │  │ │        │      │      │  ║
   ║  │         │ └───┴───┴───┴──┘ │        │      │      │  ║
   ║  │         │ + CUSUM→Consensus │        │      │      │  ║
   ║  └─────────┴──────────────────┴────────┴──────┴──────┘  ║
   ╚═══════════════════════╦═══════════════════════════════════╝
                           ▼
   ╔═══════════════════════════════════════════╗
   ║  STAGE 3: OPTIMIZATION     ParallelAgent ║
   ║  ┌──────────┬────────────┬─────────────┐ ║
   ║  │   Cost   │ Irrigation │ Comparative │ ║
   ║  │Optimizer │ Scheduler  │  Benchmark  │ ║
   ║  └──────────┴────────────┴─────────────┘ ║
   ╚═══════════════════╦═══════════════════════╝
                       ▼
   ╔═══════════════════════════════════╗
   ║  STAGE 4: GOVERNANCE  Sequential ║
   ║  ┌────────────┬──────────────┐   ║
   ║  │ Compliance │Sustainability│   ║
   ║  └────────────┴──────────────┘   ║
   ╚═══════════════════╦═══════════════╝
                       ▼
        ┌──────────────────────────────────────────┐
        │  STAGE 5: OUTPUT                         │
        │  Report Generator → Alert Agent (HITL)   │  ← Gmail MCP
        │                     ↓                    │
        │              [Human Approval]            │
        │         Approve / Modify / Reject        │
        └──────────────────────────────────────────┘
""", language="text")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="section-title">ADK Patterns</div>', unsafe_allow_html=True)
    st.markdown("""
| Pattern | Count | Usage |
|---------|-------|-------|
| **SequentialAgent** | 3 | Pipeline stages (ordered) |
| **ParallelAgent** | 3 | Anomaly×5, Analysis×5, Opt×3 |
| **LoopAgent** | 1 | Continuous monitoring (30 iter) |
| **Human-in-the-Loop** | 1 | Alert approval gate |
| **LlmAgent** | 21 | All specialized agents |
    """)

with col2:
    st.markdown('<div class="section-title">MCP & A2A Connections</div>', unsafe_allow_html=True)
    st.markdown("""
| Protocol | Server | Purpose |
|----------|--------|---------|
| **MCP** | BigQuery | Consumption + sensor data |
| **MCP** | Earth Engine | NDVI satellite imagery |
| **MCP** | Weather API | Forecast + ET₀ |
| **MCP** | Gmail API | Alert dispatch |
| **A2A** | Municipal Sys | Work orders |
| **A2A** | IoT Gateway | Valve control |
    """)

st.markdown("---")
st.markdown('<div class="section-title">Technology Stack</div>', unsafe_allow_html=True)
st.markdown("""
**AI/Agent:** `Google ADK` `Gemini 2.5 Flash` `Gemini 2.5 Pro` `MCP` `A2A`

**Cloud:** `Cloud Run` `BigQuery` `Earth Engine` `Vertex AI` `Gmail API` `Cloud Storage`

**Backend:** `Python 3.12` `FastAPI` `Pydantic` `NumPy` `Docker`

**Frontend:** `Streamlit` `Plotly` `Pandas`

**Data:** `ASKİ Water Authority` `IoT Sensors (ESP32)` `Sentinel-2 Satellite` `OpenMeteo`
""")
