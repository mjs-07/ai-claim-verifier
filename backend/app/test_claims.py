from claim_filter import extract_claims

text = """
I think pizza tastes amazing.

The Earth revolves around the Sun.

The U.S. has fifty states.

People should exercise daily.

India's capital is New Delhi.
"""

claims = extract_claims(text)

print("\nDetected Claims:\n")

for claim in claims:
    print("-", claim)