from dotenv import load_dotenv
import os
from utils.db_utils import *
import pandas as pd
import config

load_dotenv(override=True)
DB_USERNAME = os.getenv('RDS_USERNAME') 
DB_PASSWORD = os.getenv('RDS_PASSWORD') 
DB_HOST = os.getenv('RDS_ENDPOINT') 
DB_NAME = 'financial_data' 

stock_json_folder = config.AVAN_JSON_PATH +'/avan_data_DAILY'
stock_overview_json_folder = config.AVAN_JSON_PATH +'/avan_stock_OVERVIEW'
coin_json_folder = config.BN_JSON_PATH +'/binance_data_1DAY'
 
conn = connect_to_db(DB_NAME, DB_HOST, DB_USERNAME, DB_PASSWORD)

'''
--- RAW JSON -> SQL
'''
# update stock data
create_stock_historical_price_table(conn)
for filename in os.listdir(stock_json_folder):
    if filename.endswith('.json'):
        file_path = os.path.join(stock_json_folder, filename)
        try:
            insert_stock_historical_price_table(conn, file_path)
        except Exception as e:
            print(f'Error processing {filename}: {e}')
            continue
    print(f'Inserted {filename} historical price')

# update stock overview data
create_stock_overview_table(conn)
for filename in os.listdir(stock_overview_json_folder):
    if filename.endswith('.json'):
        file_path = os.path.join(stock_overview_json_folder, filename)
        try:
            insert_stock_overview_table(conn, file_path)
            print(f'Inserted {filename} overview')
        except Exception as e:
            print(f'Error processing {filename}: {e}')
            continue 

# update coin data
create_coin_historical_price_table(conn)
for filename in os.listdir(coin_json_folder):
    if filename.endswith('.json'):
        file_path = os.path.join(coin_json_folder, filename)
        try:
            insert_coin_historical_price_table(conn, file_path)
        except Exception as e:
            print(f'Error processing {filename}: {e}')
            continue
    print(f'Inserted {filename} historical price')

'''
--- ROLLING COINT CSV -> DB
'''
# stock rolling coint of 120 
df = pd.read_csv('./data/rolling_coint_result_csv/final_coint_stock_data_top_100.csv')#config.STOCK_COINT_RESULT_CSV
df.columns = df.columns.str.replace('_p_val$', '', regex=True)
df_melted = pd.melt(df, id_vars=['date'], var_name='pair_name', value_name='value')
df_melted[['stock1', 'stock2']] = df_melted['pair_name'].str.split('_', expand=True)
df_melted = df_melted.drop(columns=['pair_name'])
df_melted['window_length'] = 120
df_melted = df_melted[['date', 'window_length', 'stock1', 'stock2', 'value']]

create_stock_pair_coint_table(conn)
insert_stock_pair_coint_table(conn, list(df_melted.itertuples(index=False, name=None)))


# coin rolling coint of 120  
df = pd.read_csv('./data/rolling_coint_result_csv/final_coint_binance_data.csv')#config.COIN_COINT_RESULT_CSV
df.columns = df.columns.str.replace('_p_val$', '', regex=True)
df_melted = pd.melt(df, id_vars=['date'], var_name='pair_name', value_name='value')
df_melted[['coin1', 'coin2']] = df_melted['pair_name'].str.split('_', expand=True)
df_melted = df_melted.drop(columns=['pair_name'])
df_melted['window_length'] = 120
df_melted = df_melted[['date', 'window_length', 'coin1', 'coin2', 'value']]

create_coin_pair_coint_table(conn)
insert_coin_pair_coint_table(conn, list(df_melted.itertuples(index=False, name=None)))


'''
--- SIGNALS to DB
'''
# coins
create_coin_signal_table(conn)
insert_coin_signal_table(conn, list(pd.read_csv(config.COIN_SIGNAL_CSV).itertuples(index=False, name=None)))

# stocks
create_stock_signal_table(conn)
insert_stock_signal_table(conn, list(pd.read_csv(config.STOCK_SIGNAL_CSV).itertuples(index=False, name=None)))


conn.close()