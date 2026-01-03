import yaml
import pandas as pd
import numpy as np
def load_rules():
    with open("config/rules.yaml", "r") as f:
        return yaml.safe_load(f)["rules"]



def evaluate_rule(rule, df: pd.DataFrame):
    """
    Evaluates a single rule against the provided DataFrame.
    Supports simple comparison operators: >, <, >=, <=, ==, !=
    """
    metric = rule["metric"]
    operator = rule["condition"]["operator"]
    limit = rule["condition"]["threshold"]
    near_breach_threshold_delta = rule["condition"].get("near_breach_threshold_delta", 0)

    if metric not in df.columns:
        raise ValueError(f"Column '{metric}' not found in DataFrame")

    latest_value = df[metric].iloc[-1]
    breached = False
    if operator == ">":
        breached = latest_value > limit
    elif operator == "<":
        breached = latest_value < limit
    elif operator == ">=":
        breached = latest_value >= limit
    elif operator == "<=":
        breached = latest_value <= limit
    else:
        raise ValueError(f"Unsupported operator: {operator}")

    near_breach = False
    new_breach_value = None
    if near_breach_threshold_delta > 0:
        if operator == ">" or operator == ">=":
            near_breach = latest_value >= (limit - near_breach_threshold_delta)
            new_breach_value = limit - near_breach_threshold_delta
        elif operator == "<" or operator == "<=":
            near_breach = latest_value <= (limit + near_breach_threshold_delta)
            new_breach_value = limit + near_breach_threshold_delta

    return {
        "breached": breached,
        "near_breach": near_breach,
        "value": latest_value,
        "new_breach_value": new_breach_value,
        "limit": limit,
        "operator": operator,
    }

