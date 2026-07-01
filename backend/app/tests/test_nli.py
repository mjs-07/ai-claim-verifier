from nli_verifier import (
    verify_with_nli
)

pairs = [

    {
        "The Earth revolves around the Sun.",
        "The Earth revolves around the Sun once every 365.25 days.",
        #"expected": "entailment"
    },

    {
        "The Moon is made of cheese.",
        "The Moon is a rocky natural satellite of Earth.",
        #"expected": "contradiction"
    },

    {
        "India's capital is New Delhi.",
        "India is the seventh-largest country by area.",
        #"expected": "neutral"
    },

    {
        "Water boils at 100°C.",
        "Water boils at 100 degrees Celsius at sea level.",
        #"expected": "entailment"
    },

    {
        "COVID-19 is caused by bacteria.",
        "COVID-19 is caused by the SARS-CoV-2 virus.",
        #"expected": "contradiction"
    },

    {
        "WHO declared COVID-19 a pandemic.",
        "WHO declared COVID-19 a pandemic in March 2020.",
        #"expected": "entailment"
    },

    {
        "Paris is the capital of Germany.",
        "Berlin is the capital of Germany.",
        #"expected": "contradiction"
    },

    {
        "Apple acquired OpenAI.",
        "Apple announced a new iPhone today.",
        #"expected": "neutral"
    },

    {
        "Jupiter is the largest planet.",
        "Jupiter is the largest planet in the Solar System.",
        #"expected": "entailment"
    },

    {
        "Humans have three hearts.",
        "Humans normally have one heart.",
        #"expected": "contradiction"
    }

]

for claim, evidence in pairs:

    print("\n--------------------------------")

    print("Claim:")
    print(claim)

    print()

    print("Evidence:")
    print(evidence)

    print()

    print(
        verify_with_nli(
            claim,
            evidence
        )
    )