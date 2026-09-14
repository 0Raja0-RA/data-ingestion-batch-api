import requests

print("Uji Next Link Pagination")
url_next = "http://127.0.0.1:8000/transactions?page=1&limit=10"
total_next = 0

while url_next:
    response = requests.get(url_next, timeout=(3, 10))
    response.raise_for_status()
    payload = response.json()
    
    data = payload.get("data", [])
    total_next += len(data)
    print("Fetched:", len(data))
    
    # Mengambil URL selanjutnya langsung dari payload API
    url_next = payload.get("next")

print("Total (Next Link):", total_next)


print("\nUji Cursor Pagination")
url_cursor = "http://127.0.0.1:8000/cursor-transactions"
cursor = None
total_cursor = 0

while True:
    params = {"limit": 10}
    if cursor:
        params["cursor"] = cursor

    response = requests.get(url_cursor, params=params, timeout=(3, 10))
    response.raise_for_status()
    payload = response.json()
    
    data = payload.get("data", [])
    total_cursor += len(data)
    
    # Cursor adalah opaque token, client tidak perlu tahu isinya
    cursor = payload.get("next_cursor")
    print(f"Fetched: {len(data)} | Next Cursor: {cursor}")
    
    if not cursor:
        break

print("Total (Cursor):", total_cursor)