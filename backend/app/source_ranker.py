from urllib.parse import urlparse


DOMAIN_MAP = {

    # Government

    "nasa.gov": "Government",
    "cdc.gov": "Government",
    "nih.gov": "Government",
    "india.gov.in": "Government",

    # International Organizations

    "who.int": "International Organization",
    "un.org": "International Organization",
    "unesco.org": "International Organization",

    # Scientific

    "nature.com": "Scientific Journal",
    "sciencedirect.com": "Scientific Journal",
    "springer.com": "Scientific Journal",

    # Universities

    "mit.edu": "University",
    "stanford.edu": "University",
    "ox.ac.uk": "University",
    "cam.ac.uk": "University",

    # Encyclopedia

    "wikipedia.org": "Encyclopedia",
    "britannica.com": "Encyclopedia",

    # News

    "reuters.com": "Major News",
    "apnews.com": "Major News",
    "bbc.com": "Major News",

    # Documentation

    "docs.python.org": "Company Documentation",
    "developer.mozilla.org": "Company Documentation",

    # Blogs

    "medium.com": "Professional Blog",
    "towardsdatascience.com": "Professional Blog",

    # Community

    "stackoverflow.com": "Community Forum",

    # Reddit

    "reddit.com": "Reddit",

    # Video

    "youtube.com": "Video Platform",

    # Social

    "facebook.com": "Social Media",
    "instagram.com": "Social Media",
    "x.com": "Social Media",
    "twitter.com": "Social Media"

}


TRUST_TABLE = {

    "Government": 100,

    "International Organization": 99,

    "Scientific Journal": 98,

    "Major News": 96,

    "University": 95,

    "Encyclopedia": 92,

    "Company Documentation": 88,

    "Professional Blog": 75,

    "Community Forum": 70,

    "Reddit": 60,

    "Video Platform": 45,

    "Social Media": 35,

    "Unknown": 55

}


def get_source_metadata(url: str):

    domain = urlparse(url).netloc.lower()

    domain = domain.replace("www.", "")

    category = "Unknown"

    for known_domain in DOMAIN_MAP:

        if known_domain in domain:

            category = DOMAIN_MAP[known_domain]

            break

    trust = TRUST_TABLE[category]

    if trust >= 95:

        tier = "A+"

    elif trust >= 85:

        tier = "A"

    elif trust >= 70:

        tier = "B"

    elif trust >= 50:

        tier = "C"

    else:

        tier = "D"

    return {

        "domain": domain,

        "category": category,

        "tier": tier,

        "trust": trust

    }