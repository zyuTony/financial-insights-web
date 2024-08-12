import requests
import os
import json
import time
import config
import pandas as pd

def avan_single_json_append_to_csv(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
        symbol = data["Meta Data"]["2. Symbol"]
        daily_data = data["Time Series (Daily)"]
        
        # Create a dataframe with Date and Close price
        df = pd.DataFrame({
            'Date': list(daily_data.keys()),
            symbol: [daily_data[date]["4. close"] for date in daily_data]
        })
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    
def avan_pull_stock_data(interval, ticker, avan_api_key):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_{interval}&symbol={ticker}&outputsize=full&apikey={avan_api_key}'

    response = requests.get(url)
    json_file_path = config.AVAN_JSON_PATH + f'/avan_data_{interval}/{ticker}_{interval}.json'
    if response.status_code == 200:
        data = response.json()
        with open(json_file_path, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"{ticker} saved to json")
        return 1 
    else:
        print(f"Error fetching {ticker}: {response.status_code}")
        return -1

def avan_pull_stock_overview(ticker, avan_api_key):
    url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={avan_api_key}'

    response = requests.get(url)
    json_file_path = config.AVAN_JSON_PATH + f'/avan_stock_overview/{ticker}.json'
    if response.status_code == 200:
        data = response.json()
        with open(json_file_path, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"{ticker} saved to json")
        return 1 
    else:
        print(f"Error fetching {ticker}: {response.status_code}")
        return -1

def avan_pull_stocks_hist_price_to_json(avan_api_key, interval, tickers):
    if os.path.exists(config.AVAN_CHECKPOINT_FILE):
        with open(config.AVAN_CHECKPOINT_FILE, 'r') as file:
            checkpoint_data = json.load(file)
    else:
        checkpoint_data = []
    for ticker in tickers:
        if ticker in checkpoint_data:
            print(f"Skipping {ticker}, already downloaded.")
            continue
        status = avan_pull_stock_data(interval, ticker, avan_api_key)
        time.sleep(config.AVAN_SLEEP_TIME)
        if status == 1:
            checkpoint_data.append(ticker)
            with open(config.AVAN_CHECKPOINT_FILE, 'w') as file:
                json.dump(checkpoint_data, file, indent=4)
    print('Download completed! :)')  


def avan_pull_stocks_overview_json(avan_api_key, tickers):
    if os.path.exists(config.AVAN_OVERVIEW_CHECKPOINT_FILE):
        with open(config.AVAN_OVERVIEW_CHECKPOINT_FILE, 'r') as file:
            checkpoint_data = json.load(file)
    else:
        checkpoint_data = []
    for ticker in tickers:
        if ticker in checkpoint_data:
            print(f"Skipping {ticker} overview, already downloaded.")
            continue
        status = avan_pull_stock_overview(ticker, avan_api_key)
        time.sleep(config.AVAN_SLEEP_TIME)
        if status == 1:
            checkpoint_data.append(ticker)
            with open(config.AVAN_OVERVIEW_CHECKPOINT_FILE, 'w') as file:
                json.dump(checkpoint_data, file, indent=4)
    print('Download completed! :)')  
