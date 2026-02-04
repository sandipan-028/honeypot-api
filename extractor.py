import re

def extract_entities(text: str):
    # UPI ID pattern (example: name@upi, abc-12@okaxis)
    upi_ids = re.findall(
        r"[a-zA-Z0-9.\-_]{2,}@[a-zA-Z]{2,}",
        text
    )

    # URLs / phishing links
    links = re.findall(
        r"https?://[^\s]+",
        text
    )

    # Phone numbers (India-focused, flexible)
    phone_numbers = re.findall(
        r"\+?\d{10,13}",
        text
    )

    return {
        "upi_ids": list(set(upi_ids)),
        "phishing_links": list(set(links)),
        "phone_numbers": list(set(phone_numbers))
    }
