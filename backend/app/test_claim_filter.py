from claim_filter import extract_claims

text = """
The Earth revolves around the Sun.
I think astronomy is fascinating.
Water boils at 100 degrees Celsius.
You should study science.
"""

claims = extract_claims(text)

print(claims)