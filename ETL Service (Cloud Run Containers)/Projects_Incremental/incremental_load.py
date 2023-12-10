
from pyspark.context import SparkContext
from pyspark.sql import functions as f
from pyspark.sql import SQLContext
from pyspark.sql import SparkSession
from google.cloud import bigquery
from google.cloud import secretmanager
import json
import datetime as dt
import pyodbc
import pandas as pd
pd.set_option("display.max_rows", None, "display.max_columns", None)

def incremental_load():
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
    bigquery_query = f'SELECT max(TransferID) FROM `sandbox.Landing.Eagle_{Table}`;'


    job_config = bigquery.QueryJobConfig()
    job = bigquery_client.query(bigquery_query).result()
    max_row = [row[0] for row in job][0]

    max_row = max_row + 1

    # query = """select * from """ + Schema + "." + Table + ";"

    query = """SELECT P.*,CT.SYS_CHANGE_OPERATION AS OperationFlag
    FROM [Finance].[Project] AS P
    INNER JOIN CHANGETABLE(CHANGES [Finance].[Project], 0) AS CT
    ON P.ProjectId = CT.ProjectId;"""


    df = pd.read_sql(query,cnxn)

    df.insert(0, 'TransferID', range(max_row, max_row + len(df)))
    df['updated_at'] = dt.datetime.now()


    # Append the DataFrame to the BigQuery table
    job_config = bigquery.LoadJobConfig()
    job_config.write_disposition = 'WRITE_APPEND'
    job = bigquery_client.load_table_from_dataframe(df, f'sandbox.Landing.Eagle_{Table}', job_config=job_config)
    job.result()  # Wait for the job to complete


    table = f'{project_id}.Landing.Eagle'+'_'+Table
    job = bigquery_client.load_table_from_dataframe(df, table)
    total_rows = len(df)
    return total_rows
if __name__ == "__main__":
    incremental_load()