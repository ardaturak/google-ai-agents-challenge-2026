"""PRONUVE Water Intelligence — MCP Server for Agent-to-Agent communication.

Implements Model Context Protocol for external integrations:
- BigQuery data source
- Google Earth Engine NDVI
- Weather API
- Gmail notifications
"""

from google.adk.tools import MCPTool


bigquery_mcp = MCPTool(
    name="bigquery_mcp",
    description="MCP connection to BigQuery for water consumption and IoT sensor data",
    server_url="http://localhost:8001/mcp",
    capabilities=["query_consumption", "query_sensors", "query_historical"],
)

earth_engine_mcp = MCPTool(
    name="earth_engine_mcp",
    description="MCP connection to Google Earth Engine for NDVI satellite imagery",
    server_url="http://localhost:8002/mcp",
    capabilities=["get_ndvi", "get_ndvi_timeseries", "get_land_cover"],
)

weather_mcp = MCPTool(
    name="weather_mcp",
    description="MCP connection to weather data provider for forecasts and ET₀",
    server_url="http://localhost:8003/mcp",
    capabilities=["get_forecast", "get_historical_weather", "calculate_eto"],
)

gmail_mcp = MCPTool(
    name="gmail_mcp",
    description="MCP connection to Gmail API for sending alert notifications",
    server_url="http://localhost:8004/mcp",
    capabilities=["send_email", "draft_email", "check_inbox"],
)
