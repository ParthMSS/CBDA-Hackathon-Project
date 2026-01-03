import yaml
import pandas as pd
import re

def load_rules():
    with open("config/rules.yaml", "r") as f:
        return yaml.safe_load(f)["rules"]

def evaluate_rule(rule, df: pd.DataFrame):
    metric = rule["metric"]
    condition = rule["condition"]

    value = df.iloc[-1][metric]
    past_values = df.tail(7)[metric]

    # Compute moving average if required
    if "moving_average_7d" in condition:
        ma7 = past_values.mean()
        condition = condition.replace("moving_average_7d", str(ma7))

    # Extract threshold from condition (e.g., >= 1.2)
    match = re.findall(r"[0-9]*\.?[0-9]+", condition)
    limit = float(match[-1]) if match else None

    # Evaluate condition safely
    safe_env = {"value": value}
    result = eval(condition, {"__builtins__": {}}, safe_env)

    # Near breach detection
    nb = rule.get("near_breach_threshold", None)
    near = False
    if nb and limit:
        pct = float(nb.strip('%')) / 100
        if abs(value - limit) <= abs(limit * pct):
            near = True

    return {
        "rule_id": rule["id"],
        "metric": metric,
        "value": value,
        "limit": limit,
        "condition": condition,
        "evaluation": result,
        "near": near,
        "trend": "up" if past_values.iloc[-1] > past_values.iloc[0] else "down"
    }
