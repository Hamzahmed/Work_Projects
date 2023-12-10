# %%
import timeit
import requests
import json
import pandas as pd
from io import BytesIO, StringIO
import numpy as np
from datetime import datetime
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
import ast
import io
from io import StringIO
from googleapiclient.http import MediaIoBaseDownload
from venv import create
import googleapiclient.discovery
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import json
#!/usr/bin/env python
import snowflake.connector
#from snowflake.sqlalchemy import URL
#from sqlalchemy import create_engine
from snowflake.connector.pandas_tools import write_pandas
import pandas as pd
pd.set_option("display.max_rows", None, "display.max_columns", None)

# %%

with open('/Users/hamza.ahmed/Coding Projects/Python Apps Authentications/Sprout Social/Sprout_Social.json', 'r') as f:
    passcode = json.load(f)
params = passcode['Access']['Key']

path_to_json = "/Users/hamza.ahmed/Coding Projects/Python Apps Authentications/Snowflake/snowflake_auth.json"

with open(path_to_json, "r") as handler:
    info = json.load(handler)

# %%
today = datetime.today().strftime("%Y-%m-%dT%H:%M:%S")

# %%
get_url = "https://api.sproutsocial.com/v1/metadata/client"
customer_get_url = "https://api.sproutsocial.com/v1/1471694/metadata/customer"

# %%
try:
    response_costomer = requests.get(
        url=customer_get_url,json={"key": "value"},
        headers={
            "Authorization": 'Bearer ' +params,
        },
    )
    print('Response HTTP Status Code: {status_code}'.format(
        status_code=response_costomer.status_code))
    print('Response HTTP Response Body: {content}'.format(
        content=response_costomer.content))
except requests.exceptions.RequestException:
    print('HTTP Request failed')

# %%
j_customer = response_costomer.json()
df_customer = pd.json_normalize(j_customer["data"])

# %%
response_tags = requests.get(
url="https://api.sproutsocial.com/v1/1471694/data",
headers={
    "Authorization": 'Bearer ' +params,
},
)

# %%
payload = []
for x in range(1,20):
  payload.append({
    "fields": [
      "title",
      "created_time",
      "content_category",
      "post_type",
      "internal.tags.id",
      "post_category",
      "network",
      "perma_link",
      "profile_guid",
      "text",
      "title",
      "from",
      #"visual_media",
      #"hashtags"
    ],
    "filters": [
      "customer_profile_id.eq(4526462, 4530996, 4530999)",
      f"created_time.in(2020-12-01T00:00:00..{today})"
    ],#2022-06-22T23:59:59
    "metrics": [
      "lifetime.impressions",
      "lifetime.impressions_organic",
      "lifetime.impressions_paid",
      "lifetime.impressions_unique",
      "lifetime.impressions_organic_unique",
      "lifetime.impressions_viral_unique",
      "lifetime.impressions_nonviral_unique",
      "lifetime.impressions_paid_unique",
      "lifetime.impressions_follower_unique",
      "lifetime.post_content_clicks",
      "lifetime.likes",
      "lifetime.comments_count",
      "lifetime.shares_count",
      "lifetime.reactions",
      "lifetime.video_views",
      
    ],
      "page": x
  })

# %%
response = []

for r in payload:
        response.append(requests.post(
        url="https://api.sproutsocial.com/v1/1471694/analytics/posts",json=r,
        headers={
            "Authorization": 'Bearer ' +params,
        },
        ))

# %%

import json
post_data = []
for q in response:
    if q.status_code == 200:
        post_data.append(q.json())
len(post_data)

# %%
all_data = []
for y in range(len(post_data)):
    all_data.append(pd.json_normalize(post_data[y]['data']))

# %%
df_posts = pd.concat(all_data).reset_index()

# %%
import numpy as np
sum_imp_1 = np.sum(df_posts['metrics.lifetime.impressions'])
sum_imp_1

# %%
def try_literal_eval(e):
    try:
        return ast.literal_eval(e)
    except ValueError:
        return [{'id': 0, 'id': 0}]

# %%
df_posts['internal.tags'] = df_posts['internal.tags'].astype(str).apply(try_literal_eval)

# %%
df_posts = df_posts.explode('internal.tags')
df_posts['tags']  = df_posts['internal.tags'] .str['id']

# %%
response_tags = requests.get(
url="https://api.sproutsocial.com/v1/1471694/metadata/customer/tags",
headers={
    "Authorization": 'Bearer ' +params,
},
)

# %%
rt = response_tags.json()
df_tags = pd.json_normalize(rt["data"])
df_tags.drop('any_group', axis=1, inplace=True)
df_tags.drop('groups', axis=1, inplace=True)
df_tags.drop('active', axis=1, inplace=True)
df_tags = df_tags.rename(columns= {"text": "Campaigns"})

# %%
df_tags = df_tags.rename(columns={'tag_id':'tags'})
post_data = df_posts.merge(df_tags, on='tags', how='left')

# %%
post_data = post_data.drop(columns = ['internal.tags', 'tags', 'index'])

# %%
post_data = post_data.groupby(['created_time', 'content_category', 'post_category', 'post_type',
'customer_profile_id', 'profile_guid','perma_link', 'network', 'sent', 'from.guid', 'from.name',
'from.profile_picture']).agg({'text': lambda x: ','.join(x[x.notna()]), 
            'metrics.lifetime.likes': lambda x: np.mean(x[x.notna()]),
            'metrics.lifetime.comments_count': lambda x: np.mean(x[x.notna()]),
            'metrics.lifetime.impressions': lambda x: np.mean(x[x.notna()]),
            'metrics.lifetime.impressions_organic': lambda x: np.mean(x[x.notna()]),
            'metrics.lifetime.post_content_clicks': lambda x: np.mean(x[x.notna()]),
            'metrics.lifetime.shares_count': lambda x: np.mean(x[x.notna()]),
            'metrics.lifetime.reactions': lambda x: np.mean(x[x.notna()]),
            'metrics.lifetime.video_views': lambda x: np.mean(x[x.notna()]),
            'metrics.lifetime.impressions_organic_unique': lambda x: np.mean(x[x.notna()]),
            'metrics.lifetime.likes': lambda x: np.mean(x[x.notna()]),
            'metrics.lifetime.impressions_paid': lambda x: np.mean(x[x.notna()]),
            'metrics.lifetime.impressions_unique': lambda x: np.mean(x[x.notna()]),
            'metrics.lifetime.impressions_follower_unique': lambda x: np.mean(x[x.notna()]),
            'metrics.lifetime.impressions_nonviral_unique': lambda x: np.mean(x[x.notna()]),
            'metrics.lifetime.impressions_viral_unique': lambda x: np.mean(x[x.notna()]),
                        'title': lambda x: ','.join(x[x.notna()]),
            'Campaigns': lambda x: list(x[x.notna()])
            }).reset_index()
len(post_data)

# %%
import numpy as np
sum_imp_2 =np.sum(post_data['metrics.lifetime.impressions'])
sum_imp_2

# %%
post_data.columns = post_data.columns.map(str.strip)

# %%
df_posts.replace([np.inf, -np.inf], np.nan, inplace=True)
df_posts.fillna('', inplace=True)
#df_posts['hashtags'] = df_posts['hashtags'].astype("string")
df_posts['perma_link'] = df_posts['perma_link'].astype("string")
#df1['internal.tags'] = df1['internal.tags'].astype("string")
#df_posts['visual_media'] = df_posts['visual_media'].astype("string")
#df.to_excel('/Users/hamza.ahmed/Coding Projects/Data/Sprout Social/Sprout_Social_data.xlsx', 'openpyxl')

# %%
profile_payload = {
  
  "filters": [
    "customer_profile_id.eq(4526462, 4530996, 4530999)",
    f"reporting_period.in(2021-12-01T00:00:00..{today})"
  ],
  "metrics": [
    "followers_gained_organic",
    " lifetime_snapshot.followers_count",
    "followers_gained_paid",
    "net_follower_growth",
    "followers_gained",
    "followers_lost",
    "profile_views_unique"

  ]
}

# %%
response_profile = requests.post(
url="https://api.sproutsocial.com/v1/1471694/analytics/profiles",json=profile_payload,
headers={
    "Authorization": 'Bearer ' +params,
},
)

# %%
rp = response_profile.json()
df_profile = pd.json_normalize(rp["data"])

# %%
df_profile = df_profile.rename(columns={'dimensions.customer_profile_id':'customer_profile_id'})

# %%
df_customer['customer_profile_id']=df_customer['customer_profile_id'].astype(int)
df_profile['customer_profile_id'] = df_profile['customer_profile_id'].astype(int)

# %%
follower_data = df_profile.merge(df_customer, on='customer_profile_id', how='left')

# %%
#post_data['hashtags'] = post_data['hashtags'].astype("string")
post_data['perma_link'] = post_data['perma_link'].astype("string")
#post_data['internal.tags'] = post_data['internal.tags'].astype("string")
#post_data['visual_media'] = post_data['visual_media'].astype("string")
Sprout_Social_Post_Data = post_data
#Sprout_Social_Post_Data = post_data.astype(str)

# %%
follower_data['native_name'] = follower_data['native_name'].astype("string")
follower_data['link'] = follower_data['link'].astype("string")
follower_data['groups'] = follower_data['groups'].astype("string")

# %%
follower_data.loc[follower_data.network_type =='linkedin_company', 'network_type'] ='LINKEDIN'
follower_data.loc[follower_data.network_type =='fb_instagram_account', 'network_type'] ='INSTAGRAM'
follower_data.loc[follower_data.network_type =='facebook', 'network_type'] ='FACEBOOK'
Sprout_Social_Follower_Data = follower_data

# %%
Sprout_Social_Post_Data.columns = Sprout_Social_Post_Data.columns.str.upper()
Sprout_Social_Post_Data.columns = Sprout_Social_Post_Data.columns.str.replace(".", "_")
Sprout_Social_Post_Data = Sprout_Social_Post_Data.rename(columns={"TEXT": "POST_TEXT", "NETWORK": "NETWORK_TYPE","TAGS": "TAGS_ID", "CAMPAIGNS": "TAGS_CAMPAIGN" })
Sprout_Social_Post_Data = Sprout_Social_Post_Data.replace('nan','0')
#Sprout_Social_Post_Data["NETWORK_TYPE"]= Sprout_Social_Post_Data["NETWORK_TYPE"].str.upper().str.title()
Sprout_Social_Post_Data = Sprout_Social_Post_Data.replace('null','0')
Sprout_Social_Post_Data = Sprout_Social_Post_Data.replace('NaN','0')

# %%
Sprout_Social_Post_Data = Sprout_Social_Post_Data.fillna(0)

# %%


# %%


# %%
Sprout_Social_Follower_Data.columns = Sprout_Social_Follower_Data.columns.str.upper()
Sprout_Social_Follower_Data.columns = Sprout_Social_Follower_Data.columns.str.replace(".", "_")
Sprout_Social_Follower_Data = Sprout_Social_Follower_Data.rename(columns={"DIMENSIONS_REPORTING_PERIOD_BY(DAY)": "DIMENSIONS_REPORTING_PERIOD_BY_DAY" })
Sprout_Social_Follower_Data = Sprout_Social_Follower_Data.replace('nan','0')
#Sprout_Social_Follower_Data["NETWORK_TYPE"]= Sprout_Social_Follower_Data["NETWORK_TYPE"].str.upper().str.title()
Sprout_Social_Follower_Data = Sprout_Social_Follower_Data.replace('null','0')
Sprout_Social_Follower_Data = Sprout_Social_Follower_Data.replace('NaN','0')

# %%


# %%
Users = info["users"][0]["name"]
Password = info["users"][0]["password"]
Account = 'cp91638.us-central1.gcp'
authenticator='externalbrowser'
Warehouse = 'FIVETRAN_WAREHOUSE'
Database="FIVETRAN_DATABASE",
Schema="TABLEAU_CONNECTION"
Role = "ACCOUNTADMIN"


# %%
# set up connection
conn = snowflake.connector.connect(
            account = Account,
            user = Users,
            authenticator = authenticator,
            password = Password,
            warehouse = Warehouse,
            database = Database,
            schema = Schema,
            role = Role)    

# set up cursor
cur = conn.cursor()

# %%

query1 = '''
USE DATABASE FIVETRAN_DATABASE;
'''
cur.execute(query1)

query2 = '''
truncate table if exists FIVETRAN_DATABASE.TABLEAU_CONNECTION.SPROUT_SOCIAL_POST_DATA
'''
cur.execute(query2)

query3 = '''
truncate table if exists FIVETRAN_DATABASE.TABLEAU_CONNECTION.SPROUT_SOCIAL_PROFILE_DATA
'''
cur.execute(query3)
success, nchunks, nrows, _ = write_pandas(conn, Sprout_Social_Post_Data, "SPROUT_SOCIAL_POST_DATA","FIVETRAN_DATABASE", "TABLEAU_CONNECTION")
success, nchunks, nrows, _ = write_pandas(conn, Sprout_Social_Follower_Data, "SPROUT_SOCIAL_PROFILE_DATA","FIVETRAN_DATABASE", "TABLEAU_CONNECTION")

conn.close()

# %%
follower_data = follower_data.astype(str)
post_data = post_data.astype(str)

# %%
OAUTH_SCOPES = ("https://www.googleapis.com/auth/drive " + "https://www.googleapis.com/auth/drive.file " + "https://www.googleapis.com/auth/spreadsheets ")

# %%
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

# %%
SPREADSHEET_ID = '1tiocA6VBtEdMH-MFCLXiM3UcUdVTOamks6tyje5aPCQ'

SHEET_NAME = "POST DATA"
SHEET_NAME_2 = "PROFILE DATA"


# %%
range_posts = '{0}!A1:ZZ'.format( SHEET_NAME )
range_profiles = '{0}!A1:ZZ'.format( SHEET_NAME_2 )
clear_values_request_body = {
    # TODO: Add desired entries to the request body.
}

# %%
request_clear_posts = service.spreadsheets().values().clear(spreadsheetId=SPREADSHEET_ID, range=range_posts, body=clear_values_request_body)
response = request_clear_posts.execute()

request_clear_profiles = service.spreadsheets().values().clear(spreadsheetId=SPREADSHEET_ID, range=range_profiles, body=clear_values_request_body)
response = request_clear_profiles.execute()

# %%
values_posts = [post_data.columns.values.tolist()] + post_data.values.tolist()
data_posts = [
    {
        'range': f"'{SHEET_NAME}'!A1",
        'values': values_posts
    },
    # Additional ranges to update ...
]
body_posts = {
    'valueInputOption': "RAW",
    'data': data_posts

}



# %%
values_profile = [follower_data.columns.values.tolist()] + follower_data.values.tolist()
data_profile = [
    {
        'range': f"'{SHEET_NAME_2}'!A1",
        'values': values_profile
    },
    # Additional ranges to update ...
]
body_profile = {
    'valueInputOption': "RAW",
    'data': data_profile

}


# %%
result_posts = service.spreadsheets().values().batchUpdate(
    spreadsheetId=SPREADSHEET_ID, body=body_posts).execute()
print('{0} cells updated.'.format(result_posts.get('totalUpdatedCells')))


# %%
result_profiles = service.spreadsheets().values().batchUpdate(
    spreadsheetId=SPREADSHEET_ID, body=body_profile).execute()
print('{0} cells updated.'.format(result_profiles.get('totalUpdatedCells')))


