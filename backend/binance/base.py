'''
LIMITS

1. get list of id for coins by mc
2. get historical price by hourly 
3. run backtest on eth/btc hourly

'''
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

# load the env variables
load_dotenv()
api_key = os.getenv('BINANCE_API')  
api_secret = os.getenv('BINANCE_SECRET')  

# client = Client(api_key, api_secret)

# retrieve list of stock data in small intervals
start_date='1 Jan, 2023'
end_date='1 July 2024'
intervals = ['30MINUTES'] 

# get_all_ticker_by_intervals(client, intervals, start_date, end_date)

top_20_list=["BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT", "DOGEUSDT", "SOLUSDT", "MATICUSDT", "DOTUSDT", "LTCUSDT", "TRXUSDT", "AVAXUSDT", "SHIBUSDT", "LINKUSDT", "ATOMUSDT", "XMRUSDT"]

# agg_data_to_csv("./coin_prices.csv", 15)
agg_data_to_csv("./top20_coin_prices.csv", top_20_list)


# run cointegration on data pairs 
df = pd.read_csv('./top20_coin_prices.csv')
df = df.loc[:, ~df.columns.duplicated()]
df = df.dropna(axis=1, how='all')
df = df.fillna(0)
df = df.drop(df.columns[0], axis=1)

cointegration_results = run_cointegration_tests(df)
cointegration_df = pd.DataFrame(cointegration_results)
cointegration_df = cointegration_df.add_prefix('30min' + '_')
cointegration_df.to_csv('./top20_cointregration.csv')

 