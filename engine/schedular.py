import schedule
import time
from engine.data_loader import load_metrics
from engine.rule_engine import load_rules, evaluate_rule
from engine.alert_engine import classify_alert
from engine.llm_explainer import generate_explanation

def run_all_checks():
    df = load_metrics()
    rules = load_rules()

    alerts = []

    for rule in rules:
        result = evaluate_rule(rule, df)
        status = classify_alert(result)
        if status != "OK":
            explanation = generate_explanation(result)
            alerts.append({"status": status, "result": result, "explanation": explanation})

    print("Alerts:", alerts)
    return alerts

def start_scheduler():
    schedule.every().day.at("09:00").do(run_all_checks)
    while True:
        schedule.run_pending()
        time.sleep(1)
