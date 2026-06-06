# 💧 PRONUVE Water Intelligence

> Autonomous Multi-Agent Water Monitoring System  
> Built for Google for Startups AI Agents Challenge 2026 — Track 1: Build

[![Live Demo](https://img.shields.io/badge/Demo-Live-green)](https://pronuve-dashboard-646472994673.europe-west1.run.app)
[![Google ADK](https://img.shields.io/badge/Google-ADK-blue)](https://github.com/google/adk-python)
[![Gemini](https://img.shields.io/badge/Gemini-2.5-purple)](https://ai.google.dev/)
[![Cloud Run](https://img.shields.io/badge/Cloud-Run-orange)](https://cloud.google.com/run)

---

## 🌊 Overview

PRONUVE Water Intelligence is an autonomous multi-agent AI system that monitors municipal park irrigation, detects anomalies, predicts consumption, and ensures regulatory compliance — all powered by **21 specialized AI agents** orchestrated through Google ADK.

**Live Demo:** https://pronuve-dashboard-646472994673.europe-west1.run.app

---

## 🏗️ Architecture

```
                    ┌─────────────────────────────┐
                    │    ROOT ORCHESTRATOR         │
                    │    LlmAgent (Gemini 2.5)     │
                    └──────────┬──────────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        ▼                      ▼                      ▼
  ┌───────────┐     ┌──────────────────┐    ┌──────────────┐
  │  FULL     │     │  MONITORING      │    │  ON-DEMAND   │
  │  PIPELINE │     │  LOOP (×30)      │    │  QUERIES     │
  └─────┬─────┘     └──────────────────┘    └──────────────┘
        │
   Stage 1: DATA PIPELINE (SequentialAgent)
        │  → Ingest → Quality → Weather
        ▼
   Stage 2: ANALYSIS (ParallelAgent)
        │  → Water · Anomaly(5×) · Predict · NDVI · Leak
        ▼
   Stage 3: OPTIMIZATION (ParallelAgent)
        │  → Cost · Irrigation · Comparative
        ▼
   Stage 4: GOVERNANCE (SequentialAgent)
        │  → Compliance · Sustainability
        ▼
   Stage 5: OUTPUT (Human-in-the-Loop)
           → Report → Alert [Approve/Reject]
```

### ADK Patterns Used
| Pattern | Count | Usage |
|---------|-------|-------|
| SequentialAgent | 3 | Pipeline ordering |
| ParallelAgent | 3 | Concurrent analysis |
| LoopAgent | 1 | Continuous monitoring |
| Human-in-the-Loop | 1 | Alert approval |
| LlmAgent | 21 | All specialized agents |

### MCP Connections
| Server | Purpose |
|--------|---------|
| BigQuery | Consumption + sensor data |
| Earth Engine | NDVI satellite imagery |
| Weather API | Forecast + ET₀ |
| Gmail API | Alert dispatch |

---

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/ardaturak/google-ai-agents-challenge-2026.git
cd google-ai-agents-challenge-2026

# Setup
cp .env.example .env  # Add your API keys
pip install -r requirements.txt

# Run agents
python main.py

# Run dashboard
cd frontend
streamlit run app.py
```

---

## 📊 Dashboard Pages

| Page | Description |
|------|-------------|
| **Dashboard** | KPIs, 24-month trends, anomalies, forecasts, alerts |
| **Architecture** | Interactive pipeline topology, MCP/A2A, tech stack |
| **Park Details** | Per-park analysis: consumption vs optimal, NDVI, costs |
| **Sustainability** | SDG alignment (6,11,13,15), environmental impact |
| **Agent Demo** | Interactive pipeline simulation — run all 15 agents live |
| **Live Agent** | **Real Gemini API** — 11 agents execute live with context chaining |

---

## 📈 Impact (Pilot — 3 Parks, Ankara)

| Metric | Value |
|--------|-------|
| Water Saved | 4,080 m³/year |
| Cost Saved | 174,420 TRY/year |
| CO₂ Avoided | 1,534 kg/year |
| Energy Saved | 3,264 kWh/year |
| SDG Alignment | 6, 11, 13, 15 |

---

## 🤝 Partnership

- **ProgenX** — AI startup (Ankara, Turkey)
- **PRONUVE** — Academic research project (METU/ODTÜ)
- **TÜBİTAK** — Funded research
- **ASKİ** — Data partnership (Ankara Water Authority)

---

## 📋 Data Notice

This submission uses anonymized sample data derived from real municipal park monitoring systems. Full production dataset (100,000+ records) available for judge verification upon request.

Contact: info@progenxacademy.com

---

## 🛠️ Tech Stack

**AI/Agents:** Google ADK · Gemini 2.5 Flash · Gemini 2.5 Pro · MCP · A2A  
**Cloud:** Cloud Run · BigQuery · Earth Engine · Gmail API · Cloud Storage  
**Backend:** Python 3.12 · FastAPI · Pydantic · NumPy  
**Frontend:** Streamlit · Plotly · Pandas  
**Data:** ASKİ · IoT Sensors (ESP32) · Sentinel-2 · OpenMeteo  

---

## 📄 License

Apache 2.0
