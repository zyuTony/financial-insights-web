 #This example uses Python 2.7 and the python-request library.
'''
To ensure you always target the cryptocurrency you expect, use our permanent CoinMarketCap IDs. These IDs are used reliably by numerous mission critical platforms and never change.
Just call our /cryptocurrency/map endpoint to receive a list of all active currencies mapped to the unique id property. This map also includes other typical identifiying properties like name, symbol and platform token_address that can be cross referenced. In cryptocurrency calls you would then send, for example id=1027, instead of symbol=ETH
'''
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import requests
import os
from dotenv import load_dotenv
import json
import pandas as pd
from sqlalchemy import create_engine
from cmc_utlis import * 
import time

'''
1. get the cointegration of all coins historical data
    a. get historical daily/weekly price for top 10 MC coins
    b. sample different time frame to test to make sure each is good
    c. calculate cointegration for the 1000 combos

2. repeat above for 15m, 2h, 4h, 1D  
'''

load_dotenv()
api_key = os.getenv('CMC_API') 
username = os.getenv('RDS_USERNAME') 
password = os.getenv('RDS_PASSWORD') 
endpoint = os.getenv('RDS_ENDPOINT') 

db_name = 'financial_data' 

# ------ EXTRACT JSON
# --- pull raw historical price data from api and save as json
data = pull_coin_list(100, api_key, 'top_crypto_tickers.json')
ids, symbols= coin_list_json_to_array('top_crypto_tickers.json')
print(ids)
interval = '24h' 

all_cointegration_results = []
 
combined_coin_data = pd.DataFrame() 
for coin_id in ids:
    try:
        # Extract data
        with open('./hist_data/hist_price_{}_{}.json'.format(coin_id, interval), 'r') as file:
            data = json.load(file)

        coins_data = []
        for quote in data['data'][coin_id]['quotes']:
            coins_data.append({
                'id': coin_id,
                'symbol': data['data'][coin_id]['symbol'],
                'timestamp': quote['timestamp'],
                'price': quote['quote']['USD']['price']
            }) 
        df = pd.DataFrame(coins_data)
        combined_coin_data = pd.concat([combined_coin_data, df], axis=0)
    except FileNotFoundError:
        print(f"Data file for coin ID {coin_id} not found.")
    except KeyError as e:
        print(f"Key error for coin ID {coin_id}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred for coin ID {coin_id}: {e}")

print(combined_coin_data)
combined_coin_data.to_csv('coin_price.csv')

 