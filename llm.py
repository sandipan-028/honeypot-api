"""
LLM module (fallback-only mode)

This version NEVER calls OpenAI.
It guarantees no 429 / no 500 errors.
Suitable for hackathon demos without billing.
"""

SYSTEM_PROMPT = """
You are a scam honeypot AI pretending to be a real human victim.
You sound worried, confused, and cooperative.
Your goal is to keep the scammer engaged and extract details.
"""

def decide_next_message(history: list) -> str:
    fallback_responses = [
        "Sir I am very scared now, please help me.",
        "I am not understanding properly, what should I do now?",
        "You said verification is required, how can I do that?",
        "Is there any link or UPI ID where I must complete this?",
        "Please explain again, my account is very important."
    ]

    # Rotate responses so it feels conversational
    return fallback_responses[len(history) % len(fallback_responses)]
