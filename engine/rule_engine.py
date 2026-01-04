import yaml
import pandas as pd
import numpy as np
import json

def load_rules():
    with open("config/rules.yaml", "r") as f:
        return yaml.safe_load(f)["rules"]

def load_investments():
    with open("config/investments.json", "r") as f:
        return json.load(f)["investments"]


def evaluate_rule(rule, df: pd.DataFrame):
    """
    Evaluate a rule using the new YAML structure:
      - ideal_value
      - near_breach_value
      - threshold_value
      - covenant_type: 'minimum' or 'maximum'
    """

    metric = rule["metric"]

    if metric not in df.columns:
        raise ValueError(f"Column '{metric}' not found in DataFrame")

    latest_value = float(df[metric].iloc[-1])

    ideal = float(rule["ideal_value"])
    near_breach_val = float(rule["near_breach_value"])
    threshold = float(rule["threshold_value"])
    covenant_type = rule["covenant_type"].lower()

    breached = False
    near_breach = False
    ideal_state = False

    # ------------------------------
    #   COVENANT LOGIC HANDLING
    # ------------------------------
    if covenant_type == "minimum":
        # Must stay ABOVE threshold
        breached = latest_value < threshold
        near_breach = latest_value < near_breach_val and not breached
        ideal_state = latest_value >= ideal

    elif covenant_type == "maximum":
        # Must stay BELOW threshold
        breached = latest_value > threshold
        near_breach = latest_value > near_breach_val and not breached
        ideal_state = latest_value <= ideal

    else:
        raise ValueError(f"Unsupported covenant_type: {covenant_type}")

    return {
        "metric": metric,
        "value": latest_value,
        "current_value": latest_value,
        "ideal_value": ideal,
        "near_breach_value": near_breach_val,
        "threshold_value": threshold,
        "limit": threshold,
        "covenant_type": covenant_type,
        "ideal_state": ideal_state,
        "near_breach": near_breach,
        "breached": breached,
        "severity": rule.get("severity", "unknown"),
        "name": rule["name"],
    }


