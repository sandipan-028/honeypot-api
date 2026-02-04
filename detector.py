SCAM_KEYWORDS = [
    "blocked",
    "kyc",
    "otp",
    "urgent",
    "verify",
    "refund",
    "account",
    "click",
    "link",
    "upi"
]

def detect_scam(message: str):
    msg = message.lower()

    matched = [k for k in SCAM_KEYWORDS if k in msg]
    keyword_count = len(matched)

    confidence = min(keyword_count / 5, 1.0)

    return {
        "scam_detected": confidence > 0.4,
        "confidence_score": round(confidence, 2),
        "matched_keywords": matched
    }
