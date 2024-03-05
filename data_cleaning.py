import pandas as pd
import numpy as np
from sqlalchemy import create_engine, inspect
import psycopg2
from data_extraction import DataExtractor
from database_utils import DatabaseConnector

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


class DataCleaning:
    def __init__(self):
        pass

    
    def clean_user_data(self, legacy_users_table):
        try:
            legacy_users_table.replace('NULL', np.NaN, inplace=True)
            legacy_users_table.dropna(subset=['date_of_birth', 'email_address', 'user_uuid'], how='any', axis=0, inplace=True)

            legacy_users_table['date_of_birth'] = pd.to_datetime(legacy_users_table['date_of_birth'], errors = 'ignore')
            legacy_users_table['join_date'] = pd.to_datetime(legacy_users_table['join_date'], errors ='coerce')
            legacy_users_table = legacy_users_table.dropna(subset=['join_date'])

            # Use .loc to explicitly modify the DataFrame
            legacy_users_table.loc[:, 'phone_number'] = legacy_users_table['phone_number'].str.replace('/W', '')
            legacy_users_table = legacy_users_table.drop_duplicates(subset=['email_address'])
            
            legacy_users_table.drop(legacy_users_table.columns[0], axis=1, inplace=True)
            legacy_users_table.to_csv("users.csv")
            return legacy_users_table 
        except Exception as e:
            print(f"Error cleaning user data: {e}")
            return None

    
    def clean_card_data(self, card_data_table):
        try:
            card_data_table.replace('NULL', np.NaN, inplace=True)
            card_data_table.dropna(subset=['card_number'], how='any', axis=0, inplace=True)
            card_data_table = card_data_table[~card_data_table['card_number'].str.contains('[a-zA-Z?]', na=False)]
            return card_data_table
        except Exception as e:
            print(f"Error cleaning card data: {e}")
            return None
    
    def clean_store_data(self, store_data):
        try:
            store_data = store_data.reset_index(drop=True)
            store_data.replace('NULL', np.NaN, inplace=True)
            store_data['opening_date'] = pd.to_datetime(store_data['opening_date'], errors ='coerce')
            store_data.loc[[31, 179, 248, 341, 375], 'staff_numbers'] = [78, 30, 80, 97, 39] # individually replaces values that have been inccorectly including text
            store_data['staff_numbers'] = pd.to_numeric(store_data['staff_numbers'], errors='coerce')
            store_data.dropna(subset=['staff_numbers'], axis=0, inplace=True)
            store_data['continent'] = store_data['continent'].str.replace('eeEurope', 'Europe').str.replace('eeAmerica', 'America')
            return store_data
        except Exception as e:
            print(f"Error cleaning store data: {e}")
            return None

    def convert_product_data(self, x):
        try:
            if 'kg' in x:
                x = x.replace('kg', '')
                x = float(x)

            elif 'ml' in x:
                x = x.replace('ml', '')
                x = float(x)/1000

            elif 'g' in x:
                x = x.replace('g', '')
                x = float(x)/1000

            elif 'lb' in x:
                x = x.replace('lb', '')
                x = float(x)*0.453591

            elif 'oz' in x:
                x = x.replace('oz', '')
                x = float(x)*0.0283495   
            return x
        except Exception as e:
            print(f"Error converting product data: {e}")
            return None

    def clean_product_data(self, data):
        try:
            data.replace('NULL', np.NaN, inplace=True)
            data['date_added'] = pd.to_datetime(data['date_added'], errors ='coerce')
            data.dropna(subset=['date_added'], how='any', axis=0, inplace=True)
            data['weight'] = data['weight'].apply(lambda x: x.replace(' .', ''))
            temp_cols = data.loc[data.weight.str.contains('x'), 'weight'].str.split('x', expand=True) # splits the weight column intop 2 temp columns split by the 'x'
            numeric_cols = temp_cols.apply(lambda x: pd.to_numeric(x.str.extract('(\d+\.?\d*)', expand=False)), axis=1) # Extracts the numeric values from the temp columns just created
            final_weight = numeric_cols.prod(axis=1) # Gets the product of the 2 numeric values
            data.loc[data.weight.str.contains('x'), 'weight'] = final_weight
            data['weight'] = data['weight'].apply(lambda x: str(x).lower().strip())
            data['weight'] = data['weight'].apply(lambda x: self.convert_product_data(x))
            data.drop(data.columns[0], axis=1, inplace=True) 
            return data
        except Exception as e:
            print(f"Error cleaning product data: {e}")
            return None

    def clean_order_data(self, data):
        try:
            data.drop("level_0", axis=1, inplace=True) 
            data.drop("1", axis=1, inplace=True) 
            data.drop(data.columns[0], axis=1, inplace=True)
            data.drop('first_name', axis=1, inplace=True)
            data.drop('last_name', axis=1, inplace=True)
            return data
        except Exception as e:
            print(f"Error cleaning order data: {e}")
            return None
    
    def clean_date_data(self, data):
        try:
            data['year'] = pd.to_numeric(data['year'], errors='coerce')
            data.dropna(subset=['year'], how='any', axis=0, inplace=True)
            return data
        except Exception as e:
            print(f"Error cleaning date data: {e}")
            return None


if __name__ == "__main__":
    # Creates class instances
    extractor = DataExtractor()
    connector = DatabaseConnector()
    cleaner = DataCleaning()

    #Connects to the database, extracts the data from the relational database on AWS, cleans the data and uploads the data to the db
    db_creds = connector.read_db_creds()
    engine = connector.init_db_engine(db_creds)
    if engine is None:
        print("Failed to initialize database engine. Exiting...")
        exit()

    table_names = connector.list_db_tables(engine)
    if table_names is None:
        print("Failed to retrieve table names from the database. Exiting...")
        exit()

    legacy_users_table = extractor.read_rds_table(table_names, 'legacy_users', engine)
    if legacy_users_table is not None:
        clean_legacy_users_table = cleaner.clean_user_data(legacy_users_table)
        if clean_legacy_users_table is not None:
            clean_legacy_users_table.to_csv('users.csv')
            connector.upload_to_db(clean_legacy_users_table, "dim_users", db_creds)
        else:
            print("Failed to clean user data. Exiting...")
            exit()
    else:
        print("Failed to retrieve user data from RDS. Exiting...")
        exit()

    # Extracts, cleans and uploads store data to db
    api_key = {'x-api-key': '....'}
    number_stores_endpoint = 'https://....'
    retrieve_store_endpoint = 'https://....'
    number_stores = extractor.list_number_of_stores(number_stores_endpoint, api_key)
    if number_stores is not None:
        store_data = extractor.retrieve_stores_data(number_stores, retrieve_store_endpoint, api_key)
        if store_data is not None:
            store_data.to_csv('store_outputs.csv')
            clean_store_data_table = cleaner.clean_store_data(store_data)
            if clean_store_data_table is not None:
                clean_store_data_table.to_csv('store_outputs.csv')
                connector.upload_to_db(clean_store_data_table, "dim_store_details", db_creds)
            else:
                print("Failed to clean store data. Exiting...")
                exit()
        else:
            print("Failed to retrieve store data from API. Exiting...")
            exit()
    else:
        print("Failed to retrieve number of stores from API. Exiting...")
        exit()

    # Extracts the product data
    product_data = extractor.extract_from_s3('s3://.....csv')
    if product_data is not None:
        cleaned_product_data = cleaner.clean_product_data(product_data)
        if cleaned_product_data is not None:
            cleaned_product_data.to_csv('product.csv')
            connector.upload_to_db(cleaned_product_data, 'dim_products', db_creds)
        else:
            print("Failed to clean product data. Exiting...")
            exit()
    else:
        print("Failed to retrieve product data from S3. Exiting...")
        exit()

    # Order table data
    orders_table = extractor.read_rds_table(table_names, 'orders_table', engine)
    if orders_table is not None:
        clean_orders_table = cleaner.clean_order_data(orders_table)
        if clean_orders_table is not None:
            clean_orders_table.to_csv('orders.csv')
            connector.upload_to_db(clean_orders_table, "orders_table", db_creds)
        else:
            print("Failed to clean order data. Exiting...")
            exit()
    else:
        print("Failed to retrieve order data from RDS. Exiting...")
        exit()

    # Date data
    date_data = extractor.extract_from_s3('.....json')
    if date_data is not None:
        clean_date_data = cleaner.clean_date_data(date_data)
        if clean_date_data is not None:
            clean_date_data.to_csv('date.csv')
            connector.upload_to_db(clean_date_data, "dim_date_times", db_creds)
        else:
            print("Failed to clean date data. Exiting...")
            exit()
    else:
        print("Failed to retrieve date data from S3. Exiting...")
        exit()
