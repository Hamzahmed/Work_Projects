from create_database import create_database
import psycopg2
from dotenv import load_dotenv
from psycopg2 import sql
import geopandas as gpd
import pandas as pd
import geoalchemy2
from sqlalchemy import create_engine
import os
def existing_data():
    conn_params = {
        'user': os.environ.get('POSTGRES_USER'),
        'password': os.environ.get('POSTGRES_PASSWORD', ''),
        'host': os.environ.get('POSTGRES_HOST', ''),
        'port': os.environ.get('POSTGRES_PORT', '')
    }

    # create database if not exists
    dbname = 'threatanalysis'
    extension = 'postgis'
    create_database(conn_params,dbname, extension)


    file_path = 'data_engineer_tech_challenge_existing_dataset.geojson'
    ex_data = gpd.read_file(file_path)

    ex_data = ex_data.drop(columns = 'id')

    # Create a GeoAlchemy engine
    engine = create_engine(f"postgresql+psycopg2://{conn_params['user']}:{conn_params['password']}@{conn_params['host']}:{conn_params['port']}/{dbname}")

    # Assuming 'gdf' is your GeoPandas DataFrame
    table_name = 'eventdata' 

    # Use GeoAlchemy to create a table with geometry column
    ex_data.to_postgis(table_name, engine, if_exists='replace', index=True, index_label='id')
    return 'Existing data was uploaded successfully!'
    # # Close the connection
    # conn.close()

