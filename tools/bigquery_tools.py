"""BigQuery tools for water data access."""

from google.adk.tools import FunctionTool
from typing import Optional
import json
import os


def query_consumption_data(
    park_id: Optional[str] = None,
    start_period: Optional[str] = None,
    end_period: Optional[str] = None,
    tool_context=None,
) -> str:
    """Query water consumption data from BigQuery.

    Args:
        park_id: Specific park ID to filter (None = all parks)
        start_period: Start period in YYYYMM format (e.g. "202401")
        end_period: End period in YYYYMM format (e.g. "202412")

    Returns:
        JSON string with consumption records
    """
    from google.cloud import bigquery

    project = os.getenv("GOOGLE_CLOUD_PROJECT")
    dataset = os.getenv("BIGQUERY_DATASET", "pronuve_water")

    client = bigquery.Client(project=project)

    query = f"SELECT * FROM `{project}.{dataset}.consumption`"
    conditions = []

    if park_id:
        conditions.append(f"park_id = '{park_id}'")
    if start_period:
        conditions.append(f"period >= '{start_period}'")
    if end_period:
        conditions.append(f"period <= '{end_period}'")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY park_id, period"

    results = client.query(query).result()
    records = [dict(row) for row in results]

    if tool_context:
        tool_context.state["park_data"] = records

    return json.dumps(records, default=str)


def query_sensor_data(
    park_id: Optional[str] = None,
    hours: int = 24,
    tool_context=None,
) -> str:
    """Query IoT sensor readings from BigQuery.

    Args:
        park_id: Specific park ID to filter
        hours: Number of hours to look back (default 24)

    Returns:
        JSON string with sensor readings
    """
    from google.cloud import bigquery

    project = os.getenv("GOOGLE_CLOUD_PROJECT")
    dataset = os.getenv("BIGQUERY_DATASET", "pronuve_water")

    client = bigquery.Client(project=project)

    query = f"""
    SELECT * FROM `{project}.{dataset}.sensors`
    WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL {hours} HOUR)
    """

    if park_id:
        query += f" AND park_id = '{park_id}'"

    query += " ORDER BY timestamp DESC"

    results = client.query(query).result()
    records = [dict(row) for row in results]

    if tool_context:
        tool_context.state["sensor_data"] = records

    return json.dumps(records, default=str)


query_consumption_data = FunctionTool(query_consumption_data)
query_sensor_data = FunctionTool(query_sensor_data)
