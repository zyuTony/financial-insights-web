import os
import json
from dotenv import load_dotenv 
from binance.client import Client
import pandas as pd
from datetime import datetime
import time
from requests.exceptions import ReadTimeout, ConnectionError
from utlis import *
from tqdm import tqdm 

load_dotenv()
api_key = os.getenv('BINANCE_API')  
api_secret = os.getenv('BINANCE_SECRET')  

start_date='1 Jan, 2023'
end_date='1 July 2024'
ticker = 'TONUSDT'
interval = Client.KLINE_INTERVAL_30MINUTE

client = Client(api_key, api_secret)


def get_ticker_by_interval_name(client, coin_id, interval, start_date, end_date):
    
    retry_count = 0
    max_retries = 5
    
    while retry_count < max_retries:
        try:
            # Get data and save to JSON
            ticker_data = client.get_historical_klines(coin_id, interval, start_date, end_date)
            with open(f'./data/{coin_id}.json', 'w') as file:
                json.dump(ticker_data, file, indent=4)
                print(f'Downloaded {coin_id}')
            break  
        
        except (ReadTimeout, ConnectionError) as e:
            retry_count += 1
            wait_time = 2 ** retry_count  # Exponential backoff
            print(f"Error occurred while downloading {coin_id}: {e}")
            print(f"Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
        
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break  # Break the loop on other exceptions

    print(f"{coin_id} download completed.")

get_ticker_by_interval_name(client, ticker, interval, start_date, end_date)