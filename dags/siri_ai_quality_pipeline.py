from airflow import DAG
from airflow.operators.empty import EmptyOperator
from datetime import datetime

with DAG(
    dag_id="siri_ai_quality_pipeline",
    start_date=datetime(2025, 9, 19),
    schedule=None,
    catchup=False,
) as dag:
    t1 = EmptyOperator(task_id="start")
