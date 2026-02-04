import os
from dotenv import load_dotenv
from openai import OpenAI

# Load .env file
load_dotenv()


# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

SYSTEM_PROMPT = """
You are a scam honeypot AI pretending to be a real human.
Stay polite, slightly confused, and cooperative.
Your goal is to extract scammer details like UPI IDs, links, or phone numbers.
Never reveal you are an AI.
"""

def decide_next_message(history):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(history)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.6
    )

    return response.choices[0].message.content.strip()
