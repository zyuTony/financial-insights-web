from config import *
from utils.calc_utils import *
from utils.db_utils import *
from dotenv import load_dotenv
import pandas as pd
import psycopg2
from psycopg2 import sql

load_dotenv(override=True)
DB_USERNAME = os.getenv('RDS_USERNAME') 
DB_PASSWORD = os.getenv('RDS_PASSWORD') 
DB_HOST = os.getenv('RDS_ENDPOINT') 
DB_NAME = 'financial_data'
 
'''
STOCK BY SECTOR -- 
SQL -> calc coint -> calc signal
'''
sector = 'LIFE SCIENCES'
industry = 'PHARMACEUTICAL PREPARATIONS'

conn = connect_to_db(DB_NAME, DB_HOST, DB_USERNAME, DB_PASSWORD)
query = f"""
SELECT a.*
FROM stock_historical_price a
JOIN stock_overview b 
ON a.symbol = b.symbol
where date > '2015-01-01' 
and sector = '{sector}'
and industry = '{industry}'
"""
df = pd.read_sql(query, conn)
price_df = df.pivot(index='date', columns='symbol', values='close')
price_df.reset_index(inplace=True)

price_df.to_csv('./data/sql_stock_test.csv')
conn.close()

save_multi_pairs_rolling_coint(price_df, None, './data/checkpoints/life_science_phamaceutical_preparations_coint.json', './data/rolling_coint_result/life_science_pharm_prep_coint.csv')
 