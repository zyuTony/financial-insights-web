import os
import json
from dotenv import load_dotenv 
from binance.client import Client
import pandas as pd
from datetime import datetime
import time
from requests.exceptions import ReadTimeout, ConnectionError
from backend.binance.bn_utlis import *
from cmc_utlis import *
from tqdm import tqdm 

load_dotenv()
binance_api_key = os.getenv('BINANCE_API')  
binance_api_secret = os.getenv('BINANCE_SECRET')  
cmc_api_key = os.getenv('CMC_API')  

# CMC
top_n_coins=300
data = pull_coin_list(top_n_coins, cmc_api_key)
_, symbols= coin_list_json_to_array(data)
coin_ids = [symbol+'USDT' for symbol in symbols]
print(coin_ids)

# Binance
start_date='1 Jan, 2020'
end_date='1 July, 2024'
interval = Client.KLINE_INTERVAL_1DAY
client = Client(binance_api_key, binance_api_secret)

# pull data to json
checkpoint_file = '../data/binance_checkpoint.json'
if os.path.exists(checkpoint_file):
    with open(checkpoint_file, 'r') as file:
        checkpoint_data = json.load(file)
else:
    checkpoint_data = []

for coin_id in coin_ids:
    if coin_id in checkpoint_data:
        print(f"Skipping {coin_id}, already downloaded.")
        continue
    status = get_ticker_by_interval_name(client, coin_id, interval, start_date, end_date)
    if status == 1:
        checkpoint_data.append(coin_id)
        with open(checkpoint_file, 'w') as file:
            json.dump(checkpoint_data, file, indent=4)
print('Download completed! :)')