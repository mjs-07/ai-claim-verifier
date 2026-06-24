import requests


def verify_claim(claim: str):

    response = requests.get(
        "http://localhost:8080/search",
        params={
            "q": claim,
            "format": "json"
        }
    )

    data = response.json()

    results = data.get("results", [])

    evidence = []

    for result in results[:5]:
        evidence.append({
            "title": result.get("title"),
            "url": result.get("url")
        })

    relevant_results = 0

    claim_words = set(
        claim.lower().split()
    )

    for result in results[:5]:

        title = result.get(
            "title", ""
        ).lower()

        overlap = claim_words.intersection(
            set(title.split())
        )

        if len(overlap) >= 2:
            relevant_results += 1

    confidence = min(
        relevant_results * 25,
        95
    )

    status = ( "Supported" if confidence >= 50 else "Unknown")

    if confidence < 50:
        evidence = []

    return {
        "status": status,
        "confidence": confidence,
        "evidence": evidence
    }