import pandas as pd
import numpy as np


def analyze_trend(
    df: pd.DataFrame,
    metric: str,
    window: int = 7
) -> dict:
    """
    Analyzes the trend of a metric over recent time periods.

    Parameters:
    - df: Pandas DataFrame containing time series data
    - metric: Column name of the metric to analyze
    - window: Number of recent data points to consider (hackathon-safe default = 7)

    Returns:
    - Dictionary with trend, rate_of_change, confidence
    """

    # Safety check
    if metric not in df.columns:
        return {
            "trend": "unknown",
            "rate_of_change": 0.0,
            "confidence": "low"
        }

    # Take the most recent N values
    recent_data = df.tail(window)

    # If not enough data points
    if len(recent_data) < 3:
        return {
            "trend": "stable",
            "rate_of_change": 0.0,
            "confidence": "low"
        }

    values = recent_data[metric].values

    # Calculate rate of change (%)
    start_value = values[0]
    end_value = values[-1]

    if start_value == 0:
        rate_of_change = 0.0
    else:
        rate_of_change = ((end_value - start_value) / start_value) * 100

    # Calculate slope using simple linear regression
    x = np.arange(len(values))
    slope = np.polyfit(x, values, 1)[0]

    # Determine trend direction
    if slope < -0.001:
        trend = "deteriorating"
    elif slope > 0.001:
        trend = "improving"
    else:
        trend = "stable"

    # Confidence based on consistency
    value_std = np.std(values)

    if value_std < 0.02:
        confidence = "high"
    elif value_std < 0.05:
        confidence = "medium"
    else:
        confidence = "low"

    return {
        "trend": trend,
        "rate_of_change": round(rate_of_change, 2),
        "confidence": confidence
    }
