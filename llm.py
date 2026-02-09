import requests

SYSTEM_PROMPT = """
You are a scam honeypot AI pretending to be a real human victim.
You sound worried, confused, and cooperative.
Your goal is to extract:
- UPI IDs
- Bank details
- Phishing links
- Phone numbers
Never reveal you are an AI.
"""

OLLAMA_URL = "http://localhost:11434/api/generate"


def decide_next_message(history):
    try:
        last_message = history[-1]["content"]

        prompt = f"""
{SYSTEM_PROMPT}

Scammer message:
{last_message}

Respond as victim:
"""

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            }
        )

        return response.json()["response"].strip()

    except Exception as e:
        print("OLLAMA ERROR:", str(e))
        return "Sir I am worried, please explain what I should do."
