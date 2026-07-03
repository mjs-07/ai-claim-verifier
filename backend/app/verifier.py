import requests
import re

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

from backend.app.claim_normalizer import (
    normalize_claims
)


SEARXNG_URL = "http://localhost:8080/search"

def best_matching_text(claim: str, text: str):

    """
    Returns the sentence from the evidence that is
    most semantically similar to the claim.
    """

    if not text.strip():
        return text

    sentences = re.split(
        r'(?<=[.!?])\s+',
        text
    )

    best_sentence = text
    best_similarity = -1

    for sentence in sentences:

        sentence = sentence.strip()

        if not sentence:
            continue

        similarity = similarity_score(
            claim,
            sentence
        )

        if similarity > best_similarity:

            best_similarity = similarity
            best_sentence = sentence

    return best_sentence


def verify_claim(claim: str):

    # ---------------------------------
    # Step 1 : Normalize Search Query
    # ---------------------------------

    normalized = normalize_claims([claim])

    if normalized:
        search_query = normalized[0]
    else:
        search_query = claim

    # ---------------------------------
    # Step 2 : Retrieve Search Results
    # ---------------------------------

    response = requests.get(

        SEARXNG_URL,

        params={
            "q": search_query,
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

    # Retrieve more candidates
    results = results[:20]

    # ---------------------------------
    # Step 3 : Semantic Ranking +
    #          Source Trust Ranking
    # ---------------------------------

    candidate_evidence = []

    seen_urls = set()

    for result in results:

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

        if not url:
            continue

        # Remove duplicate URLs
        normalized_url = url.split("?")[0]

        if normalized_url in seen_urls:
            continue

        seen_urls.add(normalized_url)

        combined = (
            title +
            ". " +
            snippet
        )

        best_sentence = best_matching_text(
            claim,
            combined
        )

        similarity = similarity_score(
            claim,
            best_sentence
        )

        metadata = get_source_metadata(
            url
        )

        source_trust = metadata["trust"]

        ranking_score = (

            0.75 * similarity +

            0.25 * (source_trust / 100)

        )

        candidate_evidence.append({

            "title": title,

            "url": url,

            "snippet": snippet,

            "combined": combined,

            "matched_sentence": best_sentence, 

            "similarity": round(
                similarity * 100,
                2
            ),

            "ranking_score": ranking_score,

            "domain": metadata["domain"],

            "category": metadata["category"],

            "tier": metadata["tier"],

            "source_trust": source_trust

        })

    # ---------------------------------
    # Step 4 : Keep Best Ranked Results
    # ---------------------------------

    candidate_evidence.sort(

        key=lambda x: x["ranking_score"],

        reverse=True

    )

    top_candidates = candidate_evidence[:5]

    # ---------------------------------
    # Step 5 : NLI Verification
    # ---------------------------------

    evidence = []

    for item in top_candidates:

        nli = verify_with_nli(
            claim,
            item["matched_sentence"]
        )

        evidence.append({

            **item,

            "nli_status":
                nli["status"],

            "nli_confidence":
                round(
                    nli["confidence"],
                    2
                )

        })

    # ---------------------------------
    # Step 6 : Consensus
    # ---------------------------------

    decision = consensus_decision(
        evidence
    )

    credibility = calculate_credibility(

        decision,

        evidence

    )

    # ---------------------------------
    # Step 7 : Final Evidence Ranking
    # ---------------------------------

    evidence.sort(

        key=lambda x: (

            x["weighted_score"],

            x["ranking_score"]

        ),

        reverse=True

    )

    # Remove internal ranking score
    for item in evidence:

        item.pop(
            "ranking_score",
            None
        )

    # ---------------------------------
    # Step 8 : API Response
    # ---------------------------------

    return {

        "claim": claim,

        "status":
            decision["status"],

        "confidence":
            min(
                decision["confidence"],
                99
            ),

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