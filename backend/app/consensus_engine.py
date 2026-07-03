def consensus_decision(evidence_list):

    positive = 0.0

    negative = 0.0

    supported = 0

    contradicted = 0

    neutral = 0

    for evidence in evidence_list:

        trust = evidence["source_trust"]

        confidence = evidence["nli_confidence"]

        similarity = evidence.get("similarity", 100)

        weighted = (
            confidence
            * (trust / 100)
            * (similarity / 100)
        )

        evidence["weighted_score"] = round(weighted, 2)

        if evidence["nli_status"] == "Supported":

            positive += weighted

            supported += 1

        elif evidence["nli_status"] == "Contradicted":

            negative += weighted

            contradicted += 1

        else:

            neutral += 1

    total = positive + negative

    if total == 0:

        return {

            "status": "Insufficient Evidence",

            "confidence": 0,

            "agreement_ratio": 0,

            "positive_score": 0,

            "negative_score": 0,

            "supported_sources": supported,

            "contradicted_sources": contradicted,

            "neutral_sources": neutral,

            "consensus_strength": 0

        }

    confidence = abs(
        positive - negative
    ) / total

    confidence *= 100

    if positive > negative:

        status = "Supported"

    elif negative > positive:

        status = "Contradicted"

    else:

        status = "Insufficient Evidence"

    agreement_ratio = 0

    if total > 0:

        agreement_ratio = max(
            positive,
            negative
        ) / total
    
    voting_sources = supported + contradicted

    if voting_sources == 0:

        consensus_strength = 0

    else:

        consensus_strength = supported / voting_sources

        if negative > positive:

            consensus_strength = contradicted / voting_sources


    return {

        "status": status,

        "confidence": round(
            confidence,
            2
        ),

        "agreement_ratio": round(
            agreement_ratio,
            3
        ),

        "positive_score": round(
            positive,
            2
        ),

        "negative_score": round(
            negative,
            2
        ),

        "supported_sources": supported,

        "contradicted_sources": contradicted,

        "neutral_sources": neutral,

        "consensus_strength": round(
            consensus_strength,
            3
        )

    }