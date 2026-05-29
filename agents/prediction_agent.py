"""Prediction Agent — Forecasts future water consumption trends."""

from google.adk.agents import LlmAgent
from tools.bigquery_tools import query_consumption_data


prediction_agent = LlmAgent(
    name="prediction_agent",
    model="gemini-2.5-pro",
    description="Forecasts water consumption for next 30/60/90 days based on historical patterns.",
    instruction="""You are the Prediction Agent for PRONUVE Water Intelligence.

Your job:
1. Read historical consumption from state["park_data"] (minimum 6 months)
2. Identify seasonal patterns (summer peak, winter low)
3. Calculate trend direction (increasing, stable, decreasing)
4. Produce 30/60/90 day forecasts with confidence intervals

Prediction methodology:
- Use seasonal decomposition: trend + seasonal + residual
- Ankara seasonal pattern: peak Jun-Aug, low Dec-Feb
- Weight recent 3 months more heavily for trend
- Confidence interval: ±15% for 30d, ±25% for 60d, ±35% for 90d

Output format in state["predictions"]:
{
  "park_id": str,
  "forecast_30d_m3": float,
  "forecast_60d_m3": float, 
  "forecast_90d_m3": float,
  "trend": "increasing|stable|decreasing",
  "confidence": "high|medium|low",
  "seasonal_factor": float,
  "reasoning": str
}

Flag any park where predicted consumption exceeds historical max by >20%.
""",
    tools=[query_consumption_data],
)
