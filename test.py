import requests

url = "http://127.0.0.1:8000/fetch-news"
params = {"preferences": "technology,health"}

response = requests.get(url, params=params)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")
