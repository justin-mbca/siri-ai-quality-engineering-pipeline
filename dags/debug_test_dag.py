from airflow import DAG
from airflow.operators.empty import EmptyOperator
from datetime import datetime

with DAG(
    dag_id="debug_test_dag",
    start_date=datetime(2025, 9, 19),
    schedule=None,
    catchup=False,
) as dag:
    t1 = EmptyOperator(task_id="start")
