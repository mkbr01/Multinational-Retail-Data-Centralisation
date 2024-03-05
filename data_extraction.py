import pandas as pd
import numpy as np
import yaml
from sqlalchemy import create_engine, inspect
import psycopg2
import tabula as tb
import requests
import json
import boto3
import os

os.environ['AWS_ACCESS_KEY_ID'] = '....'
os.environ['AWS_SECRET_ACCESS_KEY'] = '.....'


class DataExtractor:
    def __init__(self):
        pass

    def read_rds_table(self, table_names, table_name, engine):
        try:
            engine = engine.connect()
            data = pd.read_sql_table(table_name, engine)
            return data
        except Exception as e:
            print(f"Error reading RDS table {table_name}: {e}")
            return None

    def retrieve_pdf_data(self, link):
     try:
        pdf_path = link
        df = tb.read_pdf(pdf_path, pages="all")
        df = pd.concat(df)
        df = df.reset_index(drop=True)
        # Convert columns to numeric without passing errors parameter
        for c in df.columns:
            df[c] = pd.to_numeric(df[c])
        return df
     except Exception as e:
        print(f"Error retrieving PDF data: {e}")
        return None

    def list_number_of_stores(self, endpoint, api_key):
        try:
            response = requests.get(endpoint, headers=api_key)
            content = response.text
            result = json.loads(content)
            number_stores = result['number_stores']
            return number_stores
        except Exception as e:
            print(f"Error listing number of stores: {e}")
            return None

    def retrieve_stores_data(self, number_stores, endpoint, api_key):
        try:
            data = []
            for store in range(0, number_stores):
                response = requests.get(f'{endpoint}{store}', headers=api_key)
                content = response.text
                result = json.loads(content)
                data.append(result)
            df = pd.DataFrame(data)
            return df
        except Exception as e:
            print(f"Error retrieving stores data: {e}")
            return None

    def extract_from_s3(self, s3_address):
        try:
            s3 = boto3.resource('s3')
            if 's3://' in s3_address:
                s3_address = s3_address.replace('s3://', '')
            elif 'https' in s3_address:
                s3_address = s3_address.replace('https://', '')
            bucket_name, file_key = s3_address.split('/', 1)
            bucket_name = 'data-handling-public'
            obj = s3.Object(bucket_name, file_key)
            body = obj.get()['Body']
            if 'csv' in file_key:
                df = pd.read_csv(body)
            elif '.json' in file_key:
                df = pd.read_json(body)
            df = df.reset_index(drop=True)
            return df
        except Exception as e:
            print(f"Error extracting data from S3: {e}")
            return None


extractor = DataExtractor()
