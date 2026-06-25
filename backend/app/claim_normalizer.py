import spacy

nlp = spacy.load("en_core_web_sm")


def normalize_claims(claims):

    normalized_claims = []

    previous_subject = None

    pronouns = {
        "it",
        "they",
        "them",
        "this",
        "these",
        "those"
    }

    for claim in claims:

        doc = nlp(claim)

        current_subject = None

        # First try grammatical subject
        for token in doc:

            if token.dep_ in (
                "nsubj",
                "nsubjpass"
            ):
                current_subject = token.text
                break

        # Fallback for definition sentences
        if not current_subject:

            for token in doc:

                if token.pos_ in (
                    "PROPN",
                    "NOUN",
                    "INTJ"
                ):
                    current_subject = token.text
                    break

        first_token = doc[0].text.lower()

        if (
            first_token in pronouns
            and previous_subject
        ):

            normalized_claim = (
                previous_subject +
                claim[len(doc[0].text):]
            )

            normalized_claims.append(
                normalized_claim
            )

        else:

            normalized_claims.append(
                claim
            )

        if current_subject:
            previous_subject = current_subject

    return normalized_claims