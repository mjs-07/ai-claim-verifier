import requests

response = requests.get(
    "http://localhost:8080/search",
    params={
        "q": "The Earth revolves around the Sun",
        "format": "json"
    }
)

print("Status Code:")
print(response.status_code)

print()

print("Content Type:")
print(response.headers.get("Content-Type"))

print()

print("Response:")
print(response.text[:1000])