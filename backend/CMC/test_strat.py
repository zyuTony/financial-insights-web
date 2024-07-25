
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import requests
import os
from dotenv import load_dotenv
import json
import pandas as pd
from sqlalchemy import create_engine
from cmc_utlis import * 
import time

load_dotenv()
api_key = os.getenv('CMC_API') 
username = os.getenv('RDS_USERNAME') 
password = os.getenv('RDS_PASSWORD') 
endpoint = os.getenv('RDS_ENDPOINT') 

# # ------ EXTRACT JSON
# # --- pull raw historical price data from api and save as json
# data = pull_coin_list(100, api_key, 'top_crypto_tickers.json')
# ids, symbols= coin_list_json_to_str('top_crypto_tickers.json')
# ids, symbols= coin_list_json_to_array('top_crypto_tickers.json')
# # Pull historical data for BTC
# coin_id = '1'
# interval = 'daily'  # Assuming daily data, adjust as necessary 

# btc_data = pull_historical_price(coin_id, api_key, f'./hist_data/hist_price_{coin_id}_{interval}.json', interval, start_date='2023-08-01', end_date='2024-07-01')

# btc_df = pd.DataFrame([{
#     'date': quote['timestamp'],
#     'BTCUSD': quote['quote']['USD']['price']
# } for quote in btc_data['data'][coin_id]['quotes']])

# # Pull historical data for ETH
# coin_id = '1027'
# eth_data = pull_historical_price(coin_id, api_key, f'./hist_data/hist_price_{coin_id}_{interval}.json', interval, start_date='2023-08-01', end_date='2024-07-01')

# eth_df = pd.DataFrame([{
#     'date': quote['timestamp'],
#     'ETHUSD': quote['quote']['USD']['price']
# } for quote in eth_data['data'][coin_id]['quotes']])

# # Convert date strings to datetime objects for proper merging
# btc_df['date'] = pd.to_datetime(btc_df['date'])
# eth_df['date'] = pd.to_datetime(eth_df['date'])

# # Merge the two DataFrames on the date column
# merged_df = pd.merge(btc_df, eth_df, on='date', how='inner')

# # Optional: Set the date as the index
# merged_df.set_index('date', inplace=True)

# # Display the merged DataFrame
# print(merged_df)

# # Save to a CSV file
# merged_df.to_csv('ethbtc_price_data.csv')
 
 

import pandas as pd
import numpy as np
import ta

df = pd.read_csv('ethbtc_price_data.csv')
df['spread'] = 20.5 * df['ETHUSD'] - 5155.77 - df['BTCUSD']
df['ETHBTC'] = df['ETHUSD'] / df['BTCUSD']
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)
# Calculate Bollinger Bands
length = 20
mult = 2.0
df['basis'] = df['spread'].rolling(window=length).mean()
df['dev'] = mult * df['spread'].rolling(window=length).std()
df['upper'] = df['basis'] + df['dev']
df['lower'] = df['basis'] - df['dev']

# Calculate RSI of the spread
rsi_length = 14
df['rsi'] = ta.momentum.RSIIndicator(df['ETHBTC'], window=rsi_length).rsi()
 
stop_loss_percentage = 10.0
initial_position = 5
trade_size = 0.8
positions = []
max_positions = 1
trades = []
current_position = initial_position
trade_id = 0

# Trading strategy
# Columns to store trade information
df['TradeID'] = np.nan
df['Action'] = np.nan
df['Size'] = np.nan
df['TradeReturn'] = np.nan
df['CurrentPosition'] = np.nan

# Trading strategy
for i in range(len(df)):
    current_price = df['ETHBTC'].iloc[i]
    if np.isnan(current_price) or np.isnan(df['rsi'].iloc[i]) or np.isnan(df['upper'].iloc[i]) or np.isnan(df['lower'].iloc[i]):
        continue
    
    # Long condition
    if df['spread'].iloc[i] <= df['lower'].iloc[i] and df['rsi'].iloc[i] <= 30 and len(positions) < max_positions:
        trade_id += 1
        positions.append({'Type': 'long', 'EntryPrice': current_price, 'EntryDate': df.index[i], 'TradeID': trade_id, 'Size': trade_size})
        df.at[df.index[i], 'TradeID'] = trade_id
        df.at[df.index[i], 'Action'] = 'Open Long'
        df.at[df.index[i], 'Size'] = trade_size
        df.at[df.index[i], 'CurrentPosition'] = current_position
    
    # Short condition
    if df['spread'].iloc[i] >= df['upper'].iloc[i] and df['rsi'].iloc[i] >= 70 and len(positions) < max_positions:
        trade_id += 1
        positions.append({'Type': 'short', 'EntryPrice': current_price, 'EntryDate': df.index[i], 'TradeID': trade_id, 'Size': trade_size})
        df.at[df.index[i], 'TradeID'] = trade_id
        df.at[df.index[i], 'Action'] = 'Open Short'
        df.at[df.index[i], 'Size'] = trade_size
        df.at[df.index[i], 'CurrentPosition'] = current_position
    
    # Check for closing positions
    for position in positions[:]:
        if position['Type'] == 'long':
            long_stop_loss = position['EntryPrice'] * (1 - stop_loss_percentage / 100)
            if current_price <= long_stop_loss or (df['spread'].iloc[i] < 150 and df['spread'].iloc[i] > -150):
                trade_return = (current_price - position['EntryPrice']) * position['Size']
                current_position += trade_return
                df.at[df.index[i], 'TradeID'] = position['TradeID']
                df.at[df.index[i], 'Action'] = 'Close Long'
                df.at[df.index[i], 'Size'] = position['Size']
                df.at[df.index[i], 'TradeReturn'] = trade_return
                df.at[df.index[i], 'CurrentPosition'] = current_position
                positions.remove(position)
        
        if position['Type'] == 'short':
            short_stop_loss = position['EntryPrice'] * (1 + stop_loss_percentage / 100)
            if current_price >= short_stop_loss or (df['spread'].iloc[i] < 150 and df['spread'].iloc[i] > -150):
                trade_return = (position['EntryPrice'] - current_price) * position['Size']
                current_position += trade_return
                df.at[df.index[i], 'TradeID'] = position['TradeID']
                df.at[df.index[i], 'Action'] = 'Close Short'
                df.at[df.index[i], 'Size'] = position['Size']
                df.at[df.index[i], 'TradeReturn'] = trade_return
                df.at[df.index[i], 'CurrentPosition'] = current_position
                positions.remove(position)

df.to_csv('eth_btc_trades.csv', index=False)
    # # Check for closing positions
    # for position in positions[:]:
    #     if position['Type'] == 'long':
    #         long_stop_loss = position['EntryPrice'] * (1 - stop_loss_percentage / 100)
    #         if current_price <= long_stop_loss or (df['spread'].iloc[i] < 150 and df['spread'].iloc[i] > -150):
    #             trade_return = (current_price - position['EntryPrice']) * position['Size']
    #             current_position += trade_return
    #             trades.append({'TradeID': position['TradeID'], 'Date': df.index[i], 'Action': 'Close Long', 'Price': current_price, 'Size': position['Size'], 'RSI': df['rsi'].iloc[i], 'UpperBand': df['upper'].iloc[i], 'LowerBand': df['lower'].iloc[i], 'Spread': df['spread'].iloc[i], 'CurrentPosition': current_position, 'TradeReturn': trade_return})
    #             positions.remove(position)
        
    #     if position['Type'] == 'short':
    #         short_stop_loss = position['EntryPrice'] * (1 + stop_loss_percentage / 100)
    #         if current_price >= short_stop_loss or (df['spread'].iloc[i] < 150 and df['spread'].iloc[i] > -150):
    #             trade_return = (position['EntryPrice'] - current_price) * position['Size']
    #             current_position += trade_return
    #             trades.append({'TradeID': position['TradeID'], 'Date': df.index[i], 'Action': 'Close Short', 'Price': current_price, 'Size': position['Size'], 'RSI': df['rsi'].iloc[i], 'UpperBand': df['upper'].iloc[i], 'LowerBand': df['lower'].iloc[i], 'Spread': df['spread'].iloc[i], 'CurrentPosition': current_position, 'TradeReturn': trade_return})
    #             positions.remove(position)

# # Convert trades to DataFrame
# trades_df = pd.DataFrame(trades)
# trades_df.to_csv('eth_btc_trades.csv', index=False)






# def calculate_indicators(df, rsi_period=14, band_period=20, band_std_dev=2):
#     df['RSI'] = ta.momentum.RSIIndicator(df['ETHBTC'], window=rsi_period).rsi()
#     bb = ta.volatility.BollingerBands(df['ETHBTC'], window=band_period, window_dev=band_std_dev)
#     df['UpperBand'] = bb.bollinger_hband()
#     df['MiddleBand'] = bb.bollinger_mavg()
#     df['LowerBand'] = bb.bollinger_lband() 
#     return df

# # Custom formula condition
# def custom_formula_condition(df, i):
#     # Implement your custom formula condition here
#     # Return True if the condition is met, otherwise False
#     return abs(df['Spread'].iloc[i]) < 150

# # Trading strategy
# def trading_strategy(df, rsi_period=14, band_period=20, band_std_dev=2, stop_loss=0.05, initial_position=5, trade_size=0.8):
#     df = calculate_indicators(df, rsi_period, band_period, band_std_dev)
    
#     positions = []
#     trades = []
#     current_position = initial_position
#     trade_id = 0
    
#     for i in range(len(df)):
#         current_price = df['ETHBTC'].iloc[i]
        
#         # Check for new positions
#         if df['RSI'].iloc[i] <= 30 and df['ETHBTC'].iloc[i] <= df['LowerBand'].iloc[i]:
#             trade_id += 1
#             positions.append({'Type': 'long', 'EntryPrice': current_price, 'EntryDate': df['date'].iloc[i], 'TradeID': trade_id, 'Size': trade_size})
#             trades.append({'TradeID': trade_id, 'Date': df['date'].iloc[i], 'Action': 'Open Long', 'Price': current_price, 'Size': trade_size, 'RSI': df['RSI'].iloc[i], 'UpperBand': df['UpperBand'].iloc[i], 'LowerBand': df['LowerBand'].iloc[i], 'Spread': df['Spread'].iloc[i], 'CurrentPosition': current_position, 'TradeReturn': 0})
#         elif df['RSI'].iloc[i] >= 70 and df['ETHBTC'].iloc[i] >= df['UpperBand'].iloc[i]:
#             trade_id += 1
#             positions.append({'Type': 'short', 'EntryPrice': current_price, 'EntryDate': df['date'].iloc[i], 'TradeID': trade_id, 'Size': trade_size})
#             trades.append({'TradeID': trade_id, 'Date': df['date'].iloc[i], 'Action': 'Open Short', 'Price': current_price, 'Size': trade_size, 'RSI': df['RSI'].iloc[i], 'UpperBand': df['UpperBand'].iloc[i], 'LowerBand': df['LowerBand'].iloc[i], 'Spread': df['Spread'].iloc[i], 'CurrentPosition': current_position, 'TradeReturn': 0})
        
#         # Check for closing positions
#         for position in positions[:]:
#             if position['Type'] == 'long' and ((current_price <= position['EntryPrice'] * (1 - stop_loss)) or custom_formula_condition(df, i)):
#                 trade_return = (current_price - position['EntryPrice']) * position['Size']
#                 current_position += trade_return
#                 trades.append({'TradeID': position['TradeID'], 'Date': df['date'].iloc[i], 'Action': 'Close Long', 'Price': current_price, 'Size': position['Size'], 'RSI': df['RSI'].iloc[i], 'UpperBand': df['UpperBand'].iloc[i], 'LowerBand': df['LowerBand'].iloc[i], 'Spread': df['Spread'].iloc[i], 'CurrentPosition': current_position, 'TradeReturn': trade_return})
#                 positions.remove(position)
#             elif position['Type'] == 'short' and ((current_price >= position['EntryPrice'] * (1 + stop_loss)) or custom_formula_condition(df, i)):
#                 trade_return = (position['EntryPrice'] - current_price) * position['Size']
#                 current_position += trade_return
#                 trades.append({'TradeID': position['TradeID'], 'Date': df['date'].iloc[i], 'Action': 'Close Short', 'Price': current_price, 'Size': position['Size'], 'RSI': df['RSI'].iloc[i], 'UpperBand': df['UpperBand'].iloc[i], 'LowerBand': df['LowerBand'].iloc[i], 'Spread': df['Spread'].iloc[i], 'CurrentPosition': current_position, 'TradeReturn': trade_return})
#                 positions.remove(position)
    
#     return pd.DataFrame(trades)

# rsi_period = 14
# band_period = 20
# band_std_dev = 2
# stop_loss = 0.1
# initial_position = 50
# trade_size = 10

# # Run the strategy and get trades
# trades_df = trading_strategy(df, rsi_period, band_period, band_std_dev, stop_loss, initial_position, trade_size)
# trades_df.to_csv('eth_btc_trades.csv', index=False)