from datetime import datetime
from twilio.rest import Client

DATA_FOLDER = '/home/ec2-user/financial_database/backend/data'

# FOLDERS
RAW_CSV_PATH = DATA_FOLDER + '/raw_csv'
CHECKPOINT_JSON_PATH = DATA_FOLDER + '/checkpoints'
COINT_CSV_PATH = DATA_FOLDER + '/rolling_coint_result_csv'
SIGNAL_CSV_PATH = DATA_FOLDER + '/signal_csv'

# BINANCE JSON 
BN_MAX_RETRIES = 3
BN_CHECKPOINT_FILE = CHECKPOINT_JSON_PATH + '/binance_checkpoint.json'
BN_JSON_PATH = DATA_FOLDER + '/binance_raw_json'
BN_DAILY_JSON_PATH = BN_JSON_PATH + '/1DAY'

# COIN GECKO JSON
DAYS_PER_API_LIMIT = 180
GECKO_JSON_PATH = DATA_FOLDER + '/gecko_raw_json'
GECKO_DAILY_JSON_PATH = DATA_FOLDER + '/gecko_raw_json/daily'

# AVAN JSON  
AVAN_SLEEP_TIME = 0.8
SEC_STOCK_TICKERS = DATA_FOLDER + '/sec_stock_tickers.json'

AVAN_CHECKPOINT_FILE = CHECKPOINT_JSON_PATH + '/avan_checkpoint.json'
AVAN_OVERVIEW_CHECKPOINT_FILE = CHECKPOINT_JSON_PATH + '/avan_overview_checkpoint.json'
AVAN_JSON_PATH = DATA_FOLDER + '/avan_raw_json'

AVAN_DAILY_JSON_PATH = AVAN_JSON_PATH + '/avan_data_DAILY'
AVAN_OVERVIEW_JSON_PATH = AVAN_JSON_PATH + '/avan_data_OVERVIEW'
AVAN_OPTION_JSON_PATH = AVAN_JSON_PATH + '/avan_data_OPTION'




# HIST PRICE CSV
STOCK_PRICE_CSV = RAW_CSV_PATH + '/stock_agg_data.csv'
COIN_PRICE_CSV = RAW_CSV_PATH + '/binance_agg_data.csv'

STOCK_SIGNAL_CSV = DATA_FOLDER + '/test.csv'
COIN_SIGNAL_CSV = DATA_FOLDER + '/test.csv'

# stock save to csv 
ROLLING_COINT_STOCK_CHECKPOINT_FILE = CHECKPOINT_JSON_PATH + '/rolling_coint_stocks_checkpoint.json'
STOCK_COINT_RESULT_CSV = COINT_CSV_PATH + '/stocks_rolling_coint_result.csv'

# coin save to csv 
ROLLING_COINT_COIN_CHECKPOINT_FILE = CHECKPOINT_JSON_PATH + '/rolling_coint_coins_checkpoint.json'
COIN_COINT_RESULT_CSV = COINT_CSV_PATH + '/coins_rolling_coint_result.csv'


'''PARAMETERS'''
#ROLLING COINT CSV CALCULATION#
# parameters
ROLLING_COINT_START_DATE = '2023-01-01'
ROLLING_COINT_END_DATE = '2024-08-01'
ROLLING_COINT_WINDOW = 120

#SIGNALS#
# criteria
HIST_WINDOW_SIG_EVAL = 720
RECENT_WINDOW_SIG_EVAL = 120 
OLS_WINDOW = 120


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
        