"""Data Ingestion Agent — Collects water consumption and sensor data."""

from google.adk.agents import LlmAgent
from tools.bigquery_tools import query_consumption_data, query_sensor_data


data_ingest_agent = LlmAgent(
    name="data_ingest_agent",
    model="gemini-2.5-flash",
    description="Collects and validates water consumption and IoT sensor data from BigQuery.",
    instruction="""You are the Data Ingestion Agent for PRONUVE Water Intelligence.

Your job:
1. Query water consumption data from BigQuery for specified parks and time periods
2. Query IoT sensor readings (soil moisture, rain intensity, temperature)
3. Validate data completeness and flag missing records
4. Store validated data in shared state for downstream agents

When querying data:
- Default to last 12 months if no period specified
- Flag any gaps > 30 days as data quality issues
- Calculate basic statistics (count, min, max, mean) for validation
- Store results in state["park_data"] and state["sensor_data"]
""",
    tools=[query_consumption_data, query_sensor_data],
)
