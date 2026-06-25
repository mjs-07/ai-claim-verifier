import spacy

nlp = spacy.load("en_core_web_sm")


def extract_claims(text: str):

    doc = nlp(text)

    claims = []

    opinion_words = {
        "think",
        "believe",
        "feel",
        "opinion",
        "guess",
        "suppose",
        "prefer",
        "hope"
    }

    recommendation_words = {
        "should",
        "must",
        "ought",
        "recommend",
        "suggest"
    }

    for sent in doc.sents:

        sentence = sent.text.strip()

        if not sentence:
            continue

        sent_doc = nlp(sentence)

        has_subject = False
        has_verb = False
        has_attribute = False

        contains_opinion = False
        contains_recommendation = False

        for token in sent_doc:

            if token.dep_ in (
                "nsubj",
                "nsubjpass"
            ):
                has_subject = True

            if token.pos_ in (
                "VERB",
                "AUX"
            ):
                has_verb = True

            if token.dep_ in (
                "attr",
                "acomp"
            ):
                has_attribute = True

            if token.lemma_.lower() in opinion_words:
                contains_opinion = True

            if token.lemma_.lower() in recommendation_words:
                contains_recommendation = True

        # Reject opinions

        if contains_opinion:
            continue

        # Reject recommendations

        if contains_recommendation:
            continue

        # Accept factual statements

        if has_verb and (
            has_subject or has_attribute
        ) and is_factual_claim(sentence):
            claims.append(sentence)

    return claims