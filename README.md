# PRONUVE Water Intelligence

> Autonomous Multi-Agent Water Quality Monitoring System  
> Built with Google Agent Development Kit (ADK) | Gemini | Cloud Run

## Overview

PRONUVE is an AI-powered water intelligence platform that monitors municipal park irrigation using **21 specialized agents** orchestrated through Google ADK patterns. The system detects anomalies, predicts consumption, optimizes costs, and ensures regulatory compliance — all autonomously.

## Architecture

```
pronuve_orchestrator (LlmAgent - gemini-2.5-flash)
├── full_pipeline (SequentialAgent)
│   ├── data_pipeline (SequentialAgent)
│   │   ├── data_ingest_agent
│   │   ├── data_quality_agent
│   │   └── weather_agent
│   ├── parallel_analysis (ParallelAgent)
│   │   ├── water_analysis_agent
│   │   ├── anomaly_detection (ParallelAgent - 5 methods)
│   │   │   ├── zscore_detector
│   │   │   ├── iqr_detector
│   │   │   ├── moving_avg_detector
│   │   │   ├── isolation_forest_detector
│   │   │   └── cusum_detector
│   │   ├── prediction_agent (gemini-2.5-pro)
│   │   ├── ndvi_agent
│   │   └── leak_detection_agent
│   ├── optimization_layer (ParallelAgent)
│   │   ├── cost_optimization_agent
│   │   ├── irrigation_scheduler_agent
│   │   └── comparative_agent
│   ├── governance_pipeline (SequentialAgent)
│   │   ├── compliance_agent
│   │   └── sustainability_agent
│   ├── report_agent
│   └── alert_agent (Human-in-the-Loop)
└── monitoring_loop (LoopAgent - 30 iterations)
```

## Key Features

| Feature | Agent(s) | ADK Pattern |
|---------|----------|-------------|
| Data ingestion + validation | data_ingest, data_quality | Sequential |
| 5-method anomaly consensus | zscore, iqr, ma, iforest, cusum | Parallel |
| Consumption forecasting | prediction_agent | LlmAgent |
| Satellite vegetation health | ndvi_agent | LlmAgent |
| Leak detection | leak_detection_agent | LlmAgent |
| Cost optimization | cost_optimization_agent | LlmAgent |
| Smart irrigation scheduling | irrigation_scheduler_agent | LlmAgent |
| Park benchmarking | comparative_agent | Parallel |
| Regulatory compliance | compliance_agent | Sequential |
| Sustainability scoring | sustainability_agent | LlmAgent |
| Alert with human approval | alert_agent | Human-in-Loop |
| Continuous monitoring | monitoring_loop | LoopAgent |

## Technology Stack

- **Agent Framework:** Google ADK (SequentialAgent, ParallelAgent, LoopAgent, LlmAgent)
- **Models:** Gemini 2.5 Flash (speed) + Gemini 2.5 Pro (complex reasoning)
- **MCP Servers:** BigQuery, Google Earth Engine, Weather API, Gmail
- **A2A Protocol:** Inter-agent communication with municipal systems
- **Backend:** FastAPI + Cloud Run (serverless)
- **Frontend:** Streamlit dashboard (real-time monitoring)
- **Data:** BigQuery (ASKİ water data + IoT sensors)
- **Deployment:** Docker → Google Cloud Run

## Quick Start

```bash
# Clone
git clone https://github.com/progenx/pronuve-agent.git
cd pronuve-agent

# Install
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your GCP credentials

# Run API
python main.py

# Run Dashboard
cd frontend && streamlit run app.py
```

## Demo

The dashboard shows:
1. **Overview** — KPIs, consumption trends, anomaly annotations
2. **Anomalies** — Multi-method consensus detection results
3. **Predictions** — 30/60/90 day forecasts with confidence bands
4. **Alerts** — Human-in-the-loop approval workflow
5. **Agent Log** — Real-time agent activity stream
6. **Architecture** — Full system topology
7. **Park Details** — Per-park deep dive
8. **Sustainability** — SDG alignment and environmental impact

## Real-World Impact

- **Partnership:** ASKİ (Ankara Water Authority) — active data collaboration
- **Data:** Real consumption data from 35+ municipal parks
- **Funding:** TÜBİTAK research grant
- **Academic:** METU Computer Engineering collaboration
- **Savings:** Projected 174,000 TRY/year water cost reduction across pilot parks

## ADK Patterns Demonstrated

1. **SequentialAgent** — Ordered pipeline stages (data → analysis → report)
2. **ParallelAgent** — Concurrent anomaly detection (5 methods simultaneously)
3. **LoopAgent** — Continuous monitoring with configurable intervals
4. **Human-in-the-Loop** — Critical alert approval before external dispatch
5. **State Management** — Cross-agent data sharing via ADK state
6. **MCP Integration** — External data sources via Model Context Protocol
7. **A2A Protocol** — Inter-system agent communication

## Team

**ProgenX** — Software & AI company (Ankara, Turkey)  
Partner: PRONUVE Water Technologies

---

*Built for Google for Startups AI Agents Challenge 2026*
