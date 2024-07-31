import os
import psycopg2
from psycopg2 import OperationalError
from psycopg2.extras import execute_values
from datetime import datetime, timezone
from utils.db_utils import *
import json
from tqdm import tqdm 

def connect_to_db(DB_NAME, DB_HOST, DB_USERNAME, DB_PASSWORD):
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USERNAME,
            password=DB_PASSWORD)
        print(f"Connected to {DB_HOST} {DB_NAME}!")
        return conn
    except OperationalError as e:
        print(f"{e}")
        return None

'''
Table Creations
'''
def create_stock_historical_price_table(conn):
    cursor = conn.cursor()
    try:
        create_table_query = """
        CREATE TABLE IF NOT EXISTS stock_historical_price (
            id SERIAL PRIMARY KEY,
            symbol VARCHAR(10) NOT NULL,
            date TIMESTAMPTZ NOT NULL,
            open NUMERIC NOT NULL,
            high NUMERIC NOT NULL,
            low NUMERIC NOT NULL,
            close NUMERIC NOT NULL,
            volume BIGINT NOT NULL,
            UNIQUE (symbol, date)
        );
        """
        cursor.execute(create_table_query)
        conn.commit()
        print(f"stock_historical_price created successfully.")
    except Exception as e:
        print(f"Failed to create table: {str(e)}")
        conn.rollback()
    finally:
        cursor.close()

def create_coin_historical_price_table(conn):
    cursor = conn.cursor()
    try:
        create_table_query = """
        CREATE TABLE IF NOT EXISTS coin_historical_price (
            id SERIAL PRIMARY KEY,
            symbol VARCHAR(10) NOT NULL,
            date TIMESTAMPTZ NOT NULL,
            open NUMERIC NOT NULL,
            high NUMERIC NOT NULL,
            low NUMERIC NOT NULL,
            close NUMERIC NOT NULL,
            volume NUMERIC NOT NULL,
            UNIQUE (symbol, date)
        );
        """
        cursor.execute(create_table_query)
        conn.commit()
        print(f"coin_historical_price created successfully.")
    except Exception as e:
        print(f"Failed to create table: {str(e)}")
        conn.rollback()
    finally:
        cursor.close()

def create_stock_pair_coint_table(conn):
    cursor = conn.cursor()
    try:
        create_table_query = """
        CREATE TABLE IF NOT EXISTS pairs_coint (
            date TIMESTAMPTZ NOT NULL,
            window_length INT NOT NULL,
            stock1 VARCHAR(50) NOT NULL,
            stock2 VARCHAR(50) NOT NULL,
            pvalue NUMERIC NOT NULL,
            UNIQUE (date, stock1, stock2)
        );
        """
        cursor.execute(create_table_query)
        conn.commit()
        print(f"stock_pairs_coint created successfully.")
    except Exception as e:
        print(f"Failed to create table: {str(e)}")
        conn.rollback()
    finally:
        cursor.close()

def create_coin_pair_coint_table(conn):
    cursor = conn.cursor()
    try:
        create_table_query = """
        CREATE TABLE IF NOT EXISTS coin_pairs_coint (
            date TIMESTAMPTZ NOT NULL,
            window_length INT NOT NULL,
            coin1 VARCHAR(50) NOT NULL,
            coin2 VARCHAR(50) NOT NULL,
            pvalue NUMERIC NOT NULL,
            UNIQUE (date, coin1, coin2)
        );
        """
        cursor.execute(create_table_query)
        conn.commit()
        print(f"coin_pairs_coint created successfully.")
    except Exception as e:
        print(f"Failed to create table: {str(e)}")
        conn.rollback()
    finally:
        cursor.close()

def create_stock_signal_table(conn):
    cursor = conn.cursor()
    try:
        create_table_query = """
        CREATE TABLE IF NOT EXISTS stock_signal (
            name1 VARCHAR(50) NOT NULL,
            name2 VARCHAR(50) NOT NULL,
            pvalue NUMERIC NOT NULL,
            ols_const NUMERIC NOT NULL,
            ols_coeff NUMERIC NOT NULL,
            r_squared NUMERIC NOT NULL,
            key_score NUMERIC NOT NULL,
            last_updated TIMESTAMPTZ NOT NULL,
            UNIQUE (name1, name2, last_updated)
        );
        """
        cursor.execute(create_table_query)
        conn.commit()
        print(f"stock_signal created successfully.")
    except Exception as e:
        print(f"Failed to create table: {str(e)}")
        conn.rollback()
    finally:
        cursor.close()

'''
Table insertion
'''
def insert_stock_historical_price_table(conn, file_path):
    cursor = conn.cursor()
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            
            symbol = data["Meta Data"]["2. Symbol"]
            time_series = data["Time Series (Daily)"]
            
            records = []
            for date_str, metrics in time_series.items():
                record = (
                    symbol,
                    datetime.strptime(date_str, '%Y-%m-%d'),
                    float(metrics["1. open"]),
                    float(metrics["2. high"]),
                    float(metrics["3. low"]),
                    float(metrics["4. close"]),
                    int(metrics["5. volume"])
                )
                records.append(record)
            
            # Insert data into the database
            insert_query = """
            INSERT INTO stock_historical_price (symbol, date, open, high, low, close, volume)
            VALUES %s
            ON CONFLICT DO NOTHING
            """
            execute_values(cursor, insert_query, records)
            conn.commit()
    except Exception as e:
        print(f"Failed to insert data from {file_path}: {e}")
        conn.rollback()
    finally:
        cursor.close()

def insert_coin_historical_price_table(conn, file_path):
    cursor = conn.cursor()
    try:
        symbol = os.path.splitext(os.path.basename(file_path))[0]
        with open(file_path, 'r') as file:
            data = json.load(file)
            extracted_data = []
            for entry in data:
                open_time = datetime.fromtimestamp(entry[0] / 1000, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
                open_price = entry[1]
                high_price = entry[2]
                low_price = entry[3]
                close_price = entry[4]
                volume = entry[5]
                extracted_data.append((symbol, open_time, open_price, high_price, low_price, close_price, volume))
            
            # Insert data into the database
            insert_query = """
            INSERT INTO coin_historical_price (symbol, date, open, high, low, close, volume)
            VALUES %s
            ON CONFLICT DO NOTHING
            """
            execute_values(cursor, insert_query, extracted_data)
            conn.commit()
    except Exception as e:
        print(f"Failed to insert data from {file_path}: {e}")
        conn.rollback()
    finally:
        cursor.close()

def insert_stock_pair_coint_table(conn, csv_as_tuple):
    cursor = conn.cursor()
    insert_query = """
    INSERT INTO stock_pairs_coint (date, window_length, stock1, stock2, pvalue)
    VALUES %s
    ON CONFLICT DO NOTHING
    """
    try:      
        chunk_size = 100
        for i in tqdm(range(0, len(csv_as_tuple), chunk_size), desc="Inserting data"):
            execute_values(cursor, insert_query, csv_as_tuple[i:i+chunk_size])
        conn.commit()
    except Exception as e:
        print(f"Failed to insert data: {e}")
        conn.rollback()
    finally:
        cursor.close()

def insert_coin_pair_coint_table(conn, csv_as_tuple):
    cursor = conn.cursor()
    insert_query = """
    INSERT INTO coin_pairs_coint (date, window_length, coin1, coin2, pvalue)
    VALUES %s
    ON CONFLICT DO NOTHING
    """
    try:      
        chunk_size = 100
        for i in tqdm(range(0, len(csv_as_tuple), chunk_size), desc="Inserting data"):
            execute_values(cursor, insert_query, csv_as_tuple[i:i+chunk_size])
        conn.commit()
    except Exception as e:
        print(f"Failed to insert data: {e}")
        conn.rollback()
    finally:
        cursor.close()

def insert_stock_signal_table(conn, csv_as_tuple):
    cursor = conn.cursor()
    insert_query = """
    INSERT INTO stock_signal (name1, name2, pvalue, ols_const, ols_coeff, r_squared, key_score, last_updated)
    VALUES %s
    ON CONFLICT DO NOTHING
    """
    try:      
        chunk_size = 100
        for i in tqdm(range(0, len(csv_as_tuple), chunk_size), desc="Inserting data"):
            execute_values(cursor, insert_query, csv_as_tuple[i:i+chunk_size])
        conn.commit()
    except Exception as e:
        print(f"Failed to insert data: {e}")
        conn.rollback()
    finally:
        cursor.close()