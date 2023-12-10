import functions_framework
import os
from google.cloud import storage
from google.cloud import bigquery
from flask import request

gs = storage.Client()
bucket_name = 'data-warehouse-tables-transformations'
path = os.path.join('RAW_TO_REFINED_SQL','RAW_TO_REFINED_query_names.txt')
bucket = gs.get_bucket(bucket_name)
blob = bucket.blob(path)
bytes = blob.download_as_bytes()
content = bytes.decode('utf-8')
query_names = content.split(',\n')
print('Executing Queries:')
print(query_names)

def run_query(query_name,dataset_name = None):
    bq_client = bigquery.Client(project = 'methodologysandbox')
    gs = storage.Client()
    path = os.path.join('RAW_TO_REFINED_SQL', f'{query_name}.sql')
    bucket_name = 'data-warehouse-tables-transformations'
    bucket = gs.get_bucket(bucket_name)
    blob = bucket.blob(path)
    query_bytes = blob.download_as_bytes()
    query_content = query_bytes.decode('utf-8')
    query_job = bq_client.query(query_content)  # API request
    rows = query_job.result()  # Waits for query to finish
    for row in rows:
        print(row.name)
    return rows

def run_raw_to_refined(request):
    data = request.get_json()  # JSON data
    print(data)
    for query in query_names:
        print(f'{query} began')
        try:
            run_query(query)
            print(f'{query} completed')
        except:
            print(f'{query} failed')

    return "Raw to refined queries completed"