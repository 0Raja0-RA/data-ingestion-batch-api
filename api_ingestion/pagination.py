import logging


logger = logging.getLogger("pagination")

MAX_PAGES = 1000


def fetch_pages(fetch_function, watermark=None, page_size=10, max_pages=MAX_PAGES):
    """
    Generator yang mengambil seluruh halaman dari API page-number based.
    fetch_function(page, limit, watermark) -> payload dict dengan key "data" (list).
    Berhenti ketika data kosong atau max_pages terlampaui (pengaman infinite loop).
    """
    page = 1

    while True:
        if page > max_pages:
            raise RuntimeError("Maximum page limit exceeded")

        payload = fetch_function(page=page, limit=page_size, watermark=watermark)
        data = payload.get("data", [])

        logger.info("Fetched page=%s records=%s", page, len(data))

        if not data:
            break

        yield data
        page += 1