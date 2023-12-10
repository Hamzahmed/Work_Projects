import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
load_dotenv()
import os
    # conn_params = {
    #     'user': os.environ.get('POSTGRES_USER'),
    #     'password': os.environ.get('POSTGRES_PASSWORD', ''),
    #     'host': os.environ.get('POSTGRES_HOST', ''),
    #     'port': os.environ.get('POSTGRES_PORT', '')
    # }
def create_database(conn_params, dbname, extension=None):
    try:
        # Creating the database here
        conn = psycopg2.connect(dbname='postgres', **conn_params)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(dbname)))
        print(f"Database '{dbname}' created successfully.")
        cursor.close()
        conn.close()

        # Connecting to the newly created database
        conn = psycopg2.connect(database=dbname, **conn_params)
        conn.autocommit = True
        cursor = conn.cursor()

        # Add the extension if provided. We are going to be working with postgis database.
        if extension:
            cursor.execute(sql.SQL("CREATE EXTENSION IF NOT EXISTS {}").format(sql.Identifier(extension)))
            print(f"{extension} extension added to '{dbname}' successfully.")

        cursor.close()
        conn.close()

    except psycopg2.Error as e:
        print(f"Error: {e}")
