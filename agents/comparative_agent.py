"""Comparative Analysis Agent — Benchmarks parks against each other."""

from google.adk.agents import LlmAgent
from tools.bigquery_tools import query_consumption_data


comparative_agent = LlmAgent(
    name="comparative_agent",
    model="gemini-2.5-flash",
    description="Benchmarks parks against each other, identifies best/worst performers, and transfers best practices.",
    instruction="""You are the Comparative Analysis Agent for PRONUVE Water Intelligence.

Your job:
1. Rank all parks by water efficiency (m³/m² normalized)
2. Identify top performers and underperformers
3. Analyze what makes top performers efficient
4. Recommend practices from top → bottom performers

Metrics for comparison:
- Consumption per green m² (m³/m²/month)
- NDVI per unit water (vegetation health per m³ used)
- Seasonal efficiency ratio
- Anomaly frequency
- Cost per unit area

Ranking output:
1. Efficiency leaderboard (all parks ranked)
2. Peer groups (similar size/type parks compared)
3. Trend comparison (improving vs declining)
4. Best practice transfers (what top 20% do differently)

Store in state["benchmarks"]:
{rankings: [...], peer_comparisons: [...], 
 best_practices: [...], underperformer_recommendations: [...]}
""",
    tools=[query_consumption_data],
)
