from glob import glob
from requests import Request, Session
import json
import pandas as pd
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from statsmodels.tsa.stattools import coint
import statsmodels.api as sm
import os
import time
from requests.exceptions import ReadTimeout, ConnectionError
from tqdm import tqdm 
 
folder = f'../data/avan_data'
output_file = '../data/stock_agg_data.csv'

df_list = []
file_list = glob(folder + "/*.json")
file_list.sort(key=os.path.getctime)

for fname in file_list:
    try:
        with open(fname, 'r') as file:
            data = json.load(file)
        
        temp_data = []
        ticker_name = data['Meta Data']['2. Symbol']
        time_series = data["Time Series (Daily)"]
        
        for date, values in time_series.items():
            close_price = values["4. close"]
            temp_data.append([date, close_price])
        
        temp_df = pd.DataFrame(temp_data, columns=['date', ticker_name])
        temp_df['date'] = pd.to_datetime(temp_df['date'])
        df_list.append(temp_df)
        print(f'Completed {ticker_name}')
    except Exception as e:
        print(f"{ticker_name}: {e}")
        continue

# Clean and output as CSV file
try:
    df = pd.concat(df_list, axis=1)
    df = df.loc[:, ~df.columns.duplicated()]
    df = df.dropna(axis=1, how='all')
    df.fillna(-1, inplace=True)
    df = df.sort_values(by='date')
    df.to_csv(output_file, index=False)
    print(f"Data has been written to {output_file}")
except Exception as e:
    print(f"An error occurred while processing the DataFrame: {e}")