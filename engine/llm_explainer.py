import requests
import os

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

def generate_explanation(result):
    prompt = f"""
Explain this rule violation:

Rule ID: {result['rule_id']}
Metric: {result['metric']}
Current Value: {result['value']}
Limit: {result['limit']}
Condition: {result['condition']}
Trend: {result['trend']}

Explain in simple English:
1. What happened?
2. Why it matters?
3. Risk level?
4. Recommend next steps.
"""

    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}"}
    payload = {
        "model": "mistral/mistral-tiny",   # free model
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(OPENROUTER_URL, json=payload, headers=headers)
    return response.json()["choices"][0]["message"]["content"]
