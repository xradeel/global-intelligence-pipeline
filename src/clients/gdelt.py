import requests, os
from dotenv import load_dotenv

load_dotenv()

class GdeltClient:
    def call(self, country="Pakistan"):

        base_url = os.environ.get("GDELT_BASE_URL")
        endpoint = f"{base_url}/api/v2/doc/doc?query={country}&mode=artlist&format=json"
        

        response = requests.get(
            endpoint
        )
        return response.json()

