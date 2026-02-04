import random

SCAMMER_REPLIES = [
    "Send money to fraudster@upi to verify account",
    "Click this link http://fake-kyc.com immediately",
    "Share OTP now or account will be blocked",
    "Call +919876543210 for verification"
]

def send_to_scammer(message: str):
    """
    Simulates scammer response.
    """
    return random.choice(SCAMMER_REPLIES)
