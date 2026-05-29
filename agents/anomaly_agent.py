"""Anomaly Detection Agent — Multi-method parallel anomaly detection.

Uses 5 statistical/ML methods in parallel:
- Z-Score (parametric)
- IQR Interquartile Range (non-parametric)
- Moving Average deviation (trend-based)
- Isolation Forest (ML-based)
- CUSUM Cumulative Sum (shift detection)

Consensus scoring: anomaly confirmed when ≥2/5 methods agree.
"""

from google.adk.agents import LlmAgent, ParallelAgent
from tools.anomaly_tools import detect_zscore, detect_iqr, detect_moving_avg
from tools.advanced_anomaly_tools import detect_isolation_forest, detect_cusum, calculate_consensus


zscore_agent = LlmAgent(
    name="zscore_detector",
    model="gemini-2.5-flash",
    description="Detects anomalies using Z-Score method (threshold: ±2σ).",
    instruction="""You detect anomalies in water consumption using Z-Score.
Read data from state["park_data"]. For each park:
1. Calculate mean and standard deviation of monthly consumption
2. Flag months where |value - mean| > 2 * std as anomalies
3. Store results in state["zscore_anomalies"]
""",
    tools=[detect_zscore],
)

iqr_agent = LlmAgent(
    name="iqr_detector",
    model="gemini-2.5-flash",
    description="Detects anomalies using IQR (Interquartile Range) method.",
    instruction="""You detect anomalies in water consumption using IQR method.
Read data from state["park_data"]. For each park:
1. Calculate Q1 (25th) and Q3 (75th percentile), IQR = Q3 - Q1
2. Bounds: [Q1 - 1.5*IQR, Q3 + 1.5*IQR]
3. Flag values outside bounds
4. Store results in state["iqr_anomalies"]
""",
    tools=[detect_iqr],
)

moving_avg_agent = LlmAgent(
    name="moving_avg_detector",
    model="gemini-2.5-flash",
    description="Detects anomalies using Moving Average deviation (>30% from 3-month MA).",
    instruction="""You detect anomalies using Moving Average deviation.
Read data from state["park_data"]. For each park:
1. Calculate 3-month moving average
2. Flag months where actual deviates > 30% from MA
3. Store results in state["ma_anomalies"]
""",
    tools=[detect_moving_avg],
)

isolation_forest_agent = LlmAgent(
    name="isolation_forest_detector",
    model="gemini-2.5-flash",
    description="Detects anomalies using Isolation Forest ML algorithm.",
    instruction="""You detect anomalies using Isolation Forest.
This ML method isolates anomalies by random recursive partitioning.
Points requiring fewer splits to isolate are more anomalous.
Read data from state["park_data"], run isolation forest, store in state["if_anomalies"]
""",
    tools=[detect_isolation_forest],
)

cusum_agent = LlmAgent(
    name="cusum_detector",
    model="gemini-2.5-flash",
    description="Detects mean shifts using CUSUM (Cumulative Sum) control chart.",
    instruction="""You detect shifts in consumption patterns using CUSUM.
CUSUM is effective for detecting gradual changes like slow leaks or
systematic over-irrigation. It accumulates deviations from the mean.
Read data from state["park_data"], run CUSUM, store in state["cusum_anomalies"]
""",
    tools=[detect_cusum],
)

parallel_detection = ParallelAgent(
    name="parallel_anomaly_detection",
    description="Runs 5 anomaly detection methods in parallel for speed and robust consensus",
    sub_agents=[zscore_agent, iqr_agent, moving_avg_agent, isolation_forest_agent, cusum_agent],
)

anomaly_detection_agent = LlmAgent(
    name="anomaly_consensus",
    model="gemini-2.5-pro",
    description="Combines results from 5 parallel detection methods into consensus score.",
    instruction="""You are the Anomaly Consensus Agent.
After parallel detection completes, combine all results:

1. Read: state["zscore_anomalies"], state["iqr_anomalies"], state["ma_anomalies"],
   state["if_anomalies"], state["cusum_anomalies"]
2. For each data point, count how many of the 5 methods flagged it
3. Consensus scoring:
   - 0/5: normal
   - 1/5: low concern (monitor)
   - 2/5: medium — likely anomaly
   - 3/5: high — confirmed anomaly, investigate
   - 4-5/5: critical — immediate action required
4. Store final results in state["anomalies"]
5. Provide summary: total anomalies, most affected parks, severity breakdown
6. Recommend specific actions for critical/high severity findings

Special attention:
- CUSUM shift detection = possible leak → recommend physical inspection
- Isolation Forest outlier = unusual pattern → check for meter malfunction
- Multiple methods agree on same period = high confidence finding
""",
    tools=[calculate_consensus],
    sub_agents=[parallel_detection],
)
