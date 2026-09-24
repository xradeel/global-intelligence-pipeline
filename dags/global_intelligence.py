from datetime import datetime, timedelta
from airflow.sdk import dag, task

from src.clients.rest_countries import RestCountriesClient
from src.clients.open_meteo import OpenMeteoClient
from src.clients.world_bank import WorldBankClient
from src.clients.gdelt import GdeltClient

from src.validations.response import validate_json_list_file
from src.transformations.countries import TransformCountries
from src.transformations.news import TransformNews
from src.transformations.weather import TransformWeather
from src.transformations.worldbank import TransformWorldBank
from src.loaders.warehouse import WarehouseLoader
from src.utils.save_data import SaveRawData


@dag(
    dag_id="global_intelligence",
    start_date=datetime(2026, 9, 23),
    schedule=None,
    catchup=False,
)
def global_intelligence():
    save_res = SaveRawData()
    loader = WarehouseLoader()

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
    def validate_responses(country_path, weather_path, economics_path, news_path):
        validations = {
            "country": validate_json_list_file(country_path),
            "weather": validate_json_list_file(weather_path),
            "economics": validate_json_list_file(economics_path),
            "news": validate_json_list_file(news_path),
        }

        failed_checks = [
            k for k, v in validations.items() if not v[0]
        ]
        if failed_checks:
            raise ValueError(f"Validation failed for datasets: {failed_checks}")

        return validations

    # Transformations

    @task
    def transform_country(raw_path: str) -> str:
        transformed_data = TransformCountries().transform_country_file(raw_path)
        processed_path = raw_path.replace("data/raw/", "data/processed/")

        save_res.json(transformed_data, processed_path)
        return processed_path

    @task
    def transform_weather(raw_path: str) -> str:
        transformed_data = TransformWeather().transform_weather_file(raw_path)
        processed_path = raw_path.replace("data/raw/", "data/processed/")

        save_res.json(transformed_data, processed_path)
        return processed_path

    @task
    def transform_economics(raw_path: str) -> str:
        transformed_data = TransformWorldBank().transform_world_bank_file(raw_path)
        processed_path = raw_path.replace("data/raw/", "data/processed/")

        save_res.json(transformed_data, processed_path)
        return processed_path

    @task
    def transform_news(raw_path: str) -> str:
        transformed_data = TransformNews().transform_gdelt_file(raw_path)
        processed_path = raw_path.replace("data/raw/", "data/processed/")

        save_res.json(transformed_data, processed_path)
        return processed_path

    # Loaders

    @task
    def load_country(processed_path: str):
        return loader.load_country(processed_path)

    @task
    def load_weather(processed_path: str, country_code="PAK"):
        return loader.load_weather(processed_path, country_code=country_code)

    @task
    def load_economics(processed_path: str):
        return loader.load_economics(processed_path)

    @task
    def load_news(processed_path: str, country_code="PAK"):
        return loader.load_news(processed_path, target_country_code=country_code)

    # Fetch tasks
    country_raw = fetch_countries("canada")
    weather_raw = fetch_weather()
    economics_raw = fetch_world_economics("PAK")
    news_raw = fetch_news("France")

    is_valid = validate_responses(
        country_raw, weather_raw, economics_raw, news_raw
    )

    # Transform tasks
    country_processed = transform_country(country_raw)
    weather_processed = transform_weather(weather_raw)
    economics_processed = transform_economics(economics_raw)
    news_processed = transform_news(news_raw)

    is_valid >> [
        country_processed,
        weather_processed,
        economics_processed,
        news_processed,
    ]

    # Load tasks
    load_country(country_processed)
    load_weather(weather_processed)
    load_economics(economics_processed)
    load_news(news_processed)


global_intelligence()