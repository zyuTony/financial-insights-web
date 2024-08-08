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

'''STEPS
1. clean up the checkpoint files to restart download
2. json file downloaded. 
   est time: for 1000 stocks
     avan data     13 minutes
     avan overview 13 minutes
     binance stock 13 minutes
3. coint data run. 
   est time: for n stocks n*(n-1)/2 pairs
   each pair takes 6 sec. easily take 30 days
    
'''
# load env var 
load_dotenv()
bn_api_key = os.getenv('BINANCE_API')  
bn_api_secret = os.getenv('BINANCE_SECRET')  
cmc_api_key = os.getenv('CMC_API')  
avan_api_key = os.getenv('ALPHA_VANTAGE_PREM_API') 

'''BN->JSON'''
start_date='1 Jan, 2020'
end_date='6 Aug, 2024'
top_n_coins=200
interval = Client.KLINE_INTERVAL_1DAY
interval_name = '1DAY'

bn_pull_top_coins_hist_price_json(cmc_api_key, bn_api_key, bn_api_secret, start_date, end_date, interval, interval_name, top_n_coins)

'''AVAN->JSON'''
top_n_stocks = 1000
interval = 'DAILY'
avan_pull_top_stocks_hist_price_json(avan_api_key, interval, top_n_stocks)
avan_pull_top_stocks_overview_json(avan_api_key, top_n_stocks)



 