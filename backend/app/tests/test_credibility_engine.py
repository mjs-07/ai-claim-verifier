from credibility_engine import (
    calculate_credibility
)

decision = {

    "status": "Supported",

    "confidence": 86,

    "consensus_strength": 0.80,

    "supported_sources": 4,

    "contradicted_sources": 1,

    "neutral_sources": 0

}

evidence = [

    {

        "source_trust": 100,

        "similarity": 94,

        "nli_confidence": 99

    },

    {

        "source_trust": 92,

        "similarity": 88,

        "nli_confidence": 98

    },

    {

        "source_trust": 60,

        "similarity": 73,

        "nli_confidence": 95

    }

]

result = calculate_credibility(

    decision,

    evidence

)

print(result)