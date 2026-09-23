import requests, os
from dotenv import load_dotenv

load_dotenv()

class WorldBankClient:
    def call(self, country_code="PAK"):

        base_url = os.environ.get("WORLD_BANK_BASE_URL")
        endpoint = f"{base_url}/v2/country/{country_code}/indicator/NY.GDP.MKTP.CD?format=json"
        

        response = requests.get(
            endpoint
        )
        return response.json()

