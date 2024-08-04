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

stock_overview_json_folder = config.AVAN_JSON_PATH +'/avan_stock_OVERVIEW'
 
conn = connect_to_db(DB_NAME, DB_HOST, DB_USERNAME, DB_PASSWORD)

'''
--- RAW JSON -> SQL
'''
'''update stock overview data'''
create_stock_overview_table(conn)
for filename in os.listdir(stock_overview_json_folder):
    if filename.endswith('.json'):
        file_path = os.path.join(stock_overview_json_folder, filename)
        try:
            insert_stock_overview_table(conn, file_path)
            print(f'finished {filename}')
        except Exception as e:
            print(f'Error processing {filename}: {e}')
            continue
    
 

print(f"Data successfully inserted into the database.")
conn.close()