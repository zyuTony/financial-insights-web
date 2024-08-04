import config
from utils.calc_utils import *
from dotenv import load_dotenv

load_dotenv(override=True)
DB_USERNAME = os.getenv('RDS_USERNAME') 
DB_PASSWORD = os.getenv('RDS_PASSWORD') 
DB_HOST = os.getenv('RDS_ENDPOINT') 
DB_NAME = 'financial_data'

'''
JSON-> CALCULATE rolling coint  **MOST TIME CONSUMING
'''
#coin
get_multi_pairs_rolling_coint(config.COIN_PRICE_CSV, config.ROLLING_COINT_TOP_N, config.ROLLING_COINT_COIN_CHECKPOINT_FILE, config.COIN_COINT_RESULT_CSV)

#stock
get_multi_pairs_rolling_coint(config.STOCK_PRICE_CSV, config.ROLLING_COINT_TOP_N, config.ROLLING_COINT_STOCK_CHECKPOINT_FILE, config.STOCK_COINT_RESULT_CSV)

'''
CALCULATE signal with formula：
(hist_sig_days/hist_tlt_days) + 2 * (recent2_sig_days/recent2_tlt_days) + 3 * (recent_sig_days/recent_tlt_days)
'''
# coin
df = get_signal('./data/rolling_coint_result_csv/final_coint_binance_data.csv', config.COIN_PRICE_CSV) # config.COIN_COINT_RESULT_CSV
df.to_csv(config.COIN_SIGNAL_CSV,index=False)

#stock
df = get_signal('./data/rolling_coint_result_csv/final_coint_stock_data_top_100.csv', config.STOCK_PRICE_CSV) # config.STOCK_COINT_RESULT_CSV
df.to_csv(config.STOCK_SIGNAL_CSV,index=False)