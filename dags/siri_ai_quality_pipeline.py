from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

import sys
sys.path.append('/opt/airflow/src')
from ingest import ingest_csv
from transform import transform_data
from quality import check_quality
from deliver import deliver_to_iceberg
from sql_step import run_sql_query
from ml_step import run_ml_pipeline

def run_ingest():
    ingest_csv('/opt/airflow/data/siri_simulated_interactions_small.csv')

def run_transform():
    transform_data('/opt/airflow/data/siri_simulated_interactions_small.csv')

def run_quality():
    check_quality('/opt/airflow/data/siri_simulated_interactions_small.csv')

def run_sql():
    run_sql_query('/opt/airflow/data/siri_simulated_interactions_small.csv')

def run_ml():
    run_ml_pipeline('/opt/airflow/data/siri_simulated_interactions_small.csv')

def run_deliver():
    deliver_to_iceberg('/opt/airflow/data/siri_simulated_interactions_small.csv')

dag = DAG(
    dag_id="siri_ai_quality_pipeline",
    start_date=datetime(2025, 9, 19),
    schedule=None,
    catchup=False,
)

ingest = PythonOperator(task_id='ingest', python_callable=run_ingest, dag=dag)
transform = PythonOperator(task_id='transform', python_callable=run_transform, dag=dag)
quality = PythonOperator(task_id='quality', python_callable=run_quality, dag=dag)
sql = PythonOperator(task_id='sql', python_callable=run_sql, dag=dag)
ml = PythonOperator(task_id='ml', python_callable=run_ml, dag=dag)
deliver = PythonOperator(task_id='deliver', python_callable=run_deliver, dag=dag)

ingest >> transform >> quality >> sql >> ml >> deliver
