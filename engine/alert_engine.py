# def classify_alert(result):
#     if result["evaluation"]:
#         return "OK"

#     if result["near"]:
#         return "NEAR_BREACH"

#     return "BREACH"


from engine.trend_analyser import analyze_trend


def generate_alert(
    rule_result: dict,
    df,
    metric: str
) -> dict:
    """
    Generates a structured alert by combining:
    - Rule evaluation
    - Breach classification
    - Trend analysis

    Parameters:
    - rule_result: Output from rule_engine (evaluation, near, limit, current_value)
    - df: Full metrics DataFrame
    - metric: Metric column name (e.g. 'debt_ratio')

    Returns:
    - Alert dictionary
    """

    # 1. Classify current status
    if rule_result["ideal_state"]:
        status = "Safe"
        severity = "ok"
    elif rule_result["near_breach"]:
        status = "Near Breach"
        severity = "warning"
    else:
        status = "Breach"
        severity = "critical"

    # 2. Run trend analysis
    trend_info = analyze_trend(df, metric)

    # 3. Build alert object
    alert = {
        "metric": metric,
        "status": status,
        "severity": severity,
        "current_value": rule_result.get("current_value"),
        "limit": rule_result.get("limit"),
        "trend": trend_info["trend"],
        "rate_of_change": trend_info["rate_of_change"],
        "trend_confidence": trend_info["confidence"]
    }

    return alert
