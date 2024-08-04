'''BINANCE JSON RETREIVAL'''
BN_CHECKPOINT_FILE = './data/checkpoints/binance_checkpoint.json'
BN_JSON_PATH = './data/binance_raw_json'
BN_MAX_RETRIES = 3

'''AVAN JSON RETREIVAL'''
SEC_STOCK_TICKERS = './data/sec_stock_tickers.json'
AVAN_CHECKPOINT_FILE = './data/checkpoints/avan_checkpoint.json'
AVAN_OVERVIEW_CHECKPOINT_FILE = './data/checkpoints/avan_overview_checkpoint.json'
AVAN_JSON_PATH = './data/avan_raw_json'
AVAN_SLEEP_TIME = 0.8

'''HIST PRICE CSV'''
STOCK_PRICE_CSV = './data/raw_csv/stock_agg_data.csv'
COIN_PRICE_CSV = './data/raw_csv/raw_csv/binance_agg_data.csv'

'''ROLLING COINT CSV CALCULATION'''
# parameters
ROLLING_COINT_START_DATE = '2023-01-01'
ROLLING_COINT_END_DATE = '2024-07-01'
ROLLING_COINT_WINDOW = 30
ROLLING_COINT_TOP_N = 3

# stock save to csv 
ROLLING_COINT_STOCK_CHECKPOINT_FILE = './data/checkpoints/rolling_coint_stocks_checkpoint.json'
STOCK_COINT_RESULT_CSV = f'./data/rolling_coint_result_csv/top{ROLLING_COINT_TOP_N}_stocks_rolling_coint_result.csv'

# coin save to csv 
ROLLING_COINT_COIN_CHECKPOINT_FILE = './data/checkpoints/rolling_coint_coins_checkpoint.json'
COIN_COINT_RESULT_CSV = f'./data/rolling_coint_result_csv/top{ROLLING_COINT_TOP_N}_coins_rolling_coint_result.csv'

'''SIGNALS'''
# criteria
HIST_WINDOW_SIG_EVAL = 1000
RECENT_WINDOW_SIG_EVAL = 120
RECENT_WINDOW2_SIG_EVAL = 360
OLS_WINDOW = 120