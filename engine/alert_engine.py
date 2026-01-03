def classify_alert(result):
    if result["evaluation"]:
        return "OK"

    if result["near"]:
        return "NEAR_BREACH"

    return "BREACH"
