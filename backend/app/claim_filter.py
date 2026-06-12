import re


def extract_claims(text: str):

    sentences = re.split(r'[.!?]+', text)

    claims = []

    opinion_starters = [
        "i think",
        "i believe",
        "in my opinion",
        "personally"
    ]

    recommendation_words = [
        "should",
        "must",
        "ought to"
    ]

    for sentence in sentences:

        sentence = sentence.strip()

        if not sentence:
            continue

        lower_sentence = sentence.lower()

        # Reject opinions

        if any(
            lower_sentence.startswith(opinion)
            for opinion in opinion_starters
        ):
            continue

        # Reject recommendations

        if any(
            word in lower_sentence
            for word in recommendation_words
        ):
            continue

        claims.append(sentence)

    return claims