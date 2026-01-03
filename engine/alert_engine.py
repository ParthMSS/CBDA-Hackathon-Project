import numpy as np
def classify_alert(result):
    if result["breached"] == np.True_:
        return "BREACH"

    if result["near_breach"] == np.True_:
        return "NEAR_BREACH"

    return "OK"
