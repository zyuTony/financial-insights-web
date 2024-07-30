import os
import json
from dotenv import load_dotenv 
from binance.client import Client
import pandas as pd
from datetime import datetime
import time
from requests.exceptions import ReadTimeout, ConnectionError
from tqdm import tqdm 
from utils.bn_utils import *
from utils.avan_utils import *
from utils.calc_utils import *

'''load env'''
load_dotenv()
bn_api_key = os.getenv('BINANCE_API')  
bn_api_secret = os.getenv('BINANCE_SECRET')  
cmc_api_key = os.getenv('CMC_API')  
avan_api_key = os.getenv('ALPHA_VANTAGE_FREE_API') 

'''BN->JSON'''
start_date='1 Jan, 2020'
end_date='1 July, 2024'
top_n_coins=10
interval = Client.KLINE_INTERVAL_1DAY
interval_name = '1DAY'

bn_pull_top_coins_hist_price_json(cmc_api_key, bn_api_key, bn_api_secret, start_date, end_date, interval, interval_name, top_n_coins)

'''AVAN->JSON'''
top_n_stocks = 1
interval = 'DAILY'
avan_pull_top_stocks_hist_price_json(avan_api_key, interval, top_n_stocks)

'''
JSON->calculate rolling coint -> calculate signal
'''
get_multi_pairs_rolling_coint(config.COIN_PRICE_CSV, config.ROLLING_COINT_TOP_N, config.ROLLING_COINT_COIN_CHECKPOINT_FILE, config.COIN_COINT_RESULT_CSV)



