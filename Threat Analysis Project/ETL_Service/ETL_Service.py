import geopandas as gpd
import pandas as pd
import psycopg2
import geoalchemy2
from dotenv import load_dotenv
from psycopg2 import sql
from sqlalchemy import create_engine
import os
from create_database import create_database
import time
from shapely.geometry import Point
from existing_data_into_postgres import existing_data
pd.set_option('display.max_columns', None)
load_dotenv()

existing_data()

#Using the connection strings to talk to the postgres database
conn_params = {
    'user': os.environ.get('POSTGRES_USER'),
    'password': os.environ.get('POSTGRES_PASSWORD', ''),
    'host': os.environ.get('POSTGRES_HOST', ''),
    'port': os.environ.get('POSTGRES_PORT', '')
}

# create database if not exists
dbname = 'threatanalysis'


conn = psycopg2.connect(dbname=dbname, **conn_params)

# Define the SQL query to fetch data from the table
table_name = "eventdata"
sql_query = f"""SELECT * FROM {table_name};"""

# Use Pandas to read the query result into a DataFrame
EventData = gpd.read_postgis(sql_query, conn, geom_col='geometry')

#Working with the county dataset
county_gdf = gpd.read_file('/app/geojson-counties-fips.json')
county_gdf.columns = county_gdf.columns.str.lower()
county_gdf = (county_gdf[['name', 'geometry']]
.copy()
.rename(columns={'name': 'event_county'})
)
county_gdf['event_county'] = county_gdf['event_county'].str.title()

#retrieving the data 2021-now from the github
gdf = gpd.read_file('/app/ccc_compiled_2021-present.csv')

#changing the lat/lon from object dtype to floatn64
gdf['lat'] = pd.to_numeric(gdf['lat'], errors='coerce')
gdf['lon'] = pd.to_numeric(gdf['lon'], errors='coerce')

#making the lat/lon into geometry and prep it for spatial join
geometry = [Point(lon, lat) for lon, lat in zip(gdf['lon'], gdf['lat'])]

gdf = gpd.GeoDataFrame(gdf, geometry=geometry, crs=gdf.crs)
gdf = gdf.replace('NA', None)

# Convert the 'dates' column to datetime format
gdf['date'] = pd.to_datetime(gdf['date'])
gdf_2021 = gdf[gdf['date'].dt.year == 2021]

#spatially joining the dataset
sjoined_data = gpd.sjoin(gdf_2021,county_gdf, predicate='within', how='left')

#joining all the sources to a comma separated list
sjoined_data['source'] = sjoined_data.apply(lambda row: ','.join(str(val) for val in row.filter(like='source_') if val is not None), axis=1)

#preparing the data to move it the postgres
new_data = gpd.GeoDataFrame({'event_id': sjoined_data['fips_code']
                                ,'event_date':sjoined_data['date']
                                ,'event_state':sjoined_data['state']
                                    ,'event_county':sjoined_data['event_county']
                                    ,'event_city':sjoined_data['locality']
                                    ,'event_type':sjoined_data['type']
                                    ,'event_source':sjoined_data['source']
                                    ,'geometry':sjoined_data['geometry']})


#grouping data to clean out the duplicates

grouped_data = new_data.groupby(['event_id', 'event_date', 'geometry']).agg({
    'event_state': 'first',
    'event_county': 'first',
    'event_city': 'first',
    'event_type': lambda x: '; '.join(x) if any(x) else None,
    'event_source': lambda x: '; '.join(x) if any(x) else None
}).reset_index()

#preping the data to append it to the existing table. 
# This is the way I would incrementally load the data into postgres servers
max_row_event = max(EventData['event_id'])
max_row_id = max(EventData['id'])

max_row_event = max_row_event + 1
max_row_id = max_row_id +1

new_event_ids = range(max_row_event, max_row_event + len(grouped_data))

new_ids = range(max_row_id, max_row_id + len(grouped_data))

grouped_data['event_id'] = new_event_ids
grouped_data['id'] = new_ids


# Here I am creating a GeoAlchemy engine to work with to_postgis
engine = create_engine(f"postgresql+psycopg2://{conn_params['user']}:{conn_params['password']}@{conn_params['host']}:{conn_params['port']}/{dbname}")

grouped_data = gpd.GeoDataFrame(grouped_data)
# Set the CRS for the GeoDataFrame
desired_crs = 'EPSG:4326'
table_name = 'eventdata'

#Move the data to postgres
grouped_data = grouped_data.set_crs(desired_crs, allow_override=True)
grouped_data.to_postgis(table_name, engine, if_exists='append', index=False)
print(f'New data added into {table_name}!')

# Close the connection
conn.close()
