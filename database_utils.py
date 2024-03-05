import pandas as pd
import numpy as np
import yaml
from sqlalchemy import create_engine, inspect
import psycopg2
import os

class DatabaseConnector:
    def __init__(self):
        pass

    def read_db_creds(self):
        try:
            with open("db_creds.yaml", "r") as f:
                db_creds = yaml.safe_load(f)
            if db_creds is None:
                raise ValueError("Failed to load database credentials from YAML file.")
            print("Database credentials loaded successfully.")
            return db_creds
        except FileNotFoundError:
            print("Error: db_creds.yaml file not found.")
            return None
        except Exception as e:
            print(f"Error reading database credentials: {e}")
            return None

    def init_db_engine(self, db_creds):
        try:
            engine = create_engine(f"{db_creds['RDS_DATABASE_TYPE']}+{db_creds['DB_API']}://{db_creds['RDS_USER']}:{db_creds['RDS_PASSWORD']}@{db_creds['RDS_HOST']}:{db_creds['RDS_PORT']}/{db_creds['RDS_DATABASE']}")
            engine.connect()
            print("Database engine initialized successfully.")
            return engine
        except Exception as e:
            print(f"Error initializing database engine: {e}")
            return None

    def list_db_tables(self, engine):
        try:
            inspector = inspect(engine)
            table_names = inspector.get_table_names()
            print("Database tables listed successfully.")
            return table_names
        except Exception as e:
            print(f"Error listing database tables: {e}")
            return None

    def upload_to_db(self, data_frame, table_name, db_creds):
        try:
            local_engine = create_engine(f"{db_creds['LOCAL_DATABASE_TYPE']}+{db_creds['LOCAL_DB_API']}://{db_creds['LOCAL_USER']}:{db_creds['LOCAL_PASSWORD']}@{db_creds['LOCAL_HOST']}:{db_creds['LOCAL_PORT']}/{db_creds['LOCAL_DATABASE']}")
            local_engine.connect()
            data_frame.to_sql(table_name, local_engine, if_exists='replace')
            print(f"Data uploaded to {table_name} successfully.")
        except Exception as e:
            print(f"Error uploading data to database: {e}")



