from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.models import DagRun, TaskInstance
from datetime import datetime, timedelta
import time
import random

# Function to create a DAG with a specified schedule interval
def create_dag(dag_id, schedule_interval, default_args):
    with DAG(dag_id, schedule_interval=schedule_interval, default_args=default_args) as dag:
        start_task = DummyOperator(task_id='start_task')
        
        # Create a dynamic delay task
        def dynamic_delay_task():
            delay = random.randint(5, 15)  # Random delay between 5 and 15 seconds
            print(f"Task {dag_id} is sleeping for {delay} seconds")
            time.sleep(delay)
        
        delay_task = PythonOperator(
            task_id='delay_task',
            python_callable=dynamic_delay_task,
            provide_context=True,
        )
        
        end_task = DummyOperator(task_id='end_task')

        start_task >> delay_task >> end_task
    return dag

# Function to check the status of a task in a DAG
def check_dag_status(dag_id, task_id, **kwargs):
    # Get the latest DagRun for the specified DAG
    dag_runs = DagRun.find(dag_id=dag_id)
    if not dag_runs:
        raise ValueError(f"No runs found for DAG {dag_id}")

    latest_dag_run = dag_runs[-1]
    task_instances = latest_dag_run.get_task_instances()

    for ti in task_instances:
        if ti.task_id == task_id:
            if ti.state == 'success':
                return True
            elif ti.state in ['failed', 'upstream_failed']:
                raise ValueError(f"Task {task_id} in DAG {dag_id} failed")
            else:
                return False

    return False

# Default arguments for all DAGs
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# List of DAG IDs and their corresponding schedule intervals
dag_configs = [
    ('dag_1', '@daily'),
    ('dag_2', '@hourly'),
    ('dag_3', '0 0 * * 1-5'),  # Every weekday at midnight
    ('dag_4', '0 12 * * *'),   # Every day at noon
    ('dag_5', '0 0 * * 0'),    # Every Sunday at midnight
    ('dag_6', '0 6 * * *'),    # Every day at 6 AM
    ('dag_7', '0 18 * * *'),   # Every day at 6 PM
    ('dag_8', '0 0 * * 1'),    # Every Monday at midnight
    ('dag_9', '0 0 * * 3'),    # Every Wednesday at midnight
    ('dag_10', '0 0 * * 5'),   # Every Friday at midnight
]

# Create the DAGs dynamically
dags = {dag_id: create_dag(dag_id, schedule_interval, default_args) for dag_id, schedule_interval in dag_configs}

# Monitoring DAG
with DAG('monitoring_dag', default_args=default_args, schedule_interval='@daily') as monitoring_dag:
    start_task = DummyOperator(task_id='start_task')

    # Create a PythonOperator for each DAG to be monitored
    for dag_id, _ in dag_configs:
        check_status_task = PythonOperator(
            task_id=f'check_status_{dag_id}',
            python_callable=check_dag_status,
            op_kwargs={
                'dag_id': dag_id,
                'task_id': 'end_task',
            },
            provide_context=True,
        )

        start_task >> check_status_task

    end_task = DummyOperator(task_id='end_task')

    # Ensure all check_status tasks are completed before the end_task
    for dag_id, _ in dag_configs:
        check_status_task = monitoring_dag.get_task(f'check_status_{dag_id}')
        check_status_task >> end_task

# Register the dynamically created DAGs
for dag in dags.values():
    globals()[dag.dag_id] = dag

# Register the monitoring DAG
globals()['monitoring_dag'] = monitoring_dag
