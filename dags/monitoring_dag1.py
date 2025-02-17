from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.sensors.external_task_sensor import ExternalTaskSensor
from airflow.models import DagRun, TaskInstance
from datetime import datetime, timedelta
import time
import random
import logging

# Function to create a DAG with a specified schedule interval and dynamic delay
def create_dag(dag_id, schedule_interval, default_args):
    with DAG(dag_id, schedule_interval=schedule_interval, default_args=default_args) as dag:
        start_task = DummyOperator(task_id='start_task')
        
        # Create a dynamic delay task
        def dynamic_delay_task():
            delay = random.randint(5, 15)  # Random delay between 5 and 15 seconds
            logging.info(f"Task {dag_id} is sleeping for {delay} seconds")
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
                logging.info(f"Task {task_id} in DAG {dag_id} completed successfully")
                return True
            elif ti.state in ['failed', 'upstream_failed']:
                logging.error(f"Task {task_id} in DAG {dag_id} failed")
                raise ValueError(f"Task {task_id} in DAG {dag_id} failed")
            else:
                logging.info(f"Task {task_id} in DAG {dag_id} is still running")
                return False

    return False

# Default arguments for all DAGs
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# List of DAG IDs, their corresponding schedule intervals, and poke intervals
dag_configs = [
    ('dag_1', '@daily', 60),  # 60 seconds
    ('dag_2', '@hourly', 30),  # 30 seconds
    ('dag_3', '0 0 * * 1-5', 45),  # Every weekday at midnight, 45 seconds
    ('dag_4', '0 12 * * *', 15),  # Every day at noon, 15 seconds
    ('dag_5', '0 0 * * 0', 20),  # Every Sunday at midnight, 20 seconds
    ('dag_6', '0 6 * * *', 10),  # Every day at 6 AM, 10 seconds
    ('dag_7', '0 18 * * *', 25),  # Every day at 6 PM, 25 seconds
    ('dag_8', '0 0 * * 1', 35),  # Every Monday at midnight, 35 seconds
    ('dag_9', '0 0 * * 3', 50),  # Every Wednesday at midnight, 50 seconds
    ('dag_10', '0 0 * * 5', 100),  # Every Friday at midnight, 100 seconds
]

# Create the DAGs dynamically
dags = {dag_id: create_dag(dag_id, schedule_interval, default_args) for dag_id, schedule_interval, _ in dag_configs}

# Monitoring DAG
with DAG('monitoring_dag', default_args=default_args, schedule_interval='@daily') as monitoring_dag:
    start_task = DummyOperator(task_id='start_task')

    # Create a PythonOperator for each DAG to be monitored
    for dag_id, _, poke_interval in dag_configs:
        check_status_task = ExternalTaskSensor(
            task_id=f'check_status_{dag_id}',
            external_dag_id=dag_id,
            external_task_id='end_task',
            mode='reschedule',  # Use 'reschedule' to avoid blocking the worker
            timeout=3600,  # Timeout after 1 hour
            poke_interval=poke_interval,  # Dynamic poke interval
            provide_context=True,
        )

        start_task >> check_status_task

    end_task = DummyOperator(task_id='end_task')

    # Ensure all check_status tasks are completed before the end_task
    for dag_id, _, _ in dag_configs:
        check_status_task = monitoring_dag.get_task(f'check_status_{dag_id}')
        check_status_task >> end_task

# Register the dynamically created DAGs
for dag in dags.values():
    globals()[dag.dag_id] = dag

# Register the monitoring DAG
globals()['monitoring_dag'] = monitoring_dag
