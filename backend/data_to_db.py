from dotenv import load_dotenv
import os
from utils.db_utils import *
import pandas as pd
import config

load_dotenv()
DB_USERNAME = os.getenv('RDS_USERNAME') 
DB_PASSWORD = os.getenv('RDS_PASSWORD') 
DB_HOST = os.getenv('RDS_ENDPOINT') 
DB_NAME = 'financial_data' 

stock_json_folder = config.AVAN_JSON_PATH +'/avan_data_DAILY'
coin_json_folder = config.BN_JSON_PATH +'/binance_data_1DAY'
    
conn = connect_to_db(DB_NAME, DB_HOST, DB_USERNAME, DB_PASSWORD)

# '''
# JSON -> SQL
# '''
# '''update stock data'''
# create_stock_historical_price_table(conn)
# for filename in os.listdir(stock_json_folder):
#     if filename.endswith('.json'):
#         file_path = os.path.join(stock_json_folder, filename)
#         try:
#             insert_stock_historical_price_table(conn, file_path)
#         except Exception as e:
#             print(f'Error processing {filename}: {e}')
#             continue
#     print(f'finished {filename}')

# conn.close()
# print(f"Data successfully inserted into the database.")


# '''update coin data'''
# create_coin_historical_price_table(conn)
# for filename in os.listdir(coin_json_folder):
#     if filename.endswith('.json'):
#         file_path = os.path.join(coin_json_folder, filename)
#         try:
#             insert_coin_historical_price_table(conn, file_path)
#         except Exception as e:
#             print(f'Error processing {filename}: {e}')
#             continue
#     print(f'finished {filename}')

# conn.close()
# print(f"Data successfully inserted into the database.")

'''
stock rolling coint of 120 insert to sql
'''

df = pd.read_csv('./data/rolling_coint_result_csv/final_coint_stock_data_top_100.csv')
# df = pd.read_csv(config.STOCK_COINT_RESULT_CSV)
# change df fit for uploading
df.columns = df.columns.str.replace('_p_val$', '', regex=True)
df_melted = pd.melt(df, id_vars=['date'], var_name='pair_name', value_name='value')
df_melted[['stock1', 'stock2']] = df_melted['pair_name'].str.split('_', expand=True)
df_melted = df_melted.drop(columns=['pair_name'])
df_melted['window_length'] = 120
df_melted = df_melted[['date', 'window_length', 'stock1', 'stock2', 'value']]

create_stock_pair_coint_table(conn)

csv_as_tuple = list(df_melted.itertuples(index=False, name=None))
insert_stock_pair_coint_table(conn, csv_as_tuple)

conn.close()
