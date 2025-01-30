import os
from airflow import DAG

# Get the filename without the .py extension
dag_id = os.path.splitext(os.path.basename(__file__))[0]

with DAG(
    dag_id=dag_id,
    # Other DAG parameters...
) as dag:
    # DAG tasks here
