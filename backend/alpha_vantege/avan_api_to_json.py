import requests
import os
from dotenv import load_dotenv
import json
import pandas as pd
from sqlalchemy import create_engine
import time

load_dotenv()
api_key = os.getenv('ALPHA_VANTAGE_PREM_API') 

 
def pull_stock_data(timeframe, ticker):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_{timeframe}&symbol={ticker}&outputsize=full&apikey={api_key}'

    response = requests.get(url)
    json_file_path = f'../data/avan_data/{ticker}_{timeframe}.json'
    if response.status_code == 200:
        data = response.json()
        with open(json_file_path, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"{ticker} saved to json")
        return 1 
    else:
        print(f"Error fetching {ticker}: {response.status_code}")
        return -1

ticker_file = "../data/sec_stock_tickers.json"
with open(ticker_file, 'r') as file:
    data = json.load(file)
ticker = []
for key, value in data.items():
    ticker.append(value["ticker"])

timeframe = 'DAILY'
tickers = ticker[:1000]
checkpoint_file = '../data/avan_checkpoint.json'
if os.path.exists(checkpoint_file):
    with open(checkpoint_file, 'r') as file:
        checkpoint_data = json.load(file)
else:
    checkpoint_data = []
for ticker in tickers:
    if ticker in checkpoint_data:
        print(f"Skipping {ticker}, already downloaded.")
        continue
    status = pull_stock_data(timeframe, ticker)
    time.sleep(0.8)
    if status == 1:
        checkpoint_data.append(ticker)
        with open(checkpoint_file, 'w') as file:
            json.dump(checkpoint_data, file, indent=4)
print('Download completed! :)')  