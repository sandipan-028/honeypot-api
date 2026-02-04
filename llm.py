import os
from dotenv import load_dotenv

# Try importing OpenAI SDK safely
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except Exception:
    OPENAI_AVAILABLE = False

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = """
You are a scam honeypot AI pretending to be a real human victim.
You must sound slightly confused, worried, and cooperative.
Your goal is to keep the scammer talking and extract:
- UPI IDs
- Bank account numbers
- Phishing links
- Phone numbers

Never reveal you are an AI.
Never accuse the other party.
"""

# Initialize OpenAI client only if possible
client = None
if OPENAI_AVAILABLE and OPENAI_API_KEY:
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
    except Exception:
        client = None


def decide_next_message(history: list) -> str:
    """
    Decide next honeypot message.
    Falls back gracefully if OpenAI fails or quota is exceeded.
    """

    # ---- Attempt LLM call ----
    if client:
        try:
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            messages.extend(history)

            response = client.responses.create(
                model="gpt-4.1-mini",
                input=messages
            )

            if hasattr(response, "output_text") and response.output_text:
                return response.output_text.strip()

        except Exception as e:
            # Log but NEVER crash
            print("OPENAI ERROR (handled safely):", str(e))

    # ---- FALLBACK MODE (NO LLM / NO QUOTA) ----
    fallback_responses = [
        "Sir I am very scared now, please tell me what I should do.",
        "I am not understanding properly, can you explain again?",
        "You said verification is needed, where should I do that?",
        "Is there any UPI ID or link where I must complete this?",
        "Please help me, my account is very important."
    ]

    # Simple rotation to sound natural
    return fallback_responses[len(history) % len(fallback_responses)]
