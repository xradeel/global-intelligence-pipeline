from datetime import datetime
from airflow.sdk import dag, task

from src.clients.rest_countries import RestCountriesClient
from src.clients.open_meteo import OpenMeteoClient
from src.clients.world_bank import WorldBankClient
from src.utils.save_raw_data import SaveRawData


save_res = SaveRawData()

@dag(
    dag_id="global_intelligence",
    start_date=datetime(2026, 9, 23),
    schedule=None,
    catchup=False
)
def global_intelligence():

    @task
    def fetch_countries(country='pakistan'):
        client = RestCountriesClient()
        res = client.call(country)
        current_date = datetime.now().strftime("%Y-%m-%d")
        path = f'data/raw/countries/{current_date}.json'

        save_res.json(res, path)
        return path

    @task
    def fetch_weather(latitude=31.5204, longitude=74.3587):
        client = OpenMeteoClient()
        res = client.call(latitude, longitude)
        current_date = datetime.now().strftime("%Y-%m-%d")
        path = f'data/raw/weather/{current_date}.json'

        save_res.json(res, path)
        return path

    @task
    def fetch_world_economics(country_code="PAK"):
        client = WorldBankClient()
        res = client.call(country_code)
        current_date = datetime.now().strftime("%Y-%m-%d")
        path = f'data/raw/worldbank/{current_date}.json'

        save_res.json(res, path)
        return path
    


    country = fetch_countries('canada')
    weather = fetch_weather()
    economics = fetch_world_economics()

global_intelligence()