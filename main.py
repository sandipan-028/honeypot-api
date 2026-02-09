from fastapi import FastAPI, Request, HTTPException
from typing import Dict, Any
import requests
import re

app = FastAPI(title="Agentic AI Honeypot")


# -----------------------------
# API KEY CONFIG
# -----------------------------
VALID_API_KEY = "sk_honeypot_demo_123"


def verify_api_key(request: Request):

    auth_header = request.headers.get("Authorization")
    x_api_key = request.headers.get("x-api-key")

    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        if token == VALID_API_KEY:
            return True

    if auth_header and auth_header == VALID_API_KEY:
        return True

    if x_api_key and x_api_key == VALID_API_KEY:
        return True

    raise HTTPException(status_code=401, detail="Invalid API key")


# -----------------------------
# SIMPLE SCAM DETECTION
# -----------------------------
SCAM_KEYWORDS = [
    "blocked",
    "verify",
    "urgent",
    "otp",
    "upi",
    "payment",
    "suspend",
    "account blocked"
]


def detect_scam(text):
    text_lower = text.lower()
    matched = [k for k in SCAM_KEYWORDS if k in text_lower]

    return {
        "scam_detected": len(matched) > 0,
        "matched_keywords": matched
    }


# -----------------------------
# INTELLIGENCE EXTRACTION
# -----------------------------
def extract_intelligence(text):

    upi_ids = re.findall(r"[a-zA-Z0-9._-]+@[a-zA-Z]+", text)
    links = re.findall(r"https?://\S+", text)
    phones = re.findall(r"\+91\d{10}", text)

    return {
        "bankAccounts": [],
        "upiIds": upi_ids,
        "phishingLinks": links,
        "phoneNumbers": phones,
        "suspiciousKeywords": SCAM_KEYWORDS
    }


# -----------------------------
# SEND FINAL RESULT TO GUVI
# -----------------------------
def send_final_result(session_id, scam_detected, total_messages, intelligence):

    payload = {
        "sessionId": session_id,
        "scamDetected": scam_detected,
        "totalMessagesExchanged": total_messages,
        "extractedIntelligence": intelligence,
        "agentNotes": "Scammer used urgency and financial redirection tactics"
    }

    try:
        requests.post(
            "https://hackathon.guvi.in/api/updateHoneyPotFinalResult",
            json=payload,
            timeout=5
        )
    except Exception as e:
        print("GUVI Reporting Error:", e)


# -----------------------------
# ROOT ROUTE
# -----------------------------
@app.get("/")
def root():
    return {"status": "honeypot api running"}


# -----------------------------
# MAIN HONEYPOT ENDPOINT
# -----------------------------
@app.post("/api/v1/honeypot/analyze")
async def analyze_honeypot(request: Request):

    verify_api_key(request)

    try:
        body: Dict[str, Any] = await request.json()
    except:
        body = {}

    # ---------------- Parse Payload ----------------
    session_id = body.get("sessionId", "unknown")

    message_obj = body.get("message", {})
    incoming_text = message_obj.get("text", "Hello")

    history = body.get("conversationHistory", [])

    # ---------------- Scam Detection ----------------
    scam_result = detect_scam(incoming_text)

    # ---------------- Intelligence Extraction ----------------
    intelligence = extract_intelligence(incoming_text)

    # ---------------- Total Messages ----------------
    total_messages = len(history) + 1

    # ---------------- Report To GUVI ----------------
    if scam_result["scam_detected"]:
        send_final_result(
            session_id=session_id,
            scam_detected=True,
            total_messages=total_messages,
            intelligence=intelligence
        )

    # ---------------- Honeypot Reply ----------------
    agent_reply = "Why is my account being suspended?"

    # ---------------- Validator Response ----------------
    return {
        "status": "success",
        "reply": agent_reply
    }
