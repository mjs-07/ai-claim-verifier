import requests

from backend.app.semantic_verifier import (
    similarity_score
)

from backend.app.nli_verifier import (
    verify_with_nli
)

from backend.app.source_ranker import (
    get_source_metadata
)

from backend.app.consensus_engine import (
    consensus_decision
)
from backend.app.credibility_engine import (
    calculate_credibility
)


SEARXNG_URL = "http://localhost:8080/search"


def verify_claim(claim: str):

    # -----------------------------
    # Step 1 : Retrieve Search Results
    # -----------------------------

    response = requests.get(
        SEARXNG_URL,
        params={
            "q": claim,
            "format": "json"
        },
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    results = data.get(
        "results",
        []
    )

    # -----------------------------
    # Step 2 : Semantic Ranking
    # -----------------------------

    candidate_evidence = []

    for result in results[:10]:

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

        combined = (
            title +
            ". " +
            snippet
        )

        similarity = similarity_score(
            claim,
            combined
        )

        candidate_evidence.append({

            "title": title,

            "url": url,

            "snippet": snippet,

            "combined": combined,

            "similarity": round(
                similarity * 100,
                2
            )

        })

    # -----------------------------
    # Step 3 : Keep Best Semantic Matches
    # -----------------------------

    candidate_evidence.sort(

        key=lambda x:
        x["similarity"],

        reverse=True

    )

    top_candidates = candidate_evidence[:5]

    # -----------------------------
    # Step 4 : Source Ranking + NLI
    # -----------------------------

    evidence = []

    for item in top_candidates:

        metadata = get_source_metadata(
            item["url"]
        )

        nli = verify_with_nli(
            claim,
            item["combined"]
        )

        evidence.append({

            **item,

            "domain":
                metadata["domain"],

            "category":
                metadata["category"],

            "tier":
                metadata["tier"],

            "source_trust":
                metadata["trust"],

            "nli_status":
                nli["status"],

            "nli_confidence":
                round(
                    nli["confidence"],
                    2
                )

        })

    # -----------------------------
    # Step 5 : Consensus Decision
    # -----------------------------

    decision = consensus_decision(
        evidence
    )

    credibility = calculate_credibility(
        decision,
        evidence
    )

    # -----------------------------
    # Step 6 : Final Evidence Ranking
    # -----------------------------

    evidence.sort(

        key=lambda x: (

            x["weighted_score"],

            x["similarity"]

        ),

        reverse=True

    )

    # -----------------------------
    # Step 7 : API Response
    # -----------------------------

    return {

        "claim": claim,

        "status":
            decision["status"],

        "confidence":
            decision["confidence"],

        "agreement_ratio":
            decision["agreement_ratio"],

        "consensus_strength":
            decision["consensus_strength"],

        "positive_score":
            decision["positive_score"],

        "negative_score":
            decision["negative_score"],

        "supported_sources":
            decision["supported_sources"],

        "contradicted_sources":
            decision["contradicted_sources"],

        "neutral_sources":
            decision["neutral_sources"],

        "credibility":

            credibility,

        "evidence":

            evidence[:3]

    }