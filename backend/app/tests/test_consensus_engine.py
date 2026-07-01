from consensus_engine import consensus_decision


sample = [

    {

        "source_trust":100,

        "nli_status":"Supported",

        "nli_confidence":99,

        "similarity":95

    },

    {

        "source_trust":92,

        "nli_status":"Supported",

        "nli_confidence":98,

        "similarity":82

    },

    {

        "source_trust":60,

        "nli_status":"Contradicted",

        "nli_confidence":95,

        "similarity":74

    }

]


result = consensus_decision(sample)

print(result)

print()

for evidence in sample:

    print(evidence)