from source_ranker import get_source_metadata


urls = [

    "https://en.wikipedia.org/wiki/Hello",

    "https://www.nasa.gov",

    "https://www.who.int",

    "https://www.reddit.com",

    "https://www.youtube.com",

    "https://www.instagram.com",

    "https://medium.com",

    "https://unknownwebsite123.com"

]

for url in urls:

    print()

    print(url)

    print(get_source_metadata(url))