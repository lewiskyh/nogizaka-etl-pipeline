from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from scripts.fetch_data import fetch_data
from scripts.transform_data import transform_data
from scripts.load_data import load_data

# The default_args dictionary defines the default parameters for the tasks in the DAG.
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2024, 12, 31),
    'retries': 1,
    'schedule_interval': '@monthly',
}
# DAG Object
dag = DAG(
    'nogizaka46_etl',
    default_args=default_args,
    description='ETL pipeline for Nogizaka46 data',
)
# define a task that runs the fetch_data function (in scripts folder)
fetch_task = PythonOperator(
    task_id='fetch_data',
    python_callable=fetch_data,
    dag=dag,
)
# define a task that runs the transform_data function (in scripts folder)
transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    dag=dag,
)
# define a task that runs the load_data function (in scripts folder)
load_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    dag=dag,
)

fetch_task >> transform_task >> load_task