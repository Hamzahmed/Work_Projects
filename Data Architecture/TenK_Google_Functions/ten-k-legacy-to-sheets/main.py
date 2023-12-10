import os
import json
import google.auth
import functions_framework
from google.oauth2 import service_account
from googleapiclient import discovery
from google.cloud import bigquery
import requests
from datetime import date
import multiprocessing

multiprocessing.set_start_method('fork')

def get_service_account_key():
    # Get the environment variable value
    json_content = os.environ.get('SERVICE_ACCOUNT_KEY')
    # Parse the JSON content
    data = json.loads(json_content)
    return data

def export_bigquery_table_to_sheets(request):
    project_id = os.environ.get('project_id')
    dataset_id = os.environ.get('dataset_id')
    table_id = os.environ.get('table_id')
    spreadsheet_id = os.environ.get('spreadsheet_id')

    # Define the required scopes for BigQuery and Sheets APIs
    scopes = [
        'https://www.googleapis.com/auth/bigquery',
        'https://www.googleapis.com/auth/spreadsheets',
    ]

    # Retrieve the service account key
    service_account_key = get_service_account_key()

    if service_account_key is None:
        return "Error: Service account key is not available."

    try:
        # Authenticate using service account credentials with specified scopes
        credentials = service_account.Credentials.from_service_account_info(
            service_account_key, scopes=scopes)

        # Initialize the BigQuery client
        bq_client = bigquery.Client(credentials=credentials, project=project_id)

        # Get the table reference
        table_ref = bq_client.dataset(dataset_id).table(table_id)

        # Get the table schema
        table = bq_client.get_table(table_ref)

        # Construct the query to extract the full table
        query = f"SELECT * FROM `{project_id}.{dataset_id}.{table_id}`"

        # Fetch the data using BigQuery client
        df = bq_client.query(query).to_dataframe()

        # Convert date objects to strings
        df = df.astype(str)

        # Create the Google Sheets service
        sheets_service = discovery.build('sheets', 'v4', credentials=credentials)

        # Clear the existing data in the sheet
        sheets_service.spreadsheets().values().clear(
            spreadsheetId=spreadsheet_id,
            range='Sheet1',
            body={}
        ).execute()

        # Write the dataframe to the spreadsheet
        df_values = [df.columns.tolist()] + df.values.tolist()
        body = {
            'values': df_values
        }
        sheets_service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range='Sheet1',
            valueInputOption='RAW',
            body=body
        ).execute()

        # Return the spreadsheet URL
        spreadsheet_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}"
        return spreadsheet_url
    except Exception as e:
        print(f"Error occurred during export: {e}")
        return "Error: Export failed."