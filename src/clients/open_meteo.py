import requests, os
from dotenv import load_dotenv

load_dotenv()

class OpenMeteoClient:
    def call(self, latitude=31.5204, longitude=74.3587):

        base_url = os.environ.get("OPEN_METEO_BASE_URL")
        endpoint = f"{base_url}/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m%2Crelative_humidity_2m%2Cwind_speed_10m&timezone=auto"
        api_key = os.environ.get("REST_COUNTRIES_API_KEY")

        response = requests.get(
            endpoint
        )
        return response.json()

