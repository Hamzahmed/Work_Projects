#Import Packages
import pandas as pd
import numpy as np
import boto3
import json
import sys
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import functions as f
from pyspark.sql import SQLContext
from awsglue.utils import getResolvedOptions
from pyspark.sql import SparkSession
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime
import csv


####THIS IS CURRENTLY BEING RUN AGAINST THE METHODTESTINGDATABASE PLEASE CHANGE TO APPROPRIATE PROD DB #####

#Define any parameters that will ultimately be passed in by the job

with open('cnxn_str.json', 'r') as f:
    cnxn_str = json.load(f)



with open('PolicyID_list.csv', newline='') as f:
    reader = csv.reader(f)
    PolicyID_list = list(reader)

table_name = cnxn_str['table_name']
database = cnxn_str['database_source']
athena_table=database+'.'+ table_name
ss_table=cnxn_str['sql_server_table_name']
table_description_query = f'DESCRIBE {athena_table}'
# PolicyID_Input = []
PolicyID_Input = PolicyID_list

sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
# args = getResolvedOptions(sys.argv, ['JOB_NAME','table_name'])
# job.init(args['JOB_NAME'], args)

# Get credentials form secret manager
def get_secret():
    secret_name = cnxn_str["secret_name"]
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name=cnxn_str['secretsmanager'],
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']
    return secret



secretvalue = json.loads(get_secret())
hostname = secretvalue['host']
print(f"Host name {hostname}")
username = secretvalue['username']
password = secretvalue['password']

# Create an S3 client
s3 = boto3.client('s3')



# pull the desired table from Athena and assign to df
df_columns_athena = spark.sql(table_description_query).toPandas()
columns_list = df_columns_athena['col_name'].tolist()



# #Provide Policy ID that you want to validate. If no Policy ID provided, the policy IDs with the top 10 most dense records in the Athena table will be used.
# PolicyID_Input = ["'"+s.lower().replace('-', '') +"'" for s in PolicyID_Input]



#Note: This only works with tables less than 300 columns.
#Building the dense record query to find the most populated columns per record OR using the provided policy id list to pull records while ignoring empty strings and nulls in the count
if len(PolicyID_Input) ==0:
    print(f'No Specific Policy IDs provided, will extract Policy IDs from the {table_name} table.')
    case_when_list = []
    for columns in columns_list:
        if columns == columns_list[-1]:
            case_when_list.append('case when ' + columns + ' is not null or ' + columns + ' <> \'\' then 1 else 0 end')
        else:
            case_when_list.append('case when ' + columns + ' is not null or ' + columns + ' <> \'\' then 1 else 0 end +')
    athena_columns_string= ' '.join(map(str,case_when_list))
    athena_dense_records_query_no_policy_id_provided = f'Select *, {athena_columns_string} as count_of_non_nulls from {athena_table} where explastupdatedtimestamp = (select max(explastupdatedtimestamp) from {athena_table})order by 1 DESC limit 10 '
    df_initial_athena = spark.sql(athena_dense_records_query_no_policy_id_provided).toPandas()
else:
    print("Using the Policy IDs provided to query the table.")
    condensed_list = (', '.join("'" + item + "'" for item in PolicyID_Input))
    athena_dense_records_query_policy_id_provided = f"""Select * from {athena_table} WHERE exppolicyid IN ({condensed_list}) order by 1 DESC limit 10"""
    df_initial_athena = spark.sql(athena_dense_records_query_policy_id_provided).toPandas()
    
    

#retrieving the policyIDs
PolicyIDs = df_initial_athena.iloc[:, [0]].values.tolist()

#If policy id is provided, then do nothing, else run dense record calculations. 
if len(PolicyID_Input) ==0:
    print('Policy ID not provided,creating list of most dense records')
    df_PolicyIDs = [item for sublist in PolicyIDs for item in sublist]
else:
    print('List is provided from the table.')
    df_PolicyIDs = PolicyID_Input


#creating query with list of policy id's
ss_query= f"""SELECT * FROM {ss_table} WHERE policyid IN  ({(', '.join("'" + item + "'" for item in df_PolicyIDs))})"""
print(ss_query)


#Run Query against SQL Server 
jdbcUrl = secretvalue['jdbcURL']
df_query = spark.read \
    .format("jdbc") \
    .option("url", jdbcUrl) \
    .option("query", ss_query) \
    .option("user", username) \
    .option("password", password) \
    .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver") \
    .load() 
    # .orderBy(f.col("PolicyID").desc())
df_sql_server = df_query.toPandas()



#Changing the variable types for version column so the df_initial_athena table and df_sql_server can be joined
df_initial_athena['expxmlversion'] = df_initial_athena['expxmlversion'].astype(int)
df_sql_server['Version'] = df_sql_server['Version'].astype(int)
df_initial_athena['explastupdatedtimestamp'] = pd.to_datetime(df_initial_athena['explastupdatedtimestamp']).apply(lambda x: x.strftime('%Y-%m-%d %H:%M'))
df_sql_server['LastUpdatedTimestamp'] = pd.to_datetime(df_sql_server['LastUpdatedTimestamp']).apply(lambda x: x.strftime('%Y-%m-%d %H:%M'))

#this step is required as the version is not provided by the user at runtime. This allows for each version to be compared between SQLServer and Athena
#aditionally removes versions that have been archived and no longer exist in sql server and new versions in sql server that do not exist in Athena
df_ss_athena= pd.merge(df_sql_server, df_initial_athena, left_on=['PolicyId','Version', 'LastUpdatedTimestamp'], right_on=['exppolicyid', 'expxmlversion', 'explastupdatedtimestamp'], how='inner')

# Create a dataframe that is extracted from the joined dataframe. This section is dropping the extra columns so that we can compare the values in this df
# This is necessary as merging the tables above added columns to the result set that we do not want to use in the compare
df_athena_cols = set(df_initial_athena.columns)
df_sql_server_cols = set(df_sql_server.columns)
df_athena = df_ss_athena.drop(df_sql_server_cols, axis=1)

df_athena.fillna(value=np.nan, inplace=True)


    
import xml.etree.ElementTree as ET
import pandas as pd

def get_section_data(xml_str, section_name):
    root = ET.fromstring(xml_str)
    data = []
    
    # recursively search for the section name
    def search_section(elem):
        if elem.tag == section_name:
            return elem
        else:
            for child in elem:
                found = search_section(child)
                if found is not None:
                    return found
            return None
    
    section = search_section(root)
    if section is not None:
        for elem in section.iter():
            if elem.tag != section_name:
                row = {}
                row['element'] = elem.tag
                for attr, val in elem.items():
                    row[attr] = val
                if elem.text and elem.text.strip():
                    row['text'] = elem.text.strip()
                data.append(row)
    
    return pd.DataFrame(data)


#Parsing individual sections of the XML and putting them into a list
section_data = []
for x in range(len(df_ss_athena)):
    section_data.append(get_section_data(df_ss_athena['XmlDoc'][x],table_name))

# create a new column in each dataframe with the corresponding UUID
df_ss_athena_column = df_athena.iloc[:, [0]].values.tolist()
df_ss_athena_column_first = [item for sublist in df_ss_athena_column for item in sublist]
for i, df in enumerate(section_data):
    df['UUID'] = df_ss_athena_column_first[i]
    df['name'] = df['name'].str.lower()
    df.fillna(value=np.nan, inplace=True)

# concatenate the dataframes into a single dataframe
result_df = pd.concat(section_data)

#Creates the data validation including comparing nulls/empty strings with missing values in a variable XML files. 
result_validate = pd.DataFrame(columns=df_athena.columns)
for x in range(len(df_athena)):
    matching_elements = [element for element in list(df_athena.columns) if element in list(section_data[x]['name'].astype(str).fillna('nan'))]
    unmatching_elements = [element for element in list(df_athena.columns) if element not in list(section_data[x]['name'].astype(str).fillna('nan'))]
    if set(df_athena.columns).intersection(set(section_data[x]['name'])):
        first_row = df_athena.iloc[x]
        result = first_row.isin(section_data[x].loc[section_data[x]['name'].isin(matching_elements)].values.flatten())
        result = result.fillna(False)  # fill NaN values with False
        result_validate.loc[x] = result
        for col in unmatching_elements:
            result_validate.loc[x, col] = 'True'

#All matches displayed with Policy ID, Version, and Athena's explastupdatedtimestamp
Overall_Validation = pd.DataFrame(result_validate)
Overall_Validation.insert(loc=0, column='policyid_athena', value=df_athena['exppolicyid'])
Overall_Validation.insert(loc=1, column='version_athena', value=df_athena['expxmlversion'])
Overall_Validation.insert(loc=2, column='explastupdatedtimestamp_athena', value=df_athena['explastupdatedtimestamp'])

#Configuring Over_Validation for s3
Overall_Validation=Overall_Validation.astype(str)
Overall_Validation.info()
today=datetime.today()

#create a pivot of Overall_Validation
Overall_Validation_Pivot=(Overall_Validation.melt(['policyid_athena','explastupdatedtimestamp_athena','version_athena'], 
             var_name='column_name', 
             value_name='column_validation'
             )
        )
Overall_Validation_Pivot['Table_Name'] = table_name
Overall_Validation_Pivot['Validation_load_date'] = today 
# Overall_Validation_Pivot=Overall_Validation_Pivot.drop('count_of_non_nulls',axis=1)
Overall_Validation_Pivot= Overall_Validation_Pivot.reset_index(drop=True)
print(Overall_Validation.head())


#Write Overall_Validation to s3
s3_url = f's3://exp-sql-server-xml-test/pxvault/pxvault_qa/Overall_validation_{table_name}_{today}.parquet'
Overall_Validation_Pivot.to_parquet(s3_url, compression='gzip')
job.commit()
