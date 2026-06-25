from sentence_transformers import (
    SentenceTransformer
)
from sentence_transformers.util import (
    cos_sim
)

print("Loading MiniLM Verifier...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("MiniLM Loaded!")


def similarity_score(
    claim: str,
    evidence_text: str
):

    claim_embedding = model.encode(
        claim,
        convert_to_tensor=True
    )

    evidence_embedding = model.encode(
        evidence_text,
        convert_to_tensor=True
    )

    score = cos_sim(
        claim_embedding,
        evidence_embedding
    )

    return float(score.item())