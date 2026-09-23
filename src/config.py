"""Configuration module for Taiwan Weather Map (HW1).

Loads environment variables from .env and exposes project settings.
"""

from __future__ import annotations

import os
from pathlib import Path
from dotenv import load_dotenv

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Load .env file from project root if it exists
ENV_PATH = PROJECT_ROOT / ".env"
if ENV_PATH.exists():
    load_dotenv(dotenv_path=ENV_PATH)

CWA_API_BASE_URL = "https://opendata.cwa.gov.tw/api"
HW1_DATASET_ID = "F-A0010-001"

HW1_REGIONS = [
    "北部地區",
    "中部地區",
    "南部地區",
    "東北部地區",
    "東部地區",
    "東南部地區",
]


def get_cwa_api_key() -> str:
    """Retrieve CWA API Key from environment variables safely.

    Raises:
        ValueError: If CWA_API_KEY is not set or empty.
    """
    key = os.getenv("CWA_API_KEY", "").strip()
    if not key or key == "your_api_key_here":
        raise ValueError(
            "CWA_API_KEY is missing or invalid. Please configure your actual API key in .env file."
        )
    return key
