import requests
import os
from dotenv import load_dotenv
import json
import pandas as pd
from sqlalchemy import create_engine


ticker = 'SPY'
timeframe = 'DAILY'
csv_file_path = f'../data/{ticker}_{timeframe}_data.csv'
json_file_path = f'../data/{ticker}_{timeframe}_data.json'

load_dotenv()
api_key = os.getenv('ALPHA_VANTAGE_FREE_API') 

if api_key is None:
    raise ValueError("API key is missing. Please set it in the .env file.")
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_{timeframe}&symbol={ticker}&outputsize=full&apikey={api_key}'

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Data saved to {json_file_path}")
 
    # different for every timeframe - for DAILY only
    time_series = data.get("Time Series (Daily)", {})
    df = pd.DataFrame.from_dict(time_series, orient='index')
    df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'Date'}, inplace=True)

    # change for strat testing
    df = df[['Date', 'Close']]
    df.columns = ['date', 'price']
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by='date')
    df.to_csv(csv_file_path, index=False)
    print(f"Data saved to {csv_file_path}")
else:
    print(f"Error fetching data: {response.status_code}")
 