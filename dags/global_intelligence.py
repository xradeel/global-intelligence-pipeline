from datetime import datetime
from airflow.sdk import dag, task


@dag(
    dag_id="global_intelligence",
    start_date=datetime(2026, 9, 23),
    schedule=None,
    catchup=False
)
def global_intelligence():

    @task
    def aoa():
        print('aoa bro, its working')

    aoa()

global_intelligence()