from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import Optional

from auth import verify_api_key
from detector import detect_scam
from extractor import extract_entities
from llm import decide_next_message

app = FastAPI(title="Agentic AI Honeypot API")


# -------------------- Models --------------------

class HoneypotRequest(BaseModel):
    conversation_id: str
    incoming_message: str
    source: Optional[str] = None
    timestamp: Optional[str] = None


# -------------------- Routes --------------------

@app.get("/")
def root():
    return {"status": "honeypot api running"}


@app.post("/api/v1/honeypot/analyze")
async def analyze_honeypot(
    req: HoneypotRequest,
    request: Request
):
    # -------- AUTH --------
    verify_api_key(request)

    try:
        # -------- SCAM DETECTION --------
        scam_result = detect_scam(req.incoming_message) or {}

        # -------- ENTITY EXTRACTION --------
        entities = extract_entities(req.incoming_message) or {}

        # -------- AGENT RESPONSE --------
        history = [
            {"role": "user", "content": req.incoming_message}
        ]
        agent_reply = decide_next_message(history)

        # -------- SAFE RESPONSE --------
        return {
            "conversation_id": req.conversation_id,
            "scam_detected": scam_result.get("scam_detected", False),
            "risk_level": scam_result.get("risk_level", "LOW"),
            "confidence_score": scam_result.get("confidence_score", 0.0),
            "matched_keywords": scam_result.get("matched_keywords", []),
            "extracted_entities": entities,
            "agent_reply": agent_reply
        }

    except Exception as e:
        # NEVER crash the API
        print("HONEYPOT ERROR:", str(e))
        raise HTTPException(
            status_code=500,
            detail="Internal honeypot processing error (handled safely)"
        )
