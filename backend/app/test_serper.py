from search_engine import search_web

results = search_web(
    "Moon is made of cheese",
    3
)

for r in results:
    print("=" * 60)
    print(r["title"])
    print(r["url"])
    print(r["snippet"])