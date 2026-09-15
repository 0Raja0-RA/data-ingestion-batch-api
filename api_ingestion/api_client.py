import logging
import random
import time

import requests


logger = logging.getLogger("api_client")

RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}


def get_json(session, url, params=None, timeout=(3, 10), max_retries=5, base_delay=1):
    """
    GET request dengan timeout, retry terbatas, exponential backoff, jitter,
    dan prioritas header Retry-After untuk HTTP 429.
    """
    for attempt in range(1, max_retries + 1):
        try:
            response = session.get(url, params=params, timeout=timeout)

            if response.status_code == 200:
                return response.json()

            if response.status_code not in RETRYABLE_STATUS_CODES:
                response.raise_for_status()

            if attempt == max_retries:
                logger.error("Max retries reached for %s (status=%s)", url, response.status_code)
                response.raise_for_status()

            if response.status_code == 429:
                retry_after = response.headers.get("Retry-After")
                wait_time = float(retry_after) if retry_after else base_delay * (2 ** (attempt - 1))
                logger.warning("Rate limited (429) on attempt %s. Waiting %.2fs", attempt, wait_time)
            else:
                wait_time = base_delay * (2 ** (attempt - 1))
                logger.warning("Temporary error %s on attempt %s. Waiting %.2fs", response.status_code, attempt, wait_time)

            jitter = random.uniform(0, 1)
            time.sleep(wait_time + jitter)

        except requests.exceptions.RequestException as error:
            if attempt == max_retries:
                logger.error("Max retries reached after network error: %s", error)
                raise
            wait_time = base_delay * (2 ** (attempt - 1))
            jitter = random.uniform(0, 1)
            logger.warning("Network error on attempt %s: %s. Waiting %.2fs", attempt, error, wait_time + jitter)
            time.sleep(wait_time + jitter)

    raise RuntimeError("Maximum retries exceeded")