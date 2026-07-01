from semantic_verifier import (
    similarity_score
)

claim = (
    "The Earth revolves around the Sun."
)

evidence = (
    "Earth orbits the Sun once every year."
)

score = similarity_score(
    claim,
    evidence
)

print("\nSimilarity:")
print(score)