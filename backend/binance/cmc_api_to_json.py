'''
1. Get data from CMC API
2. Turn into json
3. run cointegration tests for all possible pair for chosen intervals
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
from backend.utils.cmc_utils import * 
import time


load_dotenv()
api_key = os.getenv('CMC_API') 

# ------ EXTRACT JSON
# --- pull raw historical price data from api and save as json
data = pull_coin_list(100, api_key, 'top_crypto_tickers.json')
ids, symbols= coin_list_json_to_str('top_crypto_tickers.json')
ids, symbols= coin_list_json_to_array('top_crypto_tickers.json')
print(ids)
intervals = ['daily','4h', '1h'] 

all_cointegration_results = []
for interval in intervals:
    combined_coin_data = pd.DataFrame()
    print(f'Begin for interval {interval}')
    for coin_id in ids:
        # download api data
        data = pull_historical_price(coin_id, api_key, f'./hist_data/hist_price_{coin_id}_{interval}.json', interval, start_date='2023-08-01', end_date='2024-07-01')
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
        time.sleep(2.1)

    # Pivot the combined data for all coins
    df_pivot = combined_coin_data.pivot(index='timestamp', columns='symbol', values='price')
    df_pivot = df_pivot.fillna(0)

    # Run cointegration test
    cointegration_results = run_cointegration_tests(df_pivot)
    cointegration_df = pd.DataFrame(cointegration_results)
    cointegration_df = cointegration_df.add_prefix(interval + '_')
    all_cointegration_results.append(cointegration_df)

# Combine all results for all intervals by columns
final_cointegration_df = pd.concat(all_cointegration_results, axis=1)

print(final_cointegration_df)
final_cointegration_df.to_csv('cointegration_results_1_4_12h.csv')

 