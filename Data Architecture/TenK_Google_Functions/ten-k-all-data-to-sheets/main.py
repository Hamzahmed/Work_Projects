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

def export_refined_bigquery_tables_to_sheets(request):
    project_id = os.environ.get('project_id')
    dataset_id = os.environ.get('dataset_id')
    table_id = os.environ.get('table_id')
    spreadsheet_id = os.environ.get('spreadsheet_id')
    assignment_table = os.environ.get('assignment_table')
    Users_table = os.environ.get('Users_table')
    projects_table = os.environ.get('projects_table')
    status_options_table = os.environ.get('status_options_table')
    placeholders_table = os.environ.get('placeholders_table')
    Leave_table = os.environ.get('Leave_table')

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

        # Create the Google Sheets service
        sheets_service = discovery.build('sheets', 'v4', credentials=credentials)

        # Process and export Assignments
        sheet_assignment = 'Assignments'
        sheets_service.spreadsheets().values().clear(
            spreadsheetId=spreadsheet_id,
            range= f"'{sheet_assignment}'!A:Z",
            body={}
        ).execute()
        assignment_ref = bq_client.dataset(dataset_id).table(assignment_table)
        assignment = bq_client.get_table(assignment_ref)
        assignment_query = f"SELECT * FROM `{project_id}.{dataset_id}.{assignment_table}`"
        assignment_df = bq_client.query(assignment_query).to_dataframe()
        assignment_df = assignment_df.astype(str)
        assignment_df_values = [assignment_df.columns.tolist()] + assignment_df.values.tolist()
        assignment_body = {
            'valueInputOption': 'RAW',
            'data': [
                {
                    'range': f"'{sheet_assignment}'!A1",
                    'values': assignment_df_values
                }
            ]
        }
        sheets_service.spreadsheets().values().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=assignment_body
        ).execute()
        print (f"{assignment_table} exported to sheet {spreadsheet_id}")

        # Process and export Users
        sheet_Users = 'Users'
        sheets_service.spreadsheets().values().clear(
            spreadsheetId=spreadsheet_id,
            range= f"'{sheet_Users}'!A:Z",
            body={}
        ).execute()        
        Users_ref = bq_client.dataset(dataset_id).table(Users_table)
        Users = bq_client.get_table(Users_ref)
        Users_query = f"SELECT * FROM `{project_id}.{dataset_id}.{Users_table}`"
        Users_df = bq_client.query(Users_query).to_dataframe()
        Users_df = Users_df.astype(str)
        Users_df_values = [Users_df.columns.tolist()] + Users_df.values.tolist()

        Users_body = {
            'valueInputOption': 'RAW',
            'data': [
                {
                    'range': f"'{sheet_Users}'!A1",
                    'values': Users_df_values
                }
            ]
        }

        sheets_service.spreadsheets().values().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=Users_body
        ).execute()
        print (f"{Users_table} exported to sheet {spreadsheet_id}")

        # Process and export Projects
        sheet_projects = 'Projects'
        sheets_service.spreadsheets().values().clear(
            spreadsheetId=spreadsheet_id,
            range= f"'{sheet_projects}'!A:Z",
            body={}
        ).execute()        
        projects_ref = bq_client.dataset(dataset_id).table(projects_table)
        projects = bq_client.get_table(projects_ref)
        projects_query = f"SELECT * FROM `{project_id}.{dataset_id}.{projects_table}`"
        projects_df = bq_client.query(projects_query).to_dataframe()
        projects_df = projects_df.astype(str)
        projects_df_values = [projects_df.columns.tolist()] + projects_df.values.tolist()

        projects_body = {
            'valueInputOption': 'RAW',
            'data': [
                {
                    'range': f"'{sheet_projects}'!A1",
                    'values': projects_df_values
                }
            ]
        }

        sheets_service.spreadsheets().values().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=projects_body
        ).execute()
        print (f"{projects_table} exported to sheet {spreadsheet_id}")

        # Process and export status_options
        sheet_status_options = 'Status_Options'
        sheets_service.spreadsheets().values().clear(
            spreadsheetId=spreadsheet_id,
            range= f"'{sheet_status_options}'!A:Z",
            body={}
        ).execute()        
        status_options_ref = bq_client.dataset(dataset_id).table(status_options_table)
        status_options = bq_client.get_table(status_options_ref)
        status_options_query = f"SELECT * FROM `{project_id}.{dataset_id}.{status_options_table}`"
        status_options_df = bq_client.query(status_options_query).to_dataframe()
        status_options_df = status_options_df.astype(str)
        status_options_df_values = [status_options_df.columns.tolist()] + status_options_df.values.tolist()

        status_options_body = {
            'valueInputOption': 'RAW',
            'data': [
                {
                    'range': f"'{sheet_status_options}'!A1",
                    'values': status_options_df_values
                }
            ]
        }

        sheets_service.spreadsheets().values().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=status_options_body
        ).execute()
        print (f"{status_options_table} exported to sheet {spreadsheet_id}")

        # Process and export placeholders
        sheet_placeholders = 'Placeholders'
        sheets_service.spreadsheets().values().clear(
            spreadsheetId=spreadsheet_id,
            range= f"'{sheet_placeholders}'!A:Z",
            body={}
        ).execute()        
        placeholders_ref = bq_client.dataset(dataset_id).table(placeholders_table)
        placeholders = bq_client.get_table(placeholders_ref)
        placeholders_query = f"SELECT * FROM `{project_id}.{dataset_id}.{placeholders_table}`"
        placeholders_df = bq_client.query(placeholders_query).to_dataframe()
        placeholders_df = placeholders_df.astype(str)
        placeholders_df_values = [placeholders_df.columns.tolist()] + placeholders_df.values.tolist()

        placeholders_body = {
            'valueInputOption': 'RAW',
            'data': [
                {
                    'range': f"'{sheet_placeholders}'!A1",
                    'values': placeholders_df_values
                }
            ]
        }

        sheets_service.spreadsheets().values().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=placeholders_body
        ).execute()
        print (f"{placeholders_table} exported to sheet {spreadsheet_id}")
        # Process and export Leave
        sheet_Leave = 'Leave'
        sheets_service.spreadsheets().values().clear(
            spreadsheetId=spreadsheet_id,
            range= f"'{sheet_Leave}'!A:Z",
            body={}
        ).execute()        
        Leave_ref = bq_client.dataset(dataset_id).table(Leave_table)
        Leave = bq_client.get_table(Leave_ref)
        Leave_query = f"SELECT * FROM `{project_id}.{dataset_id}.{Leave_table}`"
        Leave_df = bq_client.query(Leave_query).to_dataframe()
        Leave_df = Leave_df.astype(str)
        Leave_df_values = [Leave_df.columns.tolist()] + Leave_df.values.tolist()

        Leave_body = {
            'valueInputOption': 'RAW',
            'data': [
                {
                    'range': f"'{sheet_Leave}'!A1",
                    'values': Leave_df_values
                }
            ]
        }

        sheets_service.spreadsheets().values().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=Leave_body
        ).execute()
        print (f"{Leave_table} exported to sheet {spreadsheet_id}")


        # Return the spreadsheet URL
        spreadsheet_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}"
        return spreadsheet_url

    except Exception as e:
        print(f"Error occurred during export: {e}")
        return "Error: Export failed."