from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys
import os
sys.path.append(os.path.expanduser('~/siri-ai-quality-engineering/src'))
from ingest import ingest_csv
from transform import transform_data
from quality import check_quality
from deliver import deliver_to_iceberg
from sql_step import run_sql_query
from ml_step import run_ml_pipeline

def run_ingest():
    ingest_csv('/Users/justin/siri-ai-quality-engineering/data/sample.csv')

def run_transform():
    transform_data()

def run_quality():
    check_quality('/Users/justin/siri-ai-quality-engineering/data/sample.csv')

def run_sql():
    run_sql_query('/Users/justin/siri-ai-quality-engineering/data/sample.csv')

def run_ml():
    run_ml_pipeline('/Users/justin/siri-ai-quality-engineering/data/sample.csv')

def run_deliver():
    deliver_to_iceberg()


dag = DAG(
    dag_id='sample_pipeline',
    start_date=datetime(2023, 1, 1),
    schedule=None
)

ingest = PythonOperator(task_id='ingest', python_callable=run_ingest, dag=dag)
transform = PythonOperator(task_id='transform', python_callable=run_transform, dag=dag)
quality = PythonOperator(task_id='quality', python_callable=run_quality, dag=dag)
sql = PythonOperator(task_id='sql', python_callable=run_sql, dag=dag)
ml = PythonOperator(task_id='ml', python_callable=run_ml, dag=dag)
deliver = PythonOperator(task_id='deliver', python_callable=run_deliver, dag=dag)

ingest >> transform >> quality >> sql >> ml >> deliver
