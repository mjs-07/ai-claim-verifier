from claim_normalizer import normalize_claims

claims = [
    "Hello is a salutation or greeting in the English language.",
    "It is first attested in writing from 1826."
]

result = normalize_claims(claims)

print(result)