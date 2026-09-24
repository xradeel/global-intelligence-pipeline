from datetime import datetime, timedelta
from airflow.sdk import dag, task

from src.clients.rest_countries import RestCountriesClient
from src.clients.open_meteo import OpenMeteoClient
from src.clients.world_bank import WorldBankClient
from src.clients.gdelt import GdeltClient

from src.validation.response import validate_json_list_file
from src.utils.save_raw_data import SaveRawData


@dag(
    dag_id="global_intelligence",
    start_date=datetime(2026, 9, 23),
    schedule=None,
    catchup=False,
)
def global_intelligence():
    save_res = SaveRawData()

    @task
    def fetch_countries(country="pakistan"):
        client = RestCountriesClient()
        res = client.call(country)
        current_date = datetime.now().strftime("%Y-%m-%d")
        path = f"data/raw/countries/{current_date}.json"

        save_res.json(res, path)
        return path

    @task
    def fetch_weather(latitude=31.5204, longitude=74.3587):
        client = OpenMeteoClient()
        res = client.call(latitude, longitude)
        current_date = datetime.now().strftime("%Y-%m-%d")
        path = f"data/raw/weather/{current_date}.json"

        save_res.json(res, path)
        return path

    @task
    def fetch_world_economics(country_code="PAK"):
        client = WorldBankClient()
        res = client.call(country_code)
        current_date = datetime.now().strftime("%Y-%m-%d")
        path = f"data/raw/worldbank/{current_date}.json"

        save_res.json(res, path)
        return path

    @task(
        retries=3,
        retry_delay=timedelta(seconds=15),
        retry_exponential_backoff=True,
        max_retry_delay=timedelta(minutes=2),
    )
    def fetch_news(country="Pakistan"):
        client = GdeltClient()
        res = client.call(country)
        current_date = datetime.now().strftime("%Y-%m-%d")
        path = f"data/raw/news/{current_date}.json"

        save_res.json(res, path)
        return path

    @task
    def validate_responses(
        country_path: str, weather_path: str, economics_path: str, news_path: str
    ):
        return {
            "country": validate_json_list_file(country_path),
            "weather": validate_json_list_file(weather_path),
            "economics": validate_json_list_file(economics_path),
            "news": validate_json_list_file(news_path),
        }

    # Fetch tasks
    country = fetch_countries("canada")
    weather = fetch_weather()
    economics = fetch_world_economics()
    news = fetch_news()

    # TaskFlow automatically configures the 4 fetch tasks as upstream of validate_responses
    validate_responses(country, weather, economics, news)


global_intelligence()