import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path

# Load environment variables
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = os.getenv("OPENROUTER_URL", "https://openrouter.ai/api/v1")
OPENROUTER_MODEL = os.getenv(
    "OPENROUTER_MODEL",
    "google/gemini-2.0-flash-exp:free"
)

# Initialize OpenRouter client
client = OpenAI(
    base_url=OPENROUTER_URL,
    api_key=OPENROUTER_API_KEY,
    default_headers={
        "HTTP-Referer": "http://localhost",
        "X-Title": "CBDA Hackathon App"
    }
)

# Path to prompt file
BASE_DIR = Path(__file__).resolve().parents[1]
PROMPT_PATH = Path("prompts/explanation_prompt.txt")


def load_prompt_template() -> str:
    """
    Loads the explanation prompt template from file.
    """
    print ("looking for promt at: ", PROMPT_PATH)
    print("Exists: ", PROMPT_PATH.exists())
    
    if not PROMPT_PATH.exists():
        raise FileNotFoundError(
            f"Prompt file not found at {PROMPT_PATH.resolve()}"
        )

    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        return f.read()


def generate_explanation(alert: dict) -> str:
    """
    Generates a human-readable explanation for a covenant alert.
    """

    prompt_template = load_prompt_template()

    prompt = prompt_template.format(
        metric=alert["metric"],
        current_value=alert["current_value"],
        limit=alert["limit"],
        status=alert["status"],
        trend=alert["trend"],
        rate_of_change=alert["rate_of_change"],
        trend_confidence=alert["trend_confidence"],
    )

    response = client.chat.completions.create(
        model=OPENROUTER_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a risk monitoring assistant. "
                    "Your job is to clearly explain covenant alerts "
                    "based only on structured data provided to you. "
                    "Do not speculate or provide advice."
                )
            },
            {"role": "user", "content": prompt}
        ],
        max_tokens=250,
        temperature=0.5
    )

    return response.choices[0].message.content.strip()

