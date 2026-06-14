def verify_claim(claim: str):

    claim = claim.strip()

    if len(claim) < 10:
        return {
            "status": "Unknown",
            "confidence": 0
        }

    return {
        "status": "Supported",
        "confidence": 60
    }