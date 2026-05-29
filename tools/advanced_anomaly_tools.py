"""Advanced anomaly detection — Isolation Forest and CUSUM methods."""

from google.adk.tools import FunctionTool
import json
import numpy as np


def detect_isolation_forest(park_data_json: str, contamination: float = 0.1) -> str:
    """Detect anomalies using Isolation Forest algorithm.

    Isolation Forest isolates anomalies by randomly selecting features
    and split values. Anomalies require fewer splits to isolate.

    Args:
        park_data_json: JSON string of consumption records
        contamination: Expected proportion of anomalies (default 10%)

    Returns:
        JSON string with anomaly scores and flags
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
        values = np.array([r["consumption_m3"] for r in park_records]).reshape(-1, 1)
        if len(values) < 6:
            continue

        n_samples = len(values)
        n_trees = 100
        scores = np.zeros(n_samples)

        for _ in range(n_trees):
            sample_idx = np.random.choice(n_samples, size=min(256, n_samples), replace=False)
            sample = values[sample_idx].flatten()
            split_val = np.random.uniform(sample.min(), sample.max())

            for i in range(n_samples):
                depth = 0
                low, high = values.min(), values.max()
                val = values[i, 0]
                while depth < 10:
                    split = np.random.uniform(low, high)
                    if val < split:
                        high = split
                    else:
                        low = split
                    depth += 1
                scores[i] += depth

        scores = scores / n_trees
        avg_depth = np.mean(scores)
        threshold = avg_depth * (1 - contamination * 2)

        for i, r in enumerate(park_records):
            is_anomaly = scores[i] < threshold
            results.append({
                "park_id": pid,
                "period": r["period"],
                "value": r["consumption_m3"],
                "isolation_score": round(float(scores[i]), 3),
                "avg_depth": round(float(avg_depth), 3),
                "is_anomaly": bool(is_anomaly),
                "method": "isolation_forest",
            })

    return json.dumps(results)


def detect_cusum(park_data_json: str, drift: float = 0.5, threshold_h: float = 4.0) -> str:
    """Detect anomalies using CUSUM (Cumulative Sum) control chart.

    CUSUM detects shifts in the mean level of a process.
    Effective for detecting gradual changes (e.g., slow leaks).

    Args:
        park_data_json: JSON string of consumption records
        drift: Allowable drift parameter (k, default 0.5 std)
        threshold_h: Decision threshold (h, default 4.0 std)

    Returns:
        JSON string with CUSUM scores and shift detection
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
        values = np.array([r["consumption_m3"] for r in park_records], dtype=float)

        if len(values) < 4:
            continue

        mean = np.mean(values)
        std = np.std(values)
        if std == 0:
            continue

        normalized = (values - mean) / std

        s_pos = np.zeros(len(normalized))
        s_neg = np.zeros(len(normalized))

        for i in range(1, len(normalized)):
            s_pos[i] = max(0, s_pos[i - 1] + normalized[i] - drift)
            s_neg[i] = max(0, s_neg[i - 1] - normalized[i] - drift)

        for i, r in enumerate(park_records):
            is_anomaly = s_pos[i] > threshold_h or s_neg[i] > threshold_h
            shift_direction = None
            if s_pos[i] > threshold_h:
                shift_direction = "upward"
            elif s_neg[i] > threshold_h:
                shift_direction = "downward"

            results.append({
                "park_id": pid,
                "period": r["period"],
                "value": r["consumption_m3"],
                "cusum_pos": round(float(s_pos[i]), 2),
                "cusum_neg": round(float(s_neg[i]), 2),
                "is_anomaly": bool(is_anomaly),
                "shift_direction": shift_direction,
                "method": "cusum",
            })

    return json.dumps(results)


def calculate_consensus(
    zscore_json: str,
    iqr_json: str,
    moving_avg_json: str,
    isolation_forest_json: str,
    cusum_json: str,
) -> str:
    """Calculate consensus anomaly score from all 5 detection methods.

    Args:
        zscore_json: Results from Z-Score method
        iqr_json: Results from IQR method
        moving_avg_json: Results from Moving Average method
        isolation_forest_json: Results from Isolation Forest
        cusum_json: Results from CUSUM

    Returns:
        JSON with consensus scoring (0-5 methods agreement)
    """
    methods = {
        "zscore": json.loads(zscore_json),
        "iqr": json.loads(iqr_json),
        "moving_avg": json.loads(moving_avg_json),
        "isolation_forest": json.loads(isolation_forest_json),
        "cusum": json.loads(cusum_json),
    }

    point_scores = {}

    for method_name, records in methods.items():
        for r in records:
            key = f"{r['park_id']}_{r['period']}"
            if key not in point_scores:
                point_scores[key] = {
                    "park_id": r["park_id"],
                    "period": r["period"],
                    "value": r["value"],
                    "flags": 0,
                    "methods_flagged": [],
                    "total_methods": 5,
                }
            if r.get("is_anomaly"):
                point_scores[key]["flags"] += 1
                point_scores[key]["methods_flagged"].append(method_name)

    results = []
    for key, data in point_scores.items():
        flags = data["flags"]
        if flags == 0:
            severity = "normal"
        elif flags == 1:
            severity = "low"
        elif flags == 2:
            severity = "medium"
        elif flags == 3:
            severity = "high"
        else:
            severity = "critical"

        results.append({
            "park_id": data["park_id"],
            "period": data["period"],
            "value": data["value"],
            "consensus_score": f"{flags}/5",
            "severity": severity,
            "methods_flagged": data["methods_flagged"],
            "is_anomaly": flags >= 2,
        })

    results.sort(key=lambda x: x["period"])
    anomaly_count = sum(1 for r in results if r["is_anomaly"])

    summary = {
        "total_points_analyzed": len(results),
        "anomalies_detected": anomaly_count,
        "critical_anomalies": sum(1 for r in results if r["severity"] == "critical"),
        "high_anomalies": sum(1 for r in results if r["severity"] == "high"),
        "details": results,
    }

    return json.dumps(summary, indent=2)


detect_isolation_forest = FunctionTool(detect_isolation_forest)
detect_cusum = FunctionTool(detect_cusum)
calculate_consensus = FunctionTool(calculate_consensus)
