from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime


default_args = {
    "owner": "airflow",
    "start_date": datetime(2025, 9, 15),
    "retries": 1,
}

with DAG(
    dag_id="simple_etl",
    default_args=default_args,
    schedule="@daily",
    catchup=False,
    tags="etl"
) as dag:

    extract = BashOperator(
        task_id="extract",
        bash_command="python3 src/extract.py"
    )

    transform = BashOperator(
        task_id="transform",
        bash_command="python3 src/transform.py"
    )

    load = BashOperator(
        task_id="load",
        bash_command="python3 src/load.py"
    )

    analyze = BashOperator(
        task_id="analyze",
        bash_command="python3 src/analytics.py"
    )

    extract >> transform >> load >> analyze