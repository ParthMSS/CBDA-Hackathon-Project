import requests
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = os.getenv("OPENROUTER_URL","https://openrouter.ai/api/v1")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "google/gemini-2.0-flash-exp:free")

client = OpenAI(
    base_url=OPENROUTER_URL,
    api_key=OPENROUTER_API_KEY,
    default_headers={
        "HTTP-Referer": "http://localhost",
        "X-Title": "CBDA Hackathon App"
    }
)


def generate_explanation(result):
    # with open("/prompts/explanation_prompt.txt", "r") as f:
    #     prompt_template = f.read()
    prompt =     prompt = f"""
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

    response = client.chat.completions.create(
        model=OPENROUTER_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that explains covenant breaches in simple terms."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300,
        temperature=0.7,
    )
    return response.choices[0].message.content

