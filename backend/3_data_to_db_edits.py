from dotenv import load_dotenv
import os
from utils.db_utils import *
import pandas as pd
import config
from utils.calc_utils import *

load_dotenv(override=True)
DB_USERNAME = os.getenv('RDS_USERNAME') 
DB_PASSWORD = os.getenv('RDS_PASSWORD') 
DB_HOST = os.getenv('RDS_ENDPOINT') 
DB_NAME = 'financial_data' 
coin_json_folder = config.BN_JSON_PATH +'/binance_data_1DAY'
 
conn = connect_to_db(DB_NAME, DB_HOST, DB_USERNAME, DB_PASSWORD)



conn.close()