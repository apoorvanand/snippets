from airflow import DAG
from airflow.providers.ssh.operators.ssh import SSHOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 5, 27),
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    dag_id='remote_bash_script_execution',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    tags=['example'],
) as dag:

    execute_remote_script = SSHOperator(
        task_id='run_remote_script',
        ssh_conn_id='ssh_remote_host',  # defined in Airflow connections
        command='/path/to/your/script.sh',  # remote script path
        dag=dag
    )

    execute_remote_script
