from requests import Request, Session
import json
import pandas as pd
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import datetime
from statsmodels.tsa.stattools import coint
import statsmodels.api as sm
import os
import time
from requests.exceptions import ReadTimeout, ConnectionError
from tqdm import tqdm 

def get_all_ticker_by_intervals(client, intervals, start_date, end_date):
    
    data = client.get_all_tickers()
    coin_ids = [item["symbol"] for item in data if item["symbol"].endswith("USDT")]

    checkpoint_file = '../data/binance_data_2/checkpoint.json'
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'r') as file:
            checkpoint_data = json.load(file)
    else:
        checkpoint_data = {interval: [] for interval in intervals}

    for interval in intervals:
        if interval not in checkpoint_data:
            checkpoint_data[interval] = []
        print(f"retrieve data for {interval}")

        for coin_id in coin_ids:
            if coin_id in checkpoint_data[interval]:
                print(f"Skipping {coin_id}, already downloaded.")
                continue
            
            retry_count = 0
            max_retries = 5
            
            while retry_count < max_retries:
                try:
                    # Get data and save to JSON
                    ticker_data = client.get_historical_klines(coin_id, Client.KLINE_INTERVAL_30MINUTE, start_date, end_date)
                    with open(f'./data/{coin_id}.json', 'w') as file:
                        json.dump(ticker_data, file, indent=4)
                        print(f'Downloaded {coin_id}')
                    
                    # Update checkpoint data
                    checkpoint_data[interval].append(coin_id)
                    with open(checkpoint_file, 'w') as file:
                        json.dump(checkpoint_data, file, indent=4)
                    
                    break  # Break the retry loop on successful download

                except (ReadTimeout, ConnectionError) as e:
                    retry_count += 1
                    wait_time = 2 ** retry_count  # Exponential backoff
                    print(f"Error occurred while downloading {coin_id}: {e}")
                    print(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
                    break  # Break the loop on other exceptions

    print("Data downloading process completed.")

def get_ticker_by_interval_name(client, coin_id, interval, start_date, end_date):
    # KLINE_INTERVAL_1MINUTE 
    # KLINE_INTERVAL_3MINUTE 
    # KLINE_INTERVAL_5MINUTE 
    # KLINE_INTERVAL_15MINUTE 
    # KLINE_INTERVAL_30MINUTE 
    # KLINE_INTERVAL_1HOUR 
    # KLINE_INTERVAL_2HOUR 
    # KLINE_INTERVAL_4HOUR 
    # KLINE_INTERVAL_6HOUR 
    # KLINE_INTERVAL_8HOUR 
    # KLINE_INTERVAL_12HOUR 
    # KLINE_INTERVAL_1DAY 
    # KLINE_INTERVAL_3DAY 
    # KLINE_INTERVAL_1WEEK 
    # KLINE_INTERVAL_1MONTH 
    retry_count = 0
    max_retries = 3
    
    while retry_count < max_retries:
        try:
            # Get data and save to JSON
            ticker_data = client.get_historical_klines(coin_id, interval, start_date, end_date)
            with open(f'../data/binance_data_2/{coin_id}.json', 'w') as file:
                json.dump(ticker_data, file, indent=4)
                print(f'Downloaded {coin_id}')
            return 1  
        
        except (ReadTimeout, ConnectionError) as e:
            retry_count += 1
            print(f"Network Error {coin_id}: {e}")
            print(f"Retry in {2 ** retry_count} seconds...")
            time.sleep(2 ** retry_count) # Exponential backoff
        
        except Exception as e:
            print(f"Error For {coin_id}: {e}")
            break  # Break the loop on other exceptions
    return -1

def agg_data_to_csv(output_file, coin_list=None, num_of_coins=200):
    if coin_list is None:
        with open("./data/checkpoint.json", 'r') as file:
            checkpoint_data = json.load(file)
        coin_ids = checkpoint_data['30MINUTES'][:num_of_coins]
    else:
        coin_ids = coin_list

    # extract data in csv with columns: Date, BTCUSD, ETHUSD, ...
    df_list = []
    for coin_id in tqdm(coin_ids, desc="Processing coins"):
        with open(f'./data/{coin_id}.json', 'r') as file:
            data = json.load(file)
        temp_data = []
        for entry in data:
            open_time = pd.to_datetime(entry[0], unit='ms', utc=True).strftime('%Y-%m-%d %H:%M:%S')
            close_price = entry[4]
            temp_data.append([open_time, close_price])

        temp_df = pd.DataFrame(temp_data, columns=['date', coin_id])
        temp_df['date'] = pd.to_datetime(temp_df['date'])
        df_list.append(temp_df)
        print(f'\nCompleted {coin_id}')

    df = pd.concat(df_list, axis=1)
    df = df.loc[:, ~df.columns.duplicated()]
    df = df.dropna(axis=1, how='all')
    df.to_csv(output_file, index=False)
    print("Data has been written to coin_prices.csv")
    return df


def run_coint_tests_from_csv(df):
    results = []
    n = df.shape[1]
    for i in range(n):
        for j in range(i+1, n):
            coin1 = df.columns[i]
            coin2 = df.columns[j]
            series1 = df.iloc[:, i]
            series2 = df.iloc[:, j]
            
            # Perform OLS regression
            ols_result = sm.OLS(series1, sm.add_constant(series2)).fit()
            
            # Perform cointegration test
            score, p_value, _ = coint(series1, series2)
            
            # Append the results with regression parameters
            results.append({
                'Coin1': coin1, 
                'Coin2': coin2,
                'Score': score, # Engle test score. Smaller means more cointegrated.
                'P-Value': p_value, # p value of regression residual. <=0.05 for significant
                'OLS-Constant': ols_result.params.iloc[0],  # Intercept
                'OLS-Coefficient': ols_result.params.iloc[1],  # Slope
                'R-squared': ols_result.rsquared,  # R-squared
                'Adjusted-R-squared': ols_result.rsquared_adj  # Adjusted R-squared
            })
            print(f'Finished cointegration test for {coin1} and {coin2}')
    return results

 

# extract all price data
# with open(f'./{coin_id}.json', 'r') as file:
#     data = json.load(file)
# extracted_data = []
# for entry in data:
#     open_time = datetime.utcfromtimestamp(entry[0] / 1000).strftime('%Y-%m-%d %H:%M:%S')
#     open_price = entry[1]
#     high_price = entry[2]
#     low_price = entry[3]
#     close_price = entry[4]
#     volume = entry[5]
#     extracted_data.append([open_time, open_price, high_price, low_price, close_price, volume])