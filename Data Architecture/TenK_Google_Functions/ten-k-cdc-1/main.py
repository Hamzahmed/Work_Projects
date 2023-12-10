from google.cloud import bigquery
import base64
import os
import json

# Initialize BigQuery client
client = bigquery.Client()

# Define the project ID
project_id = os.environ.get("project_id")

def retrieve_existing_data(dataset, table_name):
    table_ref = client.dataset(dataset).table(table_name)
    table = client.get_table(table_ref)
    query = f"SELECT * FROM `{table.project}.{table.dataset_id}.{table.table_id}`"
    query_job = client.query(query)

    results = query_job.result()
    existing_data = {}

    for row in results:
        row_data = dict(row)
        existing_data[row_data['id']] = row_data

    return existing_data

def transform_cdc_data(cdc_data, table_name):
    transformed_data = {}
    existing_data = retrieve_existing_data('Landing', table_name)

    # Extract the tables from Landing
    if table_name == 'TenK-Assignables':
        transformed_data['id'] = cdc_data['id']
        transformed_data['name'] = cdc_data['name']
        transformed_data['status'] = cdc_data['status']
        transformed_data['data_retrieval_time'] = cdc_data['data_retrieval_time']
        transformed_data['created_at'] = cdc_data['created_at']
        transformed_data['updated_at'] = cdc_data['updated_at']
        transformed_data['is_updated'] = cdc_data['updated_at'] > cdc_data['data_retrieval_time']
        transformed_data['is_created'] = cdc_data['created_at'] > cdc_data['data_retrieval_time']
        transformed_data['is_deleted'] = cdc_data['status'] == 'deleted'

    
    if table_name == 'TenK-Assignments':
        transformed_data['id'] = cdc_data['id']
        transformed_data['name'] = cdc_data['name']
        transformed_data['status'] = cdc_data['status']
        transformed_data['data_retrieval_time'] = cdc_data['data_retrieval_time']
        transformed_data['created_at'] = cdc_data['created_at']
        transformed_data['updated_at'] = cdc_data['updated_at']
        transformed_data['is_updated'] = cdc_data['updated_at'] > cdc_data['data_retrieval_time']
        transformed_data['is_created'] = cdc_data['created_at'] > cdc_data['data_retrieval_time']


    if table_name == 'TenK-Projects':
        transformed_data['id'] = cdc_data['id']
        transformed_data['name'] = cdc_data['name']
        transformed_data['status'] = cdc_data['status']
        transformed_data['data_retrieval_time'] = cdc_data['data_retrieval_time']
        transformed_data['created_at'] = cdc_data['created_at']
        transformed_data['updated_at'] = cdc_data['updated_at']
        transformed_data['is_updated'] = cdc_data['updated_at'] > cdc_data['data_retrieval_time']
        transformed_data['is_created'] = cdc_data['created_at'] > cdc_data['data_retrieval_time']


    if table_name == 'TenK-Users':
        transformed_data['id'] = cdc_data['id']
        transformed_data['first_name'] = cdc_data['first_name']
        transformed_data['last_name'] = cdc_data['last_name']
        transformed_data['data_retrieval_time'] = cdc_data['data_retrieval_time']
        transformed_data['created_at'] = cdc_data['created_at']
        transformed_data['updated_at'] = cdc_data['updated_at']
        transformed_data['is_updated'] = cdc_data['updated_at'] > cdc_data['data_retrieval_time']
        transformed_data['is_created'] = cdc_data['created_at'] > cdc_data['data_retrieval_time']

    if transformed_data['id'] in existing_data:
        existing_row = existing_data[transformed_data['id']]
        if existing_row != transformed_data:
            identify_changes(existing_row, transformed_data)
    else:
        handle_new_row(transformed_data, table_name)

    return transformed_data

def identify_changes(existing_row, incoming_row):
    changed_fields = []
    
    for field in existing_row:
        if existing_row[field] != incoming_row[field]:
            changed_fields.append(field)
    
    if changed_fields:
        print(f"Changes identified in row: {existing_row['id']}")
        print(f"Changed fields: {changed_fields}")
    else:
        print(f"No changes identified in row: {existing_row['id']}")

def handle_new_row(new_row, table_name):
    print("Handling new row:", new_row)
    
    existing_data = retrieve_existing_data('Landing', table_name)
    
    if new_row['id'] in existing_data:
        existing_row = existing_data[new_row['id']]
        identify_changes(existing_row, new_row)
    else:
        print("New row handled:", new_row['id'])


def insert_into_bigquery(data, dataset, table_id):
    table_ref = client.dataset(dataset).table(table_id)
    errors = client.insert_rows_json(table_ref, [data])

    if errors:
        raise Exception(f"Error inserting rows into BigQuery table: {errors}")

def process_cdc(data, context):
    # Parse the request payload as JSON
    request_json = data
    if not request_json:
        return 'Invalid request', 400

    # Get the table name from the request JSON
    table_name = request_json.get('tableName', '')
    
    # Determine the dataset based on the table name
    source_dataset = 'Landing'  
    destination_dataset = 'RAW'  
    
    # Determine the table ID based on the table name
    table_id = None
    if table_name == 'TenK-Assignables':
        table_id = 'TenK-Assignables'
    elif table_name == 'TenK-Projects':
        table_id = 'TenK-Projects'
    elif table_name == 'TenK-Users':
        table_id = 'TenK-Users'
    elif table_name == 'TenK-Assignments':
        table_id = 'TenK-Assignments'
    
    # If the table ID is found, proceed with CDC
    if table_id:
        # Construct the BigQuery source and destination tables
        source_table = f'{project_id}.{source_dataset}.{table_name}'
        destination_table = f'{project_id}.{destination_dataset}.{table_id}'
        
        # Extract the CDC data from the request JSON
        data = base64.b64decode(request_json['data']).decode('utf-8')
        cdc_data = json.loads(data)
        
        # Transform and process the CDC data as needed
        processed_data = transform_cdc_data(cdc_data, table_name)
        
        # Insert the processed data into the BigQuery table
        insert_into_bigquery(processed_data, destination_dataset, table_id)
