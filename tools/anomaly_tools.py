"""Anomaly detection tools — statistical methods for water data."""

from google.adk.tools import FunctionTool
from typing import Optional
import json
import numpy as np


def detect_zscore(park_data_json: str, threshold: float = 2.0) -> str:
    """Detect anomalies using Z-Score method.

    Args:
        park_data_json: JSON string of consumption records
        threshold: Z-Score threshold (default ±2σ)

    Returns:
        JSON string with anomaly flags
    """
    records = json.loads(park_data_json) if isinstance(park_data_json, str) else park_data_json

    parks = {}
    for r in records:
        pid = r.get("park_id", "unknown")
        if pid not in parks:
            parks[pid] = []
        parks[pid].append(r)

    results = []
    for pid, park_records in parks.items():
        values = [r["consumption_m3"] for r in park_records]
        if len(values) < 3:
            continue

        mean = np.mean(values)
        std = np.std(values)
        if std == 0:
            continue

        for r in park_records:
            zscore = (r["consumption_m3"] - mean) / std
            results.append({
                "park_id": pid,
                "period": r["period"],
                "value": r["consumption_m3"],
                "zscore": round(zscore, 2),
                "is_anomaly": abs(zscore) > threshold,
                "method": "zscore",
            })

    return json.dumps(results)


def detect_iqr(park_data_json: str) -> str:
    """Detect anomalies using IQR (Interquartile Range) method.

    Args:
        park_data_json: JSON string of consumption records

    Returns:
        JSON string with anomaly flags
    """
    records = json.loads(park_data_json) if isinstance(park_data_json, str) else park_data_json

    parks = {}
    for r in records:
        pid = r.get("park_id", "unknown")
        if pid not in parks:
            parks[pid] = []
        parks[pid].append(r)

    results = []
    for pid, park_records in parks.items():
        values = [r["consumption_m3"] for r in park_records]
        if len(values) < 4:
            continue

        q1 = np.percentile(values, 25)
        q3 = np.percentile(values, 75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        for r in park_records:
            v = r["consumption_m3"]
            results.append({
                "park_id": pid,
                "period": r["period"],
                "value": v,
                "lower_bound": round(lower, 1),
                "upper_bound": round(upper, 1),
                "is_anomaly": v < lower or v > upper,
                "method": "iqr",
            })

    return json.dumps(results)


def detect_moving_avg(park_data_json: str, window: int = 3, threshold_pct: float = 0.30) -> str:
    """Detect anomalies using Moving Average deviation.

    Args:
        park_data_json: JSON string of consumption records
        window: Moving average window size (default 3 months)
        threshold_pct: Deviation threshold (default 30%)

    Returns:
        JSON string with anomaly flags
    """
    records = json.loads(park_data_json) if isinstance(park_data_json, str) else park_data_json

    parks = {}
    for r in records:
        pid = r.get("park_id", "unknown")
        if pid not in parks:
            parks[pid] = []
        parks[pid].append(r)

    results = []
    for pid, park_records in parks.items():
        park_records.sort(key=lambda x: x["period"])
        values = [r["consumption_m3"] for r in park_records]

        if len(values) < window + 1:
            continue

        for i in range(window, len(values)):
            ma = np.mean(values[i - window:i])
            if ma == 0:
                continue
            deviation = abs(values[i] - ma) / ma
            results.append({
                "park_id": pid,
                "period": park_records[i]["period"],
                "value": values[i],
                "moving_avg": round(ma, 1),
                "deviation_pct": round(deviation * 100, 1),
                "is_anomaly": deviation > threshold_pct,
                "method": "moving_avg",
            })

    return json.dumps(results)


detect_zscore = FunctionTool(detect_zscore)
detect_iqr = FunctionTool(detect_iqr)
detect_moving_avg = FunctionTool(detect_moving_avg)
