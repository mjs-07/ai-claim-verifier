import torch

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification
)

MODEL_NAME = "cross-encoder/nli-deberta-v3-base"

print("Loading NLI Verifier...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME
)

model.eval()

print("NLI Verifier Loaded!")


LABELS = {
    0: "Contradicted",
    1: "Supported",
    2: "Insufficient Evidence"
}


def verify_with_nli(
    claim: str,
    evidence: str
):
    """
    Performs Natural Language Inference.

    IMPORTANT

    Premise    = Evidence

    Hypothesis = Claim

    Returns
    -------
    {
        status,
        confidence,
        raw_label
    }
    """

    inputs = tokenizer(
        evidence,          # Premise
        claim,             # Hypothesis
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    with torch.no_grad():

        outputs = model(**inputs)

        probabilities = torch.softmax(
            outputs.logits,
            dim=1
        )

        confidence, prediction = torch.max(
            probabilities,
            dim=1
        )

    prediction = prediction.item()

    return {

        "status":
            LABELS[prediction],

        "confidence":
            round(
                confidence.item() * 100,
                2
            ),

        "raw_label":
            prediction
    }