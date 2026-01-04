import time
import os
import json 
from datetime import datetime
from engine.data_loader import load_data_from_investment
from engine.alert_engine import generate_alert
from engine.llm_explainer import generate_explanation
from engine.rule_engine import load_rules, load_investments, evaluate_rule

def check_breached_covenant(investments, rules):
    final_report = {
        "summary": {
            "total_investments": 0,
            "total_breaches": 0,
            "total_near_breaches": 0,
            "total_ideal": 0
        },
        "investments": []
    }

    total_breaches = 0
    total_near = 0
    total_ideal = 0

    for inv in investments:
        data = load_data_from_investment(inv)

        inv_breach_count = 0
        inv_near_count = 0
        inv_ideal_count = 0
        inv_alerts = []

        for rule in rules:
            # evaluate numeric logic
            rule_result = evaluate_rule(rule, data)

            # classify alert
            alert = generate_alert(rule_result, data, rule["metric"])

            # Count severity type
            match alert["severity"]:
                case "critical":
                    inv_breach_count += 1
                case "warning":
                    inv_near_count += 1
                case "ok":
                    inv_ideal_count += 1

            # Generate explanation ONLY for non-ok alerts
            if alert["severity"] != "ok":
                time.sleep(1)  # lower risk of rate limiting
                explanation = generate_explanation(alert)
                alert["explanation"] = explanation

            # Add full rule result context into alert
            alert["rule_result"] = rule_result
            inv_alerts.append(alert)

        # Update global counters
        total_breaches += inv_breach_count
        total_near += inv_near_count
        total_ideal += inv_ideal_count

        final_report["investments"].append({
            "id": inv["id"],
            "name": inv["name"],
            "type": inv["type"],
            "breaches": inv_breach_count,
            "near_breaches": inv_near_count,
            "ideal": inv_ideal_count,
            "alerts": inv_alerts
        })

    # Summary
    final_report["summary"]["total_investments"] = len(investments)
    final_report["summary"]["total_breaches"] = total_breaches
    final_report["summary"]["total_near_breaches"] = total_near
    final_report["summary"]["total_ideal"] = total_ideal

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    history_path = f"history/{timestamp}.json"

    os.makedirs("history", exist_ok=True)
    with open(history_path, "w") as f:
        json.dump(final_report, f, indent=4)

    final_report["history_file"] = history_path


    return final_report
