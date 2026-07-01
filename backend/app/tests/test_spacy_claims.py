# test_spacy_claims.py

from claim_filter import extract_claims

text = """
Hello is a salutation or greeting in the English language.
It is first attested in writing from 1826.
"""

claims = extract_claims(text)

print("\nDetected Claims:")
for claim in claims:
    print("-", claim)