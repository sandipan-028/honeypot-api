from fastapi import Header, HTTPException

# Simple static API key for hackathon/demo
API_KEY = "sk_honeypot_demo_123"

def verify_api_key(authorization: str = Header(None)):
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing API key")

    token = authorization.split(" ", 1)[1]
    if token != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
