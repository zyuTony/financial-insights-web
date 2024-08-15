from datetime import datetime
from twilio.rest import Client

#BINANCE JSON RETREIVAL#
BN_CHECKPOINT_FILE = './data/checkpoints/binance_checkpoint.json'
BN_JSON_PATH = './data/binance_raw_json'
BN_DAILY_JSON_PATH = './data/binance_raw_json/1DAY'
BN_MAX_RETRIES = 3

#AVAN JSON RETREIVAL#
SEC_STOCK_TICKERS = './data/sec_stock_tickers.json'
AVAN_CHECKPOINT_FILE = './data/checkpoints/avan_checkpoint.json'
AVAN_OVERVIEW_CHECKPOINT_FILE = './data/checkpoints/avan_overview_checkpoint.json'
AVAN_JSON_PATH = './data/avan_raw_json'
AVAN_DAILY_JSON_PATH = './data/avan_raw_json/avan_data_DAILY'
AVAN_OVERVIEW_JSON_PATH = './data/avan_raw_json/avan_data_OVERVIEW'
AVAN_OPTION_JSON_PATH = './data/avan_raw_json/avan_data_OPTION'
AVAN_SLEEP_TIME = 0.8

#HIST PRICE CSV#
STOCK_PRICE_CSV = './data/raw_csv/stock_agg_data.csv'
COIN_PRICE_CSV = './data/raw_csv/raw_csv/binance_agg_data.csv'

#ROLLING COINT CSV CALCULATION#
# parameters
ROLLING_COINT_START_DATE = '2023-01-01'
ROLLING_COINT_END_DATE = '2024-07-01'
ROLLING_COINT_WINDOW = 120
ROLLING_COINT_TOP_N = 20

# stock save to csv 
ROLLING_COINT_STOCK_CHECKPOINT_FILE = './data/checkpoints/rolling_coint_stocks_checkpoint.json'
STOCK_COINT_RESULT_CSV = f'./data/rolling_coint_result_csv/stocks_rolling_coint_result.csv'

# coin save to csv 
ROLLING_COINT_COIN_CHECKPOINT_FILE = './data/checkpoints/rolling_coint_coins_checkpoint.json'
COIN_COINT_RESULT_CSV =  f'./data/rolling_coint_result_csv/coins_rolling_coint_result.csv'

#SIGNALS#
# criteria
HIST_WINDOW_SIG_EVAL = 720
RECENT_WINDOW_SIG_EVAL = 120 
OLS_WINDOW = 120

STOCK_SIGNAL_CSV = './data/test.csv'
COIN_SIGNAL_CSV = './data/test.csv'


# send text notification
def outgoing_call(account_sid, auth_token, to_number):
    client = Client(account_sid, auth_token)
    call = client.calls.create(
        url="http://demo.twilio.com/docs/voice.xml",
        to=to_number,
        from_='+18449903647')

    print(call.sid)
        
def send_sms_message(account_sid, auth_token, to_number, message):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
            body=message,
            from_='+18449903647',
            to=to_number)

    print(message.sid)
        