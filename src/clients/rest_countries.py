import requests, os
from dotenv import load_dotenv

load_dotenv()

class RestCountriesClient:
    def call(self, country='canada'):

        base_url = os.environ.get("REST_COUNTRIES_BASE_URL")
        endpoint = f"{base_url}/countries/v5"
        api_key = os.environ.get("REST_COUNTRIES_API_KEY")
        headers = {'Authorization': f'Bearer {api_key}', "Accept": "application/json"}

        response = requests.get(
            endpoint,
            headers=headers,
            params={"q": country},
            timeout=10
        )
        return response.json()

