# %%
import json
import numpy as np
#!/usr/bin/env python
import snowflake.connector
#from snowflake.sqlalchemy import URL
#from sqlalchemy import create_engine
import lxml
from lxml import etree
from snowflake.connector.pandas_tools import write_pandas
import pandas as pd
import urllib.request
path_to_json = "/Users/hamza.ahmed/Coding Projects/Python Apps Authentications/Snowflake/snowflake_auth.json"

pd.set_option("display.max_rows", None, "display.max_columns", None)

with open(path_to_json, "r") as handler:
    info = json.load(handler)

# %%
Users = info["users"][0]["name"]
Password = info["users"][0]["password"]
Account = 'cp91638.us-central1.gcp'
authenticator='externalbrowser'
Warehouse = 'FIVETRAN_WAREHOUSE'
Database="FIVETRAN_DATABASE",
Schema="EPS_TABLEAU_CONNECTION"
Role = "ACCOUNTADMIN"

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
query = '''
select * from FIVETRAN_DATABASE.YOUTUBE_ANALYTICS.EPS_YOUTUBE_ANALYTICS;
'''
cur.execute(query)

df1 = pd.read_sql(query, conn)

query_b = '''
select * from FIVETRAN_DATABASE.EPS_TABLEAU_CONNECTION.EPS_YOUTUBE_DATA_UPDATED;
'''
cur.execute(query_b)
df2 = pd.read_sql(query_b, conn)
Video_IDs = df1['VIDEO_ID']

# %%
len(Video_IDs)

# %%
video_urls = []
for x in Video_IDs:
    video_urls.append('http://youtube.com/watch?v=' + x)

# %%

Video_Titles = []
for x in video_urls:
    youtube = etree.HTML(urllib.request.urlopen(x).read())
    video_title = youtube.xpath("/html/head/title")
    Video_Titles.append(video_title[0].text)

# %%
df1['VIDEO_URLS'] = video_urls
df1['VIDEO_TITLES'] = Video_Titles

# %%
Users = info["users"][0]["name"]
Password = info["users"][0]["password"]
Account = "cp91638.us-central1.gcp"
authenticator="externalbrowser"
Warehouse = "FIVETRAN_WAREHOUSE"
Database="FIVETRAN_DATABASE",
Schema="EPS_TABLEAU_CONNECTION"
Role = "ACCOUNTADMIN"



conn = snowflake.connector.connect(
            account = Account,
            user = Users,
            authenticator = authenticator,
            password = Password,
            warehouse = Warehouse,
            database = Database,
            schema = Schema,
            role = Role)   

cur = conn.cursor()

query3 = '''
USE DATABASE FIVETRAN_DATABASE;
'''
cur.execute(query3)


query4 = '''
truncate table if exists FIVETRAN_DATABASE.EPS_TABLEAU_CONNECTION.EPS_YOUTUBE_DATA_UPDATED
'''
cur.execute(query4)

success, nchunks, nrows, _ = write_pandas(conn, df1, "EPS_YOUTUBE_DATA_UPDATED","FIVETRAN_DATABASE", "EPS_TABLEAU_CONNECTION")
conn.close()


