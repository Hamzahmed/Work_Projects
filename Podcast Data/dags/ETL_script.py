from airflow import DAG
#from airflow.operators.python import PythonOperator, BashOperator 
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@airflow.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)}

with DAG("ETL_script",
        description= "DAG for Data retrieval",
        default_args = default_args,
        start_date= datetime(2022, 1, 1),
        schedule_interval= "@weekly", 
        catchup = False
        ) as dag:
    t1 = BashOperator(
            task_id = 'extract_data',
            bash_command = '/Users/hamza.ahmed/Coding Projects/Python_Apps/Docker_Applications/Airflow_Docker_Apps/Python_Scripts/API_extract.py',
            dag=dag,)
    
    t2 = BashOperator(
        task_id = "Insert_into_google_Sheets",
        bash_command = 'python3 "/Users/hamza.ahmed/Coding Projects/Python_Apps/Docker_Applications/Airflow_Docker_Apps/Python_Scripts/Google_Sheets_Connection.py"',
        dag=dag,)
    
    t1 >> t2 # Defining the task dependencies