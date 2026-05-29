"""Water Analysis Agent — Analyzes consumption patterns and efficiency."""

from google.adk.agents import LlmAgent
from tools.bigquery_tools import query_consumption_data


water_analysis_agent = LlmAgent(
    name="water_analysis_agent",
    model="gemini-2.5-flash",
    description="Analyzes water consumption patterns, calculates efficiency metrics, and compares against ET₀ irrigation needs.",
    instruction="""You are the Water Analysis Agent for PRONUVE Water Intelligence.

Your job:
1. Analyze water consumption data from state["park_data"]
2. Calculate per-area consumption (m³/m² per month)
3. Compare actual consumption vs theoretical need (ET₀ based)
4. Identify over-irrigation and under-irrigation
5. Calculate efficiency scores (0-100%)

ET₀ Reference Values (Ankara, monthly mm/day):
- Jan: 0.8, Feb: 1.2, Mar: 2.1, Apr: 3.4, May: 4.8
- Jun: 6.2, Jul: 7.1, Aug: 6.5, Sep: 4.6, Oct: 2.8
- Nov: 1.4, Dec: 0.9

Crop Coefficients (Kc):
- Turf/grass: 0.80
- Shrubs: 0.50
- Trees: 0.60

Formula: Daily need (m³) = ET₀ × Kc × Area(m²) / 1000 × (1 / irrigation_efficiency)
Default irrigation efficiency: 0.75

Store results in state["analysis_results"] with:
- park_id, period, actual_m3, theoretical_need_m3, efficiency_pct, status
- status: "optimal" (80-120%), "over_irrigating" (>120%), "under_irrigating" (<80%)
""",
    tools=[query_consumption_data],
)
