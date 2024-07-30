BN_CHECKPOINT_FILE = './data/checkpoints/binance_checkpoint.json'
BN_JSON_PATH = './data/binance_raw_json'
BN_MAX_RETRIES = 3

SEC_STOCK_TICKERS = './data/sec_stock_tickers.json'
AVAN_CHECKPOINT_FILE = './data/checkpoints/avan_checkpoint.json'
AVAN_JSON_PATH = './data/avan_raw_json'
AVAN_SLEEP_TIME = 0.8

ROLLING_COINT_START_DATE = '2023-01-01'
ROLLING_COINT_END_DATE = '2024-07-01'
ROLLING_COINT_WINDOW = 30
ROLLING_COINT_TOP_N = 3

STOCK_PRICE_CSV = './data/stock_agg_data.csv'
ROLLING_COINT_STOCK_CHECKPOINT_FILE = './data/checkpoints/rolling_coint_stocks_checkpoint.json'
STOCK_COINT_RESULT_CSV = f'./data/rolling_coint_result_csv/top{ROLLING_COINT_TOP_N}_stocks_rolling_coint_result.csv'

COIN_PRICE_CSV = './data/raw_csv/binance_agg_data.csv'
ROLLING_COINT_COIN_CHECKPOINT_FILE = './data/checkpoints/rolling_coint_coins_checkpoint.json'
COIN_COINT_RESULT_CSV = f'./data/rolling_coint_result_csv/top{ROLLING_COINT_TOP_N}_coins_rolling_coint_result.csv'