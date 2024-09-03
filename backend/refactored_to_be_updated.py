from config import *
from utils.db_utils import *
from utils.gecko_utils import *
from dotenv import load_dotenv
import os
from utils.refactor_data_updater import *

load_dotenv(override=True)
gc_api_key = os.getenv('GECKO_API') 
DB_USERNAME = os.getenv('RDS_USERNAME') 
DB_PASSWORD = os.getenv('RDS_PASSWORD') 
DB_HOST = os.getenv('RDS_ENDPOINT') 
DB_NAME = 'financial_data'

        
# db = coin_gecko_OHLC_db_refresher(DB_NAME, DB_HOST, DB_USERNAME, DB_PASSWORD, "coin_historical_price")
# db.connect()
# db.create_table()
# for filename in os.listdir(GECKO_DAILY_JSON_PATH):
#     if filename.endswith('.json'):
#         file_path = os.path.join(GECKO_DAILY_JSON_PATH, filename)
#         db.insert_data(file_path)
# db.close()

db = coin_gecko_OHLC_hourly_db_refresher(DB_NAME, DB_HOST, DB_USERNAME, DB_PASSWORD, "coin_hourly_historical_price")
db.connect()
db.create_table()
for filename in os.listdir(GECKO_HOURLY_JSON_PATH):
    if filename.endswith('.json'):
        file_path = os.path.join(GECKO_HOURLY_JSON_PATH, filename)
        db.insert_data(file_path)
db.close()

# db = avan_stock_OHLC_db_refresher(DB_NAME, DB_HOST, DB_USERNAME, DB_PASSWORD, "stock_historical_price")
# db.connect()
# db.create_table()
# for filename in os.listdir(AVAN_DAILY_JSON_PATH):
#     if filename.endswith('.json'):
#         file_path = os.path.join(AVAN_DAILY_JSON_PATH, filename)
#         db.insert_data(file_path)
# db.close()

# db = coin_gecko_overview_db_refresher(DB_NAME, DB_HOST, DB_USERNAME, DB_PASSWORD, "coin_overview")
# db.connect()
# db.create_table()
# db.insert_data(GECKO_JSON_PATH+'/mapping/top_symbol_by_mc.json')
# db.close()

# db = avan_stock_overview_db_refresher(DB_NAME, DB_HOST, DB_USERNAME, DB_PASSWORD, "stock_overview")
# db.connect()
# db.create_table()
# for filename in os.listdir(AVAN_OVERVIEW_JSON_PATH):
#     if filename.endswith('.json'):
#         file_path = os.path.join(AVAN_OVERVIEW_JSON_PATH, filename)
#         db.insert_data(file_path)
# db.close()