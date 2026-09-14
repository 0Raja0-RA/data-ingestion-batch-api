import requests

url = "http://127.0.0.1:8000/transactions"
page = 1
limit = 10
MAX_PAGES = 1000
all_data = []

while True:
    if page > MAX_PAGES:
        raise RuntimeError("Maximum page limit exceeded")

    response = requests.get(url, params={"page": page, "limit": limit}, timeout=(3, 10))
    response.raise_for_status()

    data = response.json().get("data", [])
    if not data:
        break

    all_data.extend(data)
    print(f"Page {page}: {len(data)} record")
    page += 1

print("Total record:", len(all_data))