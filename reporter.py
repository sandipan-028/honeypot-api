import requests


def send_final_result(
    session_id,
    scam_detected,
    total_messages,
    intelligence,
    agent_notes
):

    intelligence_dict = {
        "bankAccounts": intelligence.get("bankAccounts", []),
        "upiIds": intelligence.get("upiIds", []),
        "phishingLinks": intelligence.get("phishingLinks", []),
        "phoneNumbers": intelligence.get("phoneNumbers", []),
        "suspiciousKeywords": intelligence.get("suspiciousKeywords", [])
    }

    payload = {
        "sessionId": session_id,
        "scamDetected": scam_detected,
        "totalMessagesExchanged": total_messages,
        "extractedIntelligence": intelligence_dict,
        "agentNotes": agent_notes
    }

    try:
        response = requests.post(
            "https://hackathon.guvi.in/api/updateHoneyPotFinalResult",
            json=payload,
            timeout=5
        )

        print("GUVI API Status:", response.status_code)
        print("GUVI API Response:", response.text)

    except Exception as e:
        print("Error sending final result:", e)
