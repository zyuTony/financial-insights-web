from dotenv import load_dotenv
import os
from utils.db_utils import *
from utils.calc_utils import *
from utils.avan_utils import *
import pandas as pd
from config import *


load_dotenv(override=True)
DB_USERNAME = os.getenv('RDS_USERNAME') 
DB_PASSWORD = os.getenv('RDS_PASSWORD') 
DB_HOST = os.getenv('RDS_ENDPOINT') 
DB_NAME = 'financial_data' 

gc_api_key = os.getenv('GECKO_API') 
cmc_api_key = os.getenv('CMC_API')  
avan_api_key = os.getenv('ALPHA_VANTAGE_PREM_API') 
 
'''
DATA SOLUTION:
1) provide list of tickers from same segment manually
2) download jsons from avan
3) aggregate to csv file
4) get all pairs of rolling coint data
'''
# # provide list of tickers from same segment manually
symbols = ["TXGE", "XOM", "CVX", "COP", "EOG", "EPD", "SLB", "MPC", "PSX", "ET", "OXY", "WMB", "OKE", "VLO", "KMI", "TBN", "LNG", "MPLX", "HES", "FANG", "BKR", "TRGP", "DVN", "HAL", "CQP", "TPL", "EQT", "CTRA", "MRO", "WES", "PAA", "PR", "OVV", "FTI", "APA", "CHK", "CHRD", "DINO", "HESM", "AR", "VNOM", "WFRD", "IEP", "RRC", "SUN", "DTM", "NOV", "MTDR", "SWN", "AM"]
price_agg_csv = './data/energy_price.csv'
price_coint_checkpoint_file = './data/energy_price_checkpoint.json'
rolling_coint_csv = './data/energy_price_coint.csv'
signal_csv = './data/energy_price_signal.csv'

# # get those data from avan 
# for symbol in symbols:
#     avan_pull_stock_data('DAILY', symbol, avan_api_key)

# # aggregate to csv file
# combined_df = pd.DataFrame()
# for filename in os.listdir(AVAN_DAILY_JSON_PATH):
#     if filename.endswith('.json'):
#         file_path = os.path.join(AVAN_DAILY_JSON_PATH, filename)
        
#         with open(file_path, 'r') as file:
#             data = json.load(file)
#             symbol = data["Meta Data"]["2. Symbol"]
        
#         if symbol in symbols:
#             print(f'begin {symbol}')
#             df = avan_single_json_append_to_csv(file_path)
            
#             if combined_df.empty:
#                 combined_df = df
#             else:
#                 combined_df = pd.merge(combined_df, df, on='Date', how='outer')
# combined_df.sort_values(by='date', inplace=True)
# combined_df.to_csv(price_agg_csv, index=False)

# # get rolling coint data
# price_data = pd.read_csv(price_agg_csv)
# get_multi_pairs_rolling_coint(price_agg_csv, None, price_coint_checkpoint_file, rolling_coint_csv)

'''
TRADING SOLUTION:
1) select series with last data point <= 0.05 -> mark as cointegrated
    -- output last_sig_days = X; 
2) calculate key score: (% sig in recent 90 days) + (% sig in all history)
3) calculate ols coeff
4) filter out super low r squared series
5) use ols to calculate the I(0) data series.
6) calculate rolling mean and 1, 2 std dev range.   
7) trade the pair by long/short at std dev range and sell at mean at 0.
8) output I(0)s data series ranged from 120D+last_sig_days AND its std dev range
date | pair1       | pair2  
     | range low   | range low 
     | range high  | range high    
     | I(0)...     | I(0)...    
'''

# df = get_signal(rolling_coint_csv, price_agg_csv)
# df.to_csv(signal_csv,index=False)
# Read the price data
rolling_coint_df = pd.read_csv(rolling_coint_csv, parse_dates=['date']) 
hist_price_df = pd.read_csv(price_agg_csv)
hist_price_df = hist_price_df[-120:]
ols_df = get_multi_pairs_ols_coeff(hist_price_df, rolling_coint_df.columns[1:])
 
results = []
for index, row in ols_df.iterrows():
    name1 = row['name1']
    name2 = row['name2']
    ols_constant = row['OLS-constant']
    ols_coeff = row['OLS-coeff']

    result = hist_price_df[name1] - ols_constant - (ols_coeff * hist_price_df[name2])
    results.append(result)

# Convert the list of results into a DataFrame
results_df = pd.DataFrame(results).T

# Rename columns to match the 'name1' from the 'ols' DataFrame
results_df.columns = [f"{row['name1']}_{row['name2']}" for index, row in ols_df.iterrows()]
results_df = pd.concat([hist_price_df['date'].reset_index(drop=True), results_df.reset_index(drop=True)], axis=1)
# Display the resulting DataFrame
results_df.to_csv('./data/test.csv', index=False)

df = get_signal(rolling_coint_csv, price_agg_csv)
df.to_csv('./data/test_signal.csv', index=False)

top_15 = df.sort_values(by='most_recent_coint_pct', ascending=False).head(15)
selected_columns = [f"{row['name1']}_{row['name2']}" for _, row in top_15.iterrows()]
results_df_filtered = results_df[['date'] + selected_columns]

results_df_filtered.to_csv('./data/test_filtered.csv', index=False)
