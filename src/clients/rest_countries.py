import requests, os
from dotenv import load_dotenv

load_dotenv()

class RestCountriesClient:
    def call(country='canada'):

        base_url = os.environ.get("REST_COUNTRIES_BASE_URL")
        endpoint = f"{base_url}/countries/v5?q={country}"
        api_key = os.environ.get("REST_COUNTRIES_API_KEY")

        response = requests.get(
            endpoint,
            headers={'Authorization': f'Bearer {api_key}'}
        )
        print(response.json())
        return



RestCountriesClient.call("pakistan")