WEIGHTS = {

    "consensus_confidence": 0.35,

    "consensus_strength": 0.25,

    "source_trust": 0.20,

    "similarity": 0.10,

    "nli": 0.10

}


def calculate_credibility(

    decision,

    evidence

):

    avg_trust = 0

    avg_similarity = 0

    avg_nli = 0

    if evidence:

        avg_trust = sum(

            e["source_trust"]

            for e in evidence

        ) / len(evidence)

        avg_similarity = sum(

            e["similarity"]

            for e in evidence

        ) / len(evidence)

        avg_nli = sum(

            e["nli_confidence"]

            for e in evidence

        ) / len(evidence)

    consensus_confidence = decision.get(
        "confidence",
        0
    )

    consensus_strength = (
        decision.get(
            "consensus_strength",
            0
        ) * 100
    )

    credibility = (

        WEIGHTS["consensus_confidence"]
        * consensus_confidence

        +

        WEIGHTS["consensus_strength"]
        * consensus_strength

        +

        WEIGHTS["source_trust"]
        * avg_trust

        +

        WEIGHTS["similarity"]
        * avg_similarity

        +

        WEIGHTS["nli"]
        * avg_nli

    )

    credibility = round(

        credibility,

        2

    )

    # -----------------------------
    # Grade & Risk
    # -----------------------------

    if credibility >= 90:

        grade = "A+"

        risk = "Very Low"

    elif credibility >= 80:

        grade = "A"

        risk = "Low"

    elif credibility >= 70:

        grade = "B"

        risk = "Moderate"

    elif credibility >= 60:

        grade = "C"

        risk = "Elevated"

    else:

        grade = "D"

        risk = "High"

    # -----------------------------
    # Dynamic Verification Summary
    # -----------------------------

    supported = decision.get(
        "supported_sources",
        0
    )

    contradicted = decision.get(
        "contradicted_sources",
        0
    )

    neutral = decision.get(
        "neutral_sources",
        0
    )

    status = decision.get(
        "status",
        "Unknown"
    )

    if status == "Supported":

        if supported >= 3:

            summary = (
                f"Verified by {supported} trusted "
                f"sources with strong agreement."
            )

        elif supported == 2:

            summary = (
                "Supported by multiple trusted "
                "sources."
            )

        else:

            summary = (
                "Supported by available "
                "evidence."
            )

    elif status == "Contradicted":

        if contradicted >= 3:

            summary = (
                f"{contradicted} trusted sources "
                "contradict this claim."
            )

        elif contradicted == 2:

            summary = (
                "Multiple trusted sources "
                "contradict this claim."
            )

        else:

            summary = (
                "Available evidence contradicts "
                "this claim."
            )

    else:

        if neutral > 0:

            summary = (
                "Reliable evidence is currently "
                "insufficient to verify this claim."
            )

        else:

            summary = (
                "Evidence is mixed. Interpret "
                "this claim cautiously."
            )

    # -----------------------------
    # Return
    # -----------------------------

    return {

        "credibility_score":

            credibility,

        "grade":

            grade,

        "risk_level":

            risk,

        "verification_summary":

            summary,

        "metrics": {

            "consensus_confidence":

                round(
                    consensus_confidence,
                    2
                ),

            "consensus_strength":

                round(
                    consensus_strength,
                    2
                ),

            "average_source_trust":

                round(
                    avg_trust,
                    2
                ),

            "average_similarity":

                round(
                    avg_similarity,
                    2
                ),

            "average_nli_confidence":

                round(
                    avg_nli,
                    2
                )

        }

    }