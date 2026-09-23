"""CWA Open Data API Client for Taiwan Weather Map (HW1).

Handles HTTP requests to the CWA Open Data API.
Parsing logic is intentionally kept separate (see parser.py).

HW1-1 scope: F-A0010-001 六大區域一週天氣預報
"""

from __future__ import annotations

import json
import requests
from typing import Any

from src.config import CWA_API_BASE_URL, HW1_DATASET_ID, get_cwa_api_key

# Request timeout (seconds)
_CONNECT_TIMEOUT = 10
_READ_TIMEOUT = 30


class CWAAPIError(Exception):
    """Raised when a CWA API call fails with a known HTTP error."""

    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        super().__init__(f"HTTP {status_code}: {message}")


def fetch_HW1_forecast() -> dict[str, Any]:
    """Fetch F-A0010-001 六大區域一週天氣預報 from CWA Open Data API.

    Returns:
        Parsed JSON response as a Python dict.

    Raises:
        ValueError: If CWA_API_KEY is not configured.
        CWAAPIError: If the server returns a non-200 HTTP status code.
        requests.exceptions.ConnectionError: On network connectivity issues.
        requests.exceptions.Timeout: If the request exceeds the timeout limit.
        json.JSONDecodeError: If the response body is not valid JSON.
    """
    api_key = get_cwa_api_key()  # Raises ValueError if not set

    url = f"{CWA_API_BASE_URL}/v1/rest/datastore/{HW1_DATASET_ID}"
    params = {
        "Authorization": api_key,
        "format": "JSON",
    }

    # NOTE: api_key is in params dict only — never logged or printed.
    print(f"[INFO] Fetching {HW1_DATASET_ID} from CWA Open Data API ...")
    print(f"[INFO] Endpoint: {url}")

    try:
        response = requests.get(
            url,
            params=params,
            timeout=(_CONNECT_TIMEOUT, _READ_TIMEOUT),
        )
    except requests.exceptions.ConnectionError as exc:
        raise requests.exceptions.ConnectionError(
            f"[ERROR] Cannot connect to CWA API. Check your internet connection. ({exc})"
        ) from exc
    except requests.exceptions.Timeout as exc:
        raise requests.exceptions.Timeout(
            f"[ERROR] Request timed out after {_READ_TIMEOUT}s. CWA server may be slow."
        ) from exc

    print(f"[INFO] HTTP Status: {response.status_code}")

    # Handle known HTTP error codes with descriptive messages
    _handle_http_errors(response)

    # Parse JSON — do NOT assume structure; return raw dict for observation
    try:
        data = response.json()
    except (json.JSONDecodeError, ValueError) as exc:
        raise json.JSONDecodeError(
            f"[ERROR] Response body is not valid JSON. Raw preview (first 500 chars):\n"
            f"{response.text[:500]}",
            doc=response.text,
            pos=0,
        ) from exc

    if not data:
        raise ValueError("[ERROR] Received an empty JSON response from CWA API.")

    return data


def _handle_http_errors(response: requests.Response) -> None:
    """Check HTTP status code and raise CWAAPIError with safe diagnostics.

    NOTE: Never logs the Authorization key or full URL with credentials.
    """
    code = response.status_code

    if code == 200:
        return

    # Safe diagnostic: show first 300 chars of body (no credentials)
    body_preview = response.text[:300] if response.text else "(empty body)"

    error_map = {
        400: "Bad Request — invalid request parameters.",
        401: "Unauthorized — CWA_API_KEY may be invalid or expired.",
        403: "Forbidden — access denied for this dataset or API key.",
        404: "Not Found — dataset ID may be incorrect.",
        429: "Too Many Requests — rate limit reached. Please wait before retrying.",
        500: "Internal Server Error — CWA server-side issue.",
        503: "Service Unavailable — CWA API may be temporarily down.",
    }

    description = error_map.get(code, f"Unexpected HTTP error.")
    raise CWAAPIError(
        status_code=code,
        message=f"{description}\nResponse body preview: {body_preview}",
    )
