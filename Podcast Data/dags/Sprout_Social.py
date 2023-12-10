from airflow import DAG
#from airflow.operators.python import PythonOperator, BashOperator 
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator
from airflow.operators.bash_operator import PythonOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['hamza.ahmed@liquidagency.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 5,
    'retry_delay': timedelta(minutes=2)}