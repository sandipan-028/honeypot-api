from fastapi import FastAPI, Depends
from pydantic import BaseModel

# Internal imports
from auth import verify_api_key
from detector import detect_scam
from extractor import extract_entities
from agent_state import AgentState
from llm import decide_next_message
from scammer_api import send_to_scammer

# -----------------------------
# Create FastAPI app
# -----------------------------
app = FastAPI(title="Agentic AI Honeypot")

# -----------------------------
# Request Schema
# -----------------------------
class HoneypotInput(BaseModel):
    conversation_id: str
    incoming_message: str
    source: str
    timestamp: str

# -----------------------------
# Health Check
# -----------------------------
@app.get("/")
def root():
    return {"status": "honeypot api running"}

# -----------------------------
# Secure Test Endpoint
# -----------------------------
@app.get("/secure")
def secure_test(auth=Depends(verify_api_key)):
    return {"status": "authenticated access granted"}

# -----------------------------
# Agentic Honeypot Endpoint
# -----------------------------
@app.post("/api/v1/honeypot/analyze")
def analyze(
    data: HoneypotInput,
    auth=Depends(verify_api_key)
):
    # 1️⃣ Scam detection
    detection = detect_scam(data.incoming_message)

    # If not a scam, exit early
    if not detection["scam_detected"]:
        return {
            "conversation_id": data.conversation_id,
            "scam_detected": False,
            "confidence_score": detection["confidence_score"],
            "risk_level": "LOW",
            "message": "No scam indicators detected"
        }

    # 2️⃣ Initialize honeypot agent state
    state = AgentState()

    # Seed conversation with initial message
    state.history.append({
        "role": "user",
        "content": data.incoming_message
    })

    MAX_TURNS = 3

    # 3️⃣ Agentic conversation loop
    while state.turns < MAX_TURNS:
        # Agent decides next message
        agent_message = decide_next_message(state.history)
        state.history.append({
            "role": "assistant",
            "content": agent_message
        })

        # Mock scammer reply
        scammer_reply = send_to_scammer(agent_message)
        state.history.append({
            "role": "user",
            "content": scammer_reply
        })

        # Extract entities from scammer reply
        extracted = extract_entities(scammer_reply)
        for key in state.extracted_entities:
            state.extracted_entities[key].extend(extracted.get(key, []))

        state.turns += 1

        # Stop early if valuable intelligence is captured
        if (
            state.extracted_entities["upi_ids"]
            or state.extracted_entities["phishing_links"]
        ):
            break

    # 4️⃣ Final response
    return {
        "conversation_id": data.conversation_id,
        "scam_detected": True,
        "persona_used": state.persona,
        "confidence_score": detection["confidence_score"],
        "matched_keywords": detection["matched_keywords"],
        "extracted_entities": state.extracted_entities,
        "risk_level": "HIGH",
        "conversation_turns": state.turns
    }
