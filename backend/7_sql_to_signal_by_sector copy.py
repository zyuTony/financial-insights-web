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


'''
STOCK BY target symbol -- 
SQL -> calc coint -> calc signal
'''
conn = connect_to_db(DB_NAME, DB_HOST, DB_USERNAME, DB_PASSWORD)
query = f"""
select a.*
from stock_historical_price a 
join stock_overview b 
on a.symbol=b.symbol
where sector = 'TRADE & SERVICES'
 or industry in ('RETAIL-FAMILY CLOTHING STORES', 'RETAIL-DEPARTMENT STORES', 'RUBBER & PLASTICS FOOTWEAR', 
'APPAREL & OTHER FINISHD PRODS OF FABRICS & SIMILAR MATL', 'RETAIL-SHOE STORES', 'RETAIL-RETAIL STORES, NEC', 'RETAIL-EATING & DRINKING PLACES'
,'FOOTWEAR, (NO RUBBER)', 'LEATHER & LEATHER PRODUCTS', 'APPAREL & OTHER FINISHD PRODS OF FABRICS & SIMILAR MATL',
'RETAIL-WOMEN''S CLOTHING STORES', 'WHOLESALE-MISC DURABLE GOODS', 'RETAIL-HOME FURNITURE, FURNISHINGS & EQUIPMENT STORES'
,'RETAIL-BUILDING MATERIALS, HARDWARE, GARDEN SUPPLY', 'RETAIL-DEPARTMENT STORES', 'RETAIL-FURNITURE STORES', 'BEVERAGES')
and date >= '2022-01-01'
"""
df = pd.read_sql(query, conn)
conn.close()

price_df = df.pivot(index='date', columns='symbol', values='close')
price_df.fillna(-1, inplace=True)
price_df.reset_index(inplace=True)

# get coint
save_target_symbol_rolling_coint('GPS', price_df, None, './data/checkpoints/gap_v_clothing_coint.json', './data/rolling_coint_result_csv/gap_v_trades_coint.csv')

# get signal
coint_df = pd.read_csv('./data/rolling_coint_result_csv/gap_v_trades_coint.csv')
signal_df = get_signal(coint_df, price_df)
signal_df.to_csv('./data/gps_v_trades_signal.csv')