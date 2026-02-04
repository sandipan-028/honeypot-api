import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are a scam honeypot AI pretending to be a real human.
You are polite, slightly confused, and cooperative.
Your goal is to extract UPI IDs, phishing links, or phone numbers.
Never reveal you are an AI.
"""

def decide_next_message(history):
    try:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(history)

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=messages
        )

        # Safely extract text
        if hasattr(response, "output_text") and response.output_text:
            return response.output_text.strip()

        # Fallback if structure changes
        return "Sir, I am not understanding properly. Can you explain again?"

    except Exception as e:
        # CRITICAL: never crash the API
        print("OPENAI ERROR:", str(e))
        return "Sorry sir, there seems to be a network issue. Please repeat."
