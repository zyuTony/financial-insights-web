from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects 

import time
import pandas as pd
import json
import os
from dotenv import load_dotenv 
import requests

from utils.cmc_utils import *
from utils.db_utils import *

from psycopg2.extras import execute_values

load_dotenv()
gc_api_key = os.getenv('GECKO_API') 
cmc_api_key = os.getenv('CMC_API')  

def pull_coin_list_ranking(api_key, page_num):
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=250&page={page_num}"
    headers = {
    "accept": "application/json",
    "x-cg-pro-api-key": gc_api_key
    }

    session = Session()
    session.headers.update(headers)

    try:
      response = session.get(url)
      data = response.json()
      return data
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)
      return -1
    
def get_unix_timestamp(date_str):
    return int(time.mktime(datetime.strptime(date_str, "%Y-%m-%d").timetuple()))

'''Get top coin by mc'''
# symbols_ranking = []
# for page_num in range(1, 6):
#     symbols_ranking.extend(pull_coin_list_ranking(gc_api_key, page_num))

# with open('./data/gecko_raw_data/mapping/top_symbol_by_mc.json', 'w') as file:
#     json.dump(symbols_ranking, file, indent=4)

with open('./data/gecko_raw_data/mapping/top_symbol_by_mc.json', 'r') as file:
    symbols_ranking = json.load(file)
 
ids = [item["id"] for item in symbols_ranking]
symbols = [item["symbol"].upper() for item in symbols_ranking]
print(ids, symbols)

start_date = '2018-03-01'
end_date = '2024-08-07'
unix_start = get_unix_timestamp(start_date)
unix_end = get_unix_timestamp(end_date)

'''DOWNLOAD DATA'''
max_days = 180
max_seconds = max_days * 24 * 60 * 60

for id, symbol in zip(ids, symbols):
    current_start = unix_start
    all_data = []
    
    while current_start < unix_end:
        current_end = min(current_start + max_seconds, unix_end)
        
        try:
            url = f"https://pro-api.coingecko.com/api/v3/coins/{id}/ohlc/range?vs_currency=usd&from={current_start}&to={current_end}&interval=daily"
            headers = {
                "accept": "application/json",
                "x-cg-pro-api-key": gc_api_key
            }
            
            response = requests.get(url, headers=headers)
            
            # Check if the response status code is 200 (OK)
            if response.status_code == 200:
                all_data.extend(response.json())  

                print(f"Downloaded data for {symbol} from {current_start} to {current_end}")
            else:
                print(f"Failed to download data for {symbol} from {current_start} to {current_end}: {response.status_code} {response.text}")
            
            current_start = current_end + 1
        except Exception as e:
            print(f"Exception occurred while downloading data for {symbol} from {current_start} to {current_end}: {e}")
            break
    
    # Save all collected data to one JSON file per coin
    with open(f'./data/gecko_raw_data/daily/{symbol}.json', 'w') as file:
        json.dump(all_data, file, indent=4)
    print(f"Saved full data for {symbol} to {symbol}.json")

'''CREATE TABLE'''
load_dotenv(override=True)
DB_USERNAME = os.getenv('RDS_USERNAME') 
DB_PASSWORD = os.getenv('RDS_PASSWORD') 
DB_HOST = os.getenv('RDS_ENDPOINT') 
DB_NAME = 'financial_data'

conn = connect_to_db(DB_NAME, DB_HOST, DB_USERNAME, DB_PASSWORD)
cursor = conn.cursor()

try:
    create_table_query = """
    CREATE TABLE IF NOT EXISTS cg_coin_hist_price (
        symbol VARCHAR(20) NOT NULL,
        date TIMESTAMPTZ NOT NULL,
        open NUMERIC NOT NULL,
        high NUMERIC NOT NULL,
        low NUMERIC NOT NULL,
        close NUMERIC NOT NULL,
        UNIQUE (symbol, date)
    );
    """
    cursor.execute(create_table_query)
    conn.commit()
    print(f"cg_coin_hist_price created successfully.")
except Exception as e:
    print(f"Failed to create table: {str(e)}")
    conn.rollback()
finally:
    cursor.close()

'''INSERT TO SQL DATABASE'''
alt_json_folder = './data/gecko_raw_data/daily'
for filename in os.listdir(alt_json_folder):
    if filename.endswith('.json'):
        file_path = os.path.join(alt_json_folder, filename)
        cursor = conn.cursor()
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                symbol = os.path.splitext(os.path.basename(file_path))[0]
                extracted_data = []
                seen_dates = set()
                for entry in data:
                    timestamp = entry[0]
                    open_price  = entry[1]
                    high = entry[2]
                    low = entry[3]
                    close = entry[4]
                    # Convert timestamp to a readable date format
                    date = pd.to_datetime(entry[0], unit='ms').strftime('%Y-%m-%d')
                     
                    if date not in seen_dates:
                        extracted_data.append([symbol, date, open_price, high, low, close])
                        seen_dates.add(date)
                
                # Insert data into the database
                insert_query = """
                INSERT INTO cg_coin_hist_price (symbol, date, open, high, low, close)
                VALUES %s
                ON CONFLICT (symbol, date)
                DO UPDATE SET
                    open = EXCLUDED.open,
                    high = EXCLUDED.high,
                    low = EXCLUDED.low,
                    close = EXCLUDED.close
                """
                execute_values(cursor, insert_query, extracted_data)
                conn.commit()
                print(f'Inserted {symbol} historical price')
        except Exception as e:
            print(f"Failed to insert data from {filename}: {e}")
            conn.rollback()
        finally:
            cursor.close()



def pull_coin_mapping_gecko(api_key):
    url = "https://api.coingecko.com/api/v3/coins/list"
    headers = {
    "accept": "application/json",
    "x-cg-pro-api-key": gc_api_key
    }

    session = Session()
    session.headers.update(headers)

    try:
      response = session.get(url)
      data = response.json()
      return data
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)
      return -1  


def fill_bn_missing_with_gecko():
    '''Get Id Symbol Mapping'''
    data = pull_coin_mapping_gecko(gc_api_key)
    with open('./data/gecko_raw_data/mapping/symbol_map.json', 'w') as file:
        json.dump(data, file, indent=4)

    '''check what else to download'''
    # Find current Binance data and Top 200 CMC coins. Download what we don't have.
    
    with open('./data/gecko_raw_data/mapping/symbol_map.json', 'r') as file:
        mapping = json.load(file)

    symbol_to_id = {item['symbol'].upper(): item['id'] for item in mapping}
    id_to_symbol = {item['id']: item['symbol'].upper() for item in mapping}

    bn_checkpoint = './data/checkpoints/binance_checkpoint.json'
    with open(bn_checkpoint, 'r') as file:
        bn_downloaded_symbols = json.load(file)

    bn_downloaded_symbols = [symbol.replace('USDT', '') for symbol in bn_downloaded_symbols]

    data = pull_coin_list(200, cmc_api_key)
    _, all_top_symbols= coin_list_json_to_array(data)

    # cleaning
    symbol_to_download = [symbol for symbol in all_top_symbols if symbol not in bn_downloaded_symbols]
    symbol_to_download = [symbol for symbol in symbol_to_download if symbol not in ['USDT', "USDC", "NFT"]]
    ids_to_download = [symbol_to_id[symbol.upper()] for symbol in symbol_to_download if symbol.upper() in symbol_to_id]

    '''DOWNLOAD DATA'''
    import requests
    for id in ids_to_download:
        time.sleep(2) # limited api 
        try:
            url = f"https://api.coingecko.com/api/v3/coins/{id}/market_chart?vs_currency=usd&days=360"

            headers = {"accept": "application/json",
                    "x-cg-pro-api-key": gc_api_key}

            response = requests.get(url, headers=headers)
            data = response.json()
            symbol = id_to_symbol[id]
            with open(f'./data/gecko_raw_data/{symbol}.json', 'w') as file:
                json.dump(data, file, indent=4)
            print(f'downloaded {symbol}.json')
        except (Exception) as e:
            print(f"fail download {symbol}: {e}")
            continue

    '''INSERT TO SQL DATABASE'''
    load_dotenv(override=True)
    DB_USERNAME = os.getenv('RDS_USERNAME') 
    DB_PASSWORD = os.getenv('RDS_PASSWORD') 
    DB_HOST = os.getenv('RDS_ENDPOINT') 
    DB_NAME = 'financial_data'

    conn = connect_to_db(DB_NAME, DB_HOST, DB_USERNAME, DB_PASSWORD)
        
    alt_json_folder = './data/gecko_raw_data'
    for filename in os.listdir(alt_json_folder):
        if filename.endswith('.json'):
            file_path = os.path.join(alt_json_folder, filename)
            cursor = conn.cursor()
            try:
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    symbol = os.path.splitext(os.path.basename(file_path))[0]
                    symbol = symbol+'USDT'
                    extracted_data = []
                    for entry in data["prices"]:
                        timestamp = entry[0]
                        price = entry[1]
                        # Convert timestamp to a readable date format
                        date = pd.to_datetime(entry[0], unit='ms').strftime('%Y-%m-%d')
                        # Append the transformed data to the list
                        extracted_data.append([symbol, date, -1,-1,-1,price,-1])
                    extracted_data = extracted_data[:-1]
                    
                    # Insert data into the database
                    insert_query = """
                    INSERT INTO coin_historical_price (symbol, date, open, high, low, close, volume)
                    VALUES %s
                    ON CONFLICT (symbol, date)
                    DO UPDATE SET
                        open = EXCLUDED.open,
                        high = EXCLUDED.high,
                        low = EXCLUDED.low,
                        close = EXCLUDED.close,
                        volume = EXCLUDED.volume
                    """
                    execute_values(cursor, insert_query, extracted_data)
                    conn.commit()
                    print(f'Inserted {symbol} historical price')
            except Exception as e:
                print(f"Failed to insert data from {filename}: {e}")
                conn.rollback()
            finally:
                cursor.close()

        