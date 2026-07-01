from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification

import torch

MODEL_NAME = "cross-encoder/nli-deberta-v3-base"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME
)

pairs = [

    {
        "claim": "The Earth revolves around the Sun.",
        "evidence": "The Earth revolves around the Sun once every 365.25 days.",
        "expected": "entailment"
    },

    {
        "claim": "The Moon is made of cheese.",
        "evidence": "The Moon is a rocky natural satellite of Earth.",
        "expected": "contradiction"
    },

    {
        "claim": "India's capital is New Delhi.",
        "evidence": "India is the seventh-largest country by area.",
        "expected": "neutral"
    },

    {
        "claim": "Water boils at 100°C.",
        "evidence": "Water boils at 100 degrees Celsius at sea level.",
        "expected": "entailment"
    },

    {
        "claim": "COVID-19 is caused by bacteria.",
        "evidence": "COVID-19 is caused by the SARS-CoV-2 virus.",
        "expected": "contradiction"
    },

    {
        "claim": "WHO declared COVID-19 a pandemic.",
        "evidence": "WHO declared COVID-19 a pandemic in March 2020.",
        "expected": "entailment"
    },

    {
        "claim": "Paris is the capital of Germany.",
        "evidence": "Berlin is the capital of Germany.",
        "expected": "contradiction"
    },

    {
        "claim": "Apple acquired OpenAI.",
        "evidence": "Apple announced a new iPhone today.",
        "expected": "neutral"
    },

    {
        "claim": "Jupiter is the largest planet.",
        "evidence": "Jupiter is the largest planet in the Solar System.",
        "expected": "entailment"
    },

    {
        "claim": "Humans have three hearts.",
        "evidence": "Humans normally have one heart.",
        "expected": "contradiction"
    }

]

for claim, evidence, expected in pairs:

    result = classifier({
        "text": claim,
        "text_pair": evidence
    }, 
    return_all_scores=True)

    print(result)