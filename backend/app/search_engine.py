import os
import requests

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
print("SERPER KEY:", SERPER_API_KEY)

SERPER_URL = "https://google.serper.dev/search"


def search_web(query: str, count: int = 5):

    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "q": query,
        "num": count
    }

    response = requests.post(
        SERPER_URL,
        headers=headers,
        json=payload,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    results = []

    # -----------------------------
    # Answer Box
    # -----------------------------
    answer = data.get("answerBox")

    if answer:

        snippet = answer.get("snippet") or answer.get("answer") or ""

        if snippet:

            results.append({

                "title": answer.get("title", "Answer Box"),

                "url": answer.get("link", ""),

                "snippet": snippet

            })

    # -----------------------------
    # Knowledge Graph
    # -----------------------------
    kg = data.get("knowledgeGraph")

    if kg:

        text = " ".join(filter(None, [

            kg.get("title", ""),

            kg.get("type", ""),

            kg.get("description", "")

        ]))

        if text:

            results.append({

                "title": kg.get("title", "Knowledge Graph"),

                "url": kg.get("website", ""),

                "snippet": text

            })

    # -----------------------------
    # Organic Results
    # -----------------------------
    for item in data.get("organic", []):

        results.append({

            "title": item.get("title", ""),

            "url": item.get("link", ""),

            "snippet": item.get("snippet", "")

        })

    return results