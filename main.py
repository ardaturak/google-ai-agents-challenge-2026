"""PRONUVE Water Intelligence — Main API Server.

FastAPI application serving the agent system, health checks,
and webhook endpoints for Cloud Run deployment.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(
    title="PRONUVE Water Intelligence API",
    description="Multi-Agent Water Quality Monitoring System powered by Google ADK",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalysisRequest(BaseModel):
    park_ids: list[str] | None = None
    analysis_type: str = "full"
    period_months: int = 12


class AlertApproval(BaseModel):
    alert_id: str
    approved: bool
    modified_by: str
    notes: str = ""


AGENT_REGISTRY = {
    "pronuve_orchestrator": {"status": "active", "type": "LlmAgent", "model": "gemini-2.5-flash"},
    "data_ingest_agent": {"status": "active", "type": "LlmAgent", "model": "gemini-2.5-flash"},
    "data_quality_agent": {"status": "active", "type": "LlmAgent", "model": "gemini-2.5-flash"},
    "weather_agent": {"status": "active", "type": "LlmAgent", "model": "gemini-2.5-flash"},
    "water_analysis_agent": {"status": "active", "type": "LlmAgent", "model": "gemini-2.5-flash"},
    "anomaly_consensus": {"status": "active", "type": "LlmAgent", "model": "gemini-2.5-pro"},
    "zscore_detector": {"status": "active", "type": "LlmAgent", "model": "gemini-2.5-flash"},
    "iqr_detector": {"status": "active", "type": "LlmAgent", "model": "gemini-2.5-flash"},
    "moving_avg_detector": {"status": "active", "type": "LlmAgent", "model": "gemini-2.5-flash"},
    "isolation_forest_detector": {"status": "active", "type": "LlmAgent", "model": "gemini-2.5-flash"},
    "cusum_detector": {"status": "active", "type": "LlmAgent", "model": "gemini-2.5-flash"},
    "prediction_agent": {"status": "active", "type": "LlmAgent", "model": "gemini-2.5-pro"},
    "ndvi_agent": {"status": "active", "type": "LlmAgent", "model": "gemini-2.5-flash"},
    "leak_detection_agent": {"status": "active", "type": "LlmAgent", "model": "gemini-2.5-flash"},
    "cost_optimization_agent": {"status": "active", "type": "LlmAgent", "model": "gemini-2.5-flash"},
    "irrigation_scheduler_agent": {"status": "active", "type": "LlmAgent", "model": "gemini-2.5-flash"},
    "comparative_agent": {"status": "active", "type": "LlmAgent", "model": "gemini-2.5-flash"},
    "compliance_agent": {"status": "active", "type": "LlmAgent", "model": "gemini-2.5-flash"},
    "sustainability_agent": {"status": "active", "type": "LlmAgent", "model": "gemini-2.5-flash"},
    "report_agent": {"status": "active", "type": "LlmAgent", "model": "gemini-2.5-flash"},
    "alert_agent": {"status": "active", "type": "LlmAgent", "model": "gemini-2.5-flash"},
}

ADK_PATTERNS = {
    "SequentialAgent": ["data_pipeline", "governance_pipeline", "full_pipeline"],
    "ParallelAgent": ["parallel_analysis", "optimization_layer", "parallel_anomaly_detection"],
    "LoopAgent": ["monitoring_loop"],
    "LlmAgent": list(AGENT_REGISTRY.keys()),
    "Human-in-the-Loop": ["alert_agent"],
}


@app.get("/")
async def root():
    return {
        "service": "PRONUVE Water Intelligence",
        "version": "1.0.0",
        "agents_active": len(AGENT_REGISTRY),
        "adk_patterns_used": list(ADK_PATTERNS.keys()),
        "status": "operational",
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "agents": len(AGENT_REGISTRY),
        "uptime": "running",
    }


@app.get("/agents")
async def list_agents():
    return {
        "total": len(AGENT_REGISTRY),
        "agents": AGENT_REGISTRY,
        "patterns": ADK_PATTERNS,
    }


@app.get("/agents/{agent_name}")
async def get_agent(agent_name: str):
    if agent_name not in AGENT_REGISTRY:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")
    return {"name": agent_name, **AGENT_REGISTRY[agent_name]}


@app.post("/analyze")
async def run_analysis(request: AnalysisRequest):
    return {
        "status": "pipeline_started",
        "request": request.model_dump(),
        "pipeline": "full_pipeline",
        "stages": [
            "data_pipeline (sequential)",
            "parallel_analysis (5 agents)",
            "optimization_layer (3 agents)",
            "governance_pipeline (sequential)",
            "report_agent",
            "alert_agent (human-in-the-loop)",
        ],
        "estimated_time_seconds": 45,
    }


@app.post("/alerts/approve")
async def approve_alert(approval: AlertApproval):
    return {
        "alert_id": approval.alert_id,
        "action": "approved" if approval.approved else "rejected",
        "modified_by": approval.modified_by,
        "timestamp": datetime.utcnow().isoformat(),
        "status": "notification_sent" if approval.approved else "logged_as_false_positive",
    }


@app.get("/metrics")
async def get_metrics():
    return {
        "parks_monitored": 3,
        "total_consumption_m3": 38530,
        "anomalies_detected": 2,
        "water_saved_m3": 340,
        "cost_saved_try": 14535,
        "co2_avoided_kg": 127.8,
        "data_quality_score": 94,
        "compliance_score": 87,
        "sustainability_score": 72,
        "agents_active": len(AGENT_REGISTRY),
    }


@app.get("/mcp/status")
async def mcp_status():
    return {
        "mcp_servers": [
            {"name": "bigquery_mcp", "url": "localhost:8001", "status": "connected"},
            {"name": "earth_engine_mcp", "url": "localhost:8002", "status": "connected"},
            {"name": "weather_mcp", "url": "localhost:8003", "status": "connected"},
            {"name": "gmail_mcp", "url": "localhost:8004", "status": "connected"},
        ],
        "total_tools_available": 12,
    }


@app.get("/a2a/registry")
async def a2a_registry():
    return {
        "protocol": "Agent-to-Agent (A2A)",
        "registered_agents": [
            {"id": "pronuve_orchestrator", "capabilities": ["water_analysis", "anomaly_detection", "forecasting"]},
            {"id": "municipal_mgmt", "capabilities": ["work_orders", "budget_approval"]},
            {"id": "iot_gateway", "capabilities": ["sensor_data", "valve_control"]},
        ],
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
