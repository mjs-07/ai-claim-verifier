import requests

from backend.app.semantic_verifier import (
    similarity_score
)


def verify_claim(claim: str):

    response = requests.get(
        "http://localhost:8080/search",
        params={
            "q": claim,
            "format": "json"
        }
    )

    data = response.json()

    results = data.get(
        "results",
        []
    )

    evidence = []

    best_similarity = 0

    for result in results[:5]:

        title = result.get(
            "title",
            ""
        )

        snippet = result.get(
            "content",
            ""
        )

        url = result.get(
            "url",
            ""
        )

        combined_text = (
            title + " " + snippet
        )

        similarity = similarity_score(
            claim,
            combined_text
        )

        evidence.append({
            "title": title,
            "url": url,
            "snippet": snippet,
            "similarity":
                round(
                    similarity * 100,
                    1
                )
        })

        if similarity > best_similarity:
            best_similarity = similarity

    evidence.sort(
        key=lambda x:
        x["similarity"],
        reverse=True
    )

    confidence = int(
        best_similarity * 100
    )

    if confidence >= 70:

        status = "Supported"

    elif confidence >= 50:

        status = "Partially Supported"

    else:

        status = "Unknown"

        evidence = []

    return {
        "claim": claim,
        "status": status,
        "confidence": confidence,
        "evidence": evidence[:5]
    }