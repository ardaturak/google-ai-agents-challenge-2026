"""Weather Tools — Fetch forecast and calculate ET₀."""

from google.adk.tools import FunctionTool


def get_weather_forecast(city: str = "Ankara", days: int = 7) -> dict:
    """Fetches weather forecast for the specified city and number of days.
    
    Args:
        city: Target city for weather data
        days: Number of forecast days (1-7)
    
    Returns:
        Weather forecast including temperature, humidity, wind, and rain probability.
    """
    forecast = []
    import random
    random.seed(42)

    for day in range(days):
        forecast.append({
            "day": day + 1,
            "temp_max_c": round(28 + random.uniform(-5, 7), 1),
            "temp_min_c": round(14 + random.uniform(-3, 4), 1),
            "humidity_pct": round(35 + random.uniform(-10, 25), 1),
            "wind_kmh": round(8 + random.uniform(-3, 12), 1),
            "rain_probability_pct": round(random.uniform(0, 40), 1),
            "rain_mm": round(random.uniform(0, 3), 1) if random.random() > 0.6 else 0,
            "solar_radiation_mj": round(18 + random.uniform(-4, 6), 1),
        })

    return {
        "city": city,
        "days": days,
        "forecast": forecast,
        "source": "OpenMeteo API (demo data)",
    }


def calculate_eto(
    temp_max: float,
    temp_min: float,
    humidity: float,
    wind_speed: float,
    solar_radiation: float,
) -> dict:
    """Calculates reference evapotranspiration using simplified Penman-Monteith.
    
    Args:
        temp_max: Maximum daily temperature (°C)
        temp_min: Minimum daily temperature (°C)
        humidity: Relative humidity (%)
        wind_speed: Wind speed at 2m height (km/h)
        solar_radiation: Solar radiation (MJ/m²/day)
    
    Returns:
        ET₀ value in mm/day and irrigation recommendation.
    """
    temp_mean = (temp_max + temp_min) / 2
    wind_ms = wind_speed / 3.6

    delta = 4098 * (0.6108 * 2.7183 ** (17.27 * temp_mean / (temp_mean + 237.3))) / (temp_mean + 237.3) ** 2
    gamma = 0.065
    es = 0.6108 * 2.7183 ** (17.27 * temp_mean / (temp_mean + 237.3))
    ea = es * humidity / 100

    rn = solar_radiation * 0.77 - 2.0

    numerator = 0.408 * delta * rn + gamma * (900 / (temp_mean + 273)) * wind_ms * (es - ea)
    denominator = delta + gamma * (1 + 0.34 * wind_ms)

    eto = max(0, numerator / denominator)

    return {
        "eto_mm_day": round(eto, 2),
        "interpretation": "high" if eto > 6 else "moderate" if eto > 3.5 else "low",
        "irrigation_factor": round(eto / 5.0, 2),
    }


get_weather_forecast = FunctionTool(get_weather_forecast)
calculate_eto = FunctionTool(calculate_eto)
