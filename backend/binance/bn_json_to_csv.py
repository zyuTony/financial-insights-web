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

folder = '../data/binance_data_2'
output_file = '../data/binance_agg_data.csv'

df_list = []
file_list = glob(folder + "/*.json")
file_list.sort(key=os.path.getctime)

for fname in tqdm(file_list):
    filename = os.path.splitext(os.path.basename(fname))[0]
    with open(fname, 'r') as file:
        data = json.load(file)
    temp_data = []
    for entry in data:
        open_time = pd.to_datetime(entry[0], unit='ms', utc=True).strftime('%Y-%m-%d %H:%M:%S')
        close_price = entry[4]
        temp_data.append([open_time, close_price])

    temp_df = pd.DataFrame(temp_data, columns=['date', filename])
    temp_df['date'] = pd.to_datetime(temp_df['date'])
    df_list.append(temp_df)
    print(f'\nCompleted {filename}')

# clean and output as csv file
df = pd.concat(df_list, axis=1)
df = df.loc[:, ~df.columns.duplicated()]
df = df.dropna(axis=1, how='all')
df.fillna(-1, inplace=True)
df.to_csv(output_file, index=False)
print(f"Data has been written to {output_file}")
 
