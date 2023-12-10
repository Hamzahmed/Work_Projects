from pyspark.context import SparkContext
from pyspark.sql import functions as f
from pyspark.sql import SQLContext
from pyspark.sql import SparkSession
from google.cloud import bigquery
from google.cloud import secretmanager
import datetime as dt
import pyodbc
import json
import pandas as pd
from requests import get
pd.set_option("display.max_rows", None, "display.max_columns", None)

def full_load():

    client = secretmanager.SecretManagerServiceClient()
    name = "projects/1071833499542/secrets/Eagle-Database/versions/latest"
    response = client.access_secret_version(name=name)
    secret_value_sql_server = json.loads(response.payload.data.decode("UTF-8"))



    gcp_connection = json.load(open('gcp-connection.json'))
    project_id = gcp_connection['project_id']
    cnxn_str =(
        f"DRIVER={{{secret_value_sql_server['DRIVER']}}};"
        f"SERVER={{{secret_value_sql_server['SERVER']}}};"
        "PORT=1433;"
        f"DATABASE={{{secret_value_sql_server['DATABASE']}}};"
        f"UID={{{secret_value_sql_server['UID']}}};"
        f"PWD={{{secret_value_sql_server['PWD']}}};"
    )
    # print(cnxn_str)
    cnxn = pyodbc.connect(cnxn_str)
    bigquery_client =  bigquery.Client(project=project_id)
    dataset_ref = bigquery_client.dataset('Landing')


    Schema = 'Finance'
    Table = 'Project'
    query = """select * from """ + Schema + "." + Table + ";"


    df = pd.read_sql(query,cnxn)


    df.insert(0, 'TransferID', range(202301, 202301 + len(df)))
    df['updated_at'] = dt.datetime.now()
    df['CurrentVersion'] = 0
    df['OperationFlag'] = 'Initial Load'

    table = f'{project_id}.Landing.Eagle'+'_'+Table
    delete_existing_table = bigquery_client.delete_table(table)
    job = bigquery_client.load_table_from_dataframe(df, table)



if __name__ == "__main__":
    full_load()
