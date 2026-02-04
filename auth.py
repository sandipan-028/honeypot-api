from fastapi import Request, HTTPException, status

# Demo API key for hackathon / judges
VALID_API_KEY = "sk_honeypot_demo_123"


def verify_api_key(request: Request):
    """
    Verifies API key from Authorization header.
    Always fails safely with 401, never crashes.
    """

    auth_header = request.headers.get("Authorization")

    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key"
        )

    # Expected format: "Bearer <key>"
    parts = auth_header.split()

    if len(parts) != 2 or parts[0] != "Bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header format"
        )

    token = parts[1]

    if token != VALID_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )

    # If valid, simply return (do nothing)
    return True
