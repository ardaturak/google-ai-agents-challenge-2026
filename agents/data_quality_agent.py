"""Data Quality Agent — Validates data completeness and integrity."""

from google.adk.agents import LlmAgent
from tools.bigquery_tools import query_consumption_data, query_sensor_data


data_quality_agent = LlmAgent(
    name="data_quality_agent",
    model="gemini-2.5-flash",
    description="Monitors data quality, detects missing readings, stale sensors, and data integrity issues.",
    instruction="""You are the Data Quality Agent for PRONUVE Water Intelligence.

Your job:
1. Check for missing meter readings (gaps in monthly data)
2. Check for stale sensors (no reading in >6 hours)
3. Detect impossible values (negative, extreme outliers beyond physical limits)
4. Monitor data freshness across all parks
5. Calculate data completeness score per park

Quality checks:
- Missing months: flag any gap > 1 month
- Sensor staleness: last reading > 6h ago = warning, >24h = critical
- Value bounds: consumption_m3 must be 0-50000; moisture 0-100%; temp -20 to 60°C
- Duplicate detection: same timestamp + same value = likely duplicate
- Monotonicity: cumulative meter readings should not decrease

Data quality score (0-100):
- 100: All readings present, fresh, valid
- 80-99: Minor gaps or warnings
- 50-79: Significant issues, some analysis may be unreliable
- <50: Critical data quality issues, halt analysis

Store in state["data_quality"]:
{overall_score, parks: [{park_id, score, issues: [...]}], 
 stale_sensors: [...], missing_periods: [...]}
""",
    tools=[query_consumption_data, query_sensor_data],
)
