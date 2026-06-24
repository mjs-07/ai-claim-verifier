import requests

response = requests.get(
    "http://localhost:8080/search",
    params={
        "q": "The Earth revolves around the Sun",
        "format": "json"
    }
)

print(response.status_code)

data = response.json()

print("Results:", len(data["results"]))

for result in data["results"][:3]:
    print(result["title"])
    print(result["url"])
    print()