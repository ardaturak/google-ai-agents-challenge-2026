"""Google Earth Engine tools for NDVI satellite analysis."""

from google.adk.tools import FunctionTool
from typing import Optional
import json


def get_ndvi_for_park(
    park_id: str,
    latitude: float,
    longitude: float,
    buffer_meters: int = 500,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> str:
    """Get NDVI vegetation index for a park area from Google Earth Engine.

    Args:
        park_id: Park identifier
        latitude: Center latitude of park
        longitude: Center longitude of park
        buffer_meters: Buffer radius around center point (default 500m)
        start_date: Start date (YYYY-MM-DD), default last 30 days
        end_date: End date (YYYY-MM-DD), default today

    Returns:
        JSON string with NDVI statistics
    """
    import ee
    from datetime import datetime, timedelta

    if not start_date:
        end_dt = datetime.now()
        start_dt = end_dt - timedelta(days=30)
        start_date = start_dt.strftime("%Y-%m-%d")
        end_date = end_dt.strftime("%Y-%m-%d")

    try:
        ee.Initialize()
    except Exception:
        ee.Authenticate()
        ee.Initialize()

    point = ee.Geometry.Point([longitude, latitude])
    aoi = point.buffer(buffer_meters)

    collection = (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterBounds(aoi)
        .filterDate(start_date, end_date)
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 40))
    )

    def calc_ndvi(image):
        ndvi = image.normalizedDifference(["B8", "B4"]).rename("NDVI")
        return image.addBands(ndvi)

    with_ndvi = collection.map(calc_ndvi)
    ndvi_stats = with_ndvi.select("NDVI").mean().reduceRegion(
        reducer=ee.Reducer.mean().combine(ee.Reducer.minMax(), sharedInputs=True),
        geometry=aoi,
        scale=10,
    ).getInfo()

    ndvi_mean = ndvi_stats.get("NDVI_mean", 0)

    if ndvi_mean > 0.5:
        health = "healthy"
    elif ndvi_mean > 0.35:
        health = "moderate"
    elif ndvi_mean > 0.2:
        health = "stressed"
    else:
        health = "critical"

    result = {
        "park_id": park_id,
        "period": f"{start_date} to {end_date}",
        "ndvi_mean": round(ndvi_mean, 3) if ndvi_mean else None,
        "ndvi_min": round(ndvi_stats.get("NDVI_min", 0), 3),
        "ndvi_max": round(ndvi_stats.get("NDVI_max", 0), 3),
        "health_status": health,
        "images_used": with_ndvi.size().getInfo(),
    }

    return json.dumps(result)


get_ndvi_for_park = FunctionTool(get_ndvi_for_park)
