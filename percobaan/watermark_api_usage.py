import requests

from watermark import load_watermark

watermark = load_watermark("../state/watermark.json")
print("Watermark dipakai:", watermark)

response = requests.get(
    "http://127.0.0.1:8000/transactions",
    params={
        "page": 1,
        "limit": 10,
        "updated_since": watermark,
    },
    timeout=(3, 10),
)

response.raise_for_status()

payload = response.json()

print("Jumlah record setelah watermark:", len(payload["data"]))
print(payload["data"])
