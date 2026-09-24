import os
import requests
from dotenv import load_dotenv

load_dotenv()


class GdeltClient:

  def call(self, country: str = "Pakistan"):
    base_url = os.environ.get(
        "GDELT_BASE_URL", "https://api.gdeltproject.org"
    ).rstrip("/")
    endpoint = f"{base_url}/api/v2/doc/doc"

    params = {
        "query": country,
        "mode": "artlist",
        "format": "json",
        "maxrecords": 50,
    }

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            " (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json",
    }

    response = requests.get(
        endpoint, params=params, headers=headers, timeout=20
    )
    response.raise_for_status()

    text = response.text.strip()
    if not text:
      return {"articles": []}

    return response.json()