import functions_framework
import requests
from google.cloud import storage
from google.cloud import bigquery
import json
import csv
from datetime import datetime
import os
import time

api_key = os.environ.get("TENK-API-KEY")

def extract_folder_name(uri):
    # split the path to make it look nice removing 'gs://'
    path_parts = uri.replace('gs://', '').split('/')

    # Find the folder name by removing the bucket name and file name
    folder_name = '/'.join(path_parts[1:-1])
    return folder_name

def upload_to_bigquery(data, dataset_name, table_name):
    bigquery_client = bigquery.Client()
    dataset_ref = bigquery_client.dataset(dataset_name)
    table_ref = dataset_ref.table(table_name)

    # Create the dataset if it doesn't exist
    dataset = bigquery.Dataset(dataset_ref)
    if not bigquery_client.get_dataset(dataset):
        bigquery_client.create_dataset(dataset)

    # Configure the job options
    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE", autodetect=True)

    # Start the load job
    load_job = bigquery_client.load_table_from_json(data, table_ref, job_config=job_config)

    # Wait for the load job to complete
    load_job.result()

    # Check the load job status
    if load_job.errors:
        print('Error loading data into BigQuery:')
        for error in load_job.errors:
            print(error)
    else:
        print('Data uploaded to BigQuery dataset {} in table {}.'.format(dataset_name, table_name))

def upload_to_bucket(data, bucket_name, file_name, dataset_name, table_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Check if any JSONL files already exist in the target folder to move it to the archive folder
    folder_prefix = os.path.dirname(file_name)
    folder_blobs = list(bucket.list_blobs(prefix=folder_prefix))
    existing_files = [blob.name for blob in folder_blobs if blob.name.endswith(".jsonl")]
    #NOTE: We might take off the archive part of this function and instead overwrite the data into the GCS bucket.

    # If there are existing files, create an "Archive" folder 
    if existing_files:
        archive_folder_name = os.path.join(folder_prefix, "Archive/")
        archive_folder = bucket.blob(archive_folder_name)
        archive_folder.upload_from_string("")

        # Move existing files to the Archive folder 
        for existing_file in existing_files:
            existing_blob = bucket.blob(existing_file)
            file_name_without_path = os.path.basename(existing_file)

            # Skip files that already have the "archive_" prefix. Ugh this is important and annoying
            if file_name_without_path.startswith("archive_"):
                continue

            new_file_name = "archive_" + file_name_without_path
            new_location = os.path.join(archive_folder_name, new_file_name)
            bucket.rename_blob(existing_blob, new_location)
            
    # Add metadata fields to each JSON object
    metadata = {
        "data_retrieval_time": datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'
    }
    for item in data:
        item.update(metadata)
    
        # Convert 'id' field to specific field names based on data type
    data_type = table_name.split('_')[1].capitalize()
    id_field_name = f"{data_type}_id"
    for item in data:
        item[id_field_name] = item.pop('id')

    # Upload the new file to the target folder
    blob = bucket.blob(file_name)
    data_str = '\n'.join([json.dumps(item) for item in data])
    blob.upload_from_string(data_str)

    # Upload the data to BigQuery
    upload_to_bigquery(data, dataset_name, table_name)

    print('Data uploaded to bucket {} in file {}. Also uploaded to BigQuery dataset {} in table {}.'.format(
        bucket_name,
        file_name,
        dataset_name,
        table_name))

#API data retrieval function
def get_api_data(url, headers, params):
    data = []
    while True:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        # Throttling limit exceeded, sleep for a duration and retry
        if response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After', '1'))
            print(f"Throttling limit exceeded. Retrying after {retry_after} seconds.")
            time.sleep(retry_after)
            continue

        response_data = response.json()
        data.extend(response_data['data'])
        # Check if there are additional pages in the original pagination
        if 'paging' in response_data:
            paging = response_data['paging']
            if not paging.get('next'):
                break
            params['page'] += 1
            continue
        # Check for additional pages in custom_field_values
        if 'custom_field_values' in response_data.get('paging', {}):
            custom_field_values_paging = response_data['paging']['custom_field_values']
            if custom_field_values_paging.get('next'):
                params['custom_field_values.paging.page'] += 1
                continue

        # Check for additional pages in tags
        if 'tags' in response_data.get('paging', {}):
            tags_paging = response_data['paging']['tags']
            if tags_paging.get('next'):
                params['tags.paging.page'] += 1
                continue

        # Break the loop if there are no more pages
        break
        
    return data


@functions_framework.http
def get_and_upload_api_data(request):
    headers = {
        "Content-Type": "application/json",
        "auth": api_key
    }
    api_data = [
        # Assignables Data API Call
        {
            "url": "https://api.rm.smartsheet.com/api/v1/status_options",
            "bucket_name": "method-incoming",
            "file_name": f"10k/status_options/10k_status_options_data_{datetime.now().strftime('%d%m%Y_%H%M%S')}.jsonl",
            "params": {"per_page": 100, "page": 1},
            "dataset_name": "Landing",
            "table_name": "TenK_status_options"
            
        },
        {
            "url": "https://api.rm.smartsheet.com/api/v1/placeholder_resources",
            "bucket_name": "method-incoming",
            "file_name": f"10k/placeholders/10k_placeholders_data_{datetime.now().strftime('%d%m%Y_%H%M%S')}.jsonl",
            "params": {"per_page": 100, "page": 1, "fields": "custom_field_values"},
            "dataset_name": "Landing",
            "table_name": "TenK_placeholders"
            
        }
    ]
    #Running the look for all the api calls, fetch the data, put them into GCS and then to BigQuery
    for api in api_data:
        #Calling the API
        data = get_api_data(api['url'], headers=headers, params=api['params'])
        #Uploading the data retrieved by the API to the bucket
        upload_to_bucket(data, api['bucket_name'], api['file_name'], api['dataset_name'], api['table_name'])
        #Putting the data into BigQuery
        upload_to_bigquery(data, api['dataset_name'], api['table_name'])
        print("Uploaded data from {} to bucket {} in file {}. Also uploaded to BigQuery dataset {} in table {}.".format(
            api['url'], api['bucket_name'], api['file_name'], api['dataset_name'], api['table_name']))
    return "Data uploaded successfully!"