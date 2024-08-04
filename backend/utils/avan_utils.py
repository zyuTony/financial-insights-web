import requests
import os
import json
import time
import config

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


def avan_pull_top_stocks_hist_price_json(avan_api_key, interval, top_n_stocks):
    # get top stock tickers from SEC file
    with open(config.SEC_STOCK_TICKERS, 'r') as file:
        data = json.load(file)
    ticker = []
    for key, value in data.items():
        ticker.append(value["ticker"])

    tickers = ticker[:top_n_stocks]
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


def avan_pull_top_stocks_overview_json(avan_api_key, top_n_stocks):
    # get top stock tickers from SEC file
    with open(config.SEC_STOCK_TICKERS, 'r') as file:
        data = json.load(file)
    ticker = []
    for key, value in data.items():
        ticker.append(value["ticker"])

    tickers = ticker[:top_n_stocks]
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
