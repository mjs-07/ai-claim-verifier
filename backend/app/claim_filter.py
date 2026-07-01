import spacy

nlp = spacy.load("en_core_web_sm")


OPINION_WORDS = {
    "think",
    "believe",
    "feel",
    "opinion",
    "guess",
    "suppose",
    "prefer",
    "hope"
}

RECOMMENDATION_WORDS = {
    "should",
    "must",
    "ought",
    "recommend",
    "suggest"
}


def is_verifiable_claim(sentence: str) -> bool:
    """
    Determines whether a sentence is a factual,
    verifiable claim.

    Returns:
        True  -> Fact-checkable
        False -> Opinion / Recommendation /
                 Fragment / Conversation
    """

    doc = nlp(sentence)

    has_subject = False
    has_verb = False
    has_attribute = False

    contains_opinion = False
    contains_recommendation = False

    entity_count = len(doc.ents)

    for token in doc:

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

        lemma = token.lemma_.lower()

        if lemma in OPINION_WORDS:
            contains_opinion = True

        if lemma in RECOMMENDATION_WORDS:
            contains_recommendation = True

    # -------------------------
    # Reject obvious non-claims
    # -------------------------

    if contains_opinion:
        return False

    if contains_recommendation:
        return False

    if len(sentence.split()) < 4:
        return False

    if not has_verb:
        return False

    if not (has_subject or has_attribute):
        return False

    # -------------------------
    # Positive indicators
    # -------------------------

    if entity_count > 0:
        return True

    if has_subject and has_verb:
        return True

    return False


def extract_claims(text: str):
    """
    Extract only factual,
    verifiable claims.
    """

    doc = nlp(text)

    claims = []

    for sent in doc.sents:

        sentence = sent.text.strip()

        if not sentence:
            continue

        if is_verifiable_claim(sentence):
            claims.append(sentence)

    return claims