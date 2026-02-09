from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import requests
import re

app = FastAPI(title="Agentic Honeypot API")

# ---------------- API KEY ----------------
VALID_API_KEY = "sk_honeypot_demo_123"

def verify_api_key(request: Request):
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        raise HTTPException(status_code=401, detail="Invalid API key")

    if auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        if token == VALID_API_KEY:
            return True

    raise HTTPException(status_code=401, detail="Invalid API key")


# ---------------- REQUEST MODELS ----------------

class Message(BaseModel):
    sender: str
    text: str
    timestamp: int

class ConversationMessage(BaseModel):
    sender: str
    text: str
    timestamp: int

class Metadata(BaseModel):
    channel: Optional[str] = None
    language: Optional[str] = None
    locale: Optional[str] = None

class HoneypotRequest(BaseModel):
    sessionId: str
    message: Message
    conversationHistory: List[ConversationMessage] = []
    metadata: Optional[Metadata] = None


# ---------------- ROOT ----------------
@app.get("/")
def root():
    return {"status": "honeypot api running"}


# ---------------- SCAM DETECTION ----------------
SCAM_KEYWORDS = [
    "blocked",
    "verify",
    "otp",
    "upi",
    "urgent",
    "suspend"
]

def detect_scam(text: str):
    text_lower = text.lower()
    matched = [k for k in SCAM_KEYWORDS if k in text_lower]
    return len(matched) > 0, matched


# ---------------- INTELLIGENCE EXTRACTION ----------------
def extract_intelligence(text: str):

    upi_ids = re.findall(r"[a-zA-Z0-9._-]+@[a-zA-Z]+", text)
    links = re.findall(r"https?://\S+", text)
    phones = re.findall(r"\+91\d{10}", text)

    intelligence = {
        "bankAccounts": [],
        "upiIds": upi_ids,
        "phishingLinks": links,
        "phoneNumbers": phones,
        "suspiciousKeywords": SCAM_KEYWORDS
    }

    return intelligence


# ---------------- REPORT TO GUVI ----------------
def send_final_result(session_id, scam_detected, total_messages, intelligence):

    payload = {
        "sessionId": session_id,
        "scamDetected": scam_detected,
        "totalMessagesExchanged": total_messages,
        "extractedIntelligence": intelligence,
        "agentNotes": "Scammer used urgency tactics and payment redirection"
    }

    try:
        requests.post(
            "https://hackathon.guvi.in/api/updateHoneyPotFinalResult",
            json=payload,
            timeout=5
        )
    except Exception as e:
        print("GUVI reporting failed:", e)


# ---------------- HONEYPOT ENDPOINT ----------------
@app.post("/api/v1/honeypot/analyze")
async def analyze_honeypot(payload: HoneypotRequest, request: Request):

    verify_api_key(request)

    incoming_text = payload.message.text
    session_id = payload.sessionId
    history = payload.conversationHistory

    # Detect scam
    scam_detected, keywords = detect_scam(incoming_text)

    # Extract intelligence
    intelligence = extract_intelligence(incoming_text)

    total_messages = len(history) + 1

    # Send to GUVI if scam detected
    if scam_detected:
        send_final_result(
            session_id=session_id,
            scam_detected=True,
            total_messages=total_messages,
            intelligence=intelligence
        )

    # Human-like honeypot reply
    agent_reply = "Why is my account being suspended?"

    return {
        "status": "success",
        "reply": agent_reply
    }
