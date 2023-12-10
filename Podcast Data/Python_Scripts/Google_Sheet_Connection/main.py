import oauth2client
from oauth2client.client import GoogleCredentials
from oauth2client import client
from oauth2client.client import flow_from_clientsecrets
from oauth2client import file
from oauth2client import tools
from googleapiclient import discovery
from googleapiclient import errors
from google_auth_oauthlib import flow
import google_auth_httplib2
import httplib2
import urllib.request
import time
import os
import io
from io import StringIO
import numpy as np
from googleapiclient.http import MediaIoBaseDownload
import pandas as pd
import json

OAUTH_SCOPES = ("https://www.googleapis.com/auth/drive " + "https://www.googleapis.com/auth/drive.file " + "https://www.googleapis.com/auth/spreadsheets ")

flow = client.flow_from_clientsecrets(
    "//Users/hamza.ahmed/Coding Projects/Python Apps Authentications/Google Sheets/client_secret.json", scope = OAUTH_SCOPES, 
    redirect_uri = "urn:ietf:wg:oauth:2.0:oob")

storage = oauth2client.file.Storage('/Users/hamza.ahmed/Coding Projects/Python Apps Authentications/Google Sheets/credentials.dat')
credentials = storage.get()

if credentials is None or credentials.invalid:
  credentials = tools.run_flow(flow, storage,
                               tools.argparser.parse_known_args()[0])
http = credentials.authorize(httplib2.Http())


service = discovery.build('sheets', 'v4', http=http)

df = pd.read_excel('/Users/hamza.ahmed/Coding Projects/Data/Podsight Data/podsight.xlsx') 

df2 = df.values.tolist()

SPREADSHEET_ID = '1CbVcfelySzeEoGMcr8r-684h10_wVEl9gL1qqaiWN4s'

SHEET_NAME = "API Connected Data"

values = df2
data = [
    {
        'range': f"'{SHEET_NAME}'!A2",
        'values': values
    },
]
body = {
    'valueInputOption': "RAW",
    'data': data
}

result = service.spreadsheets().values().batchUpdate(
    spreadsheetId=SPREADSHEET_ID, body=body).execute()
print('{0} cells updated.'.format(result.get('totalUpdatedCells')))