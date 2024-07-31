import pandas as pd
import config
from utils.db_utils import *
from utils.calc_utils import *
from dotenv import load_dotenv

'''
get signal with formula：
(hist_sig_days/hist_tlt_days) + 2 * (recent2_sig_days/recent2_tlt_days) + 3 * (recent_sig_days/recent_tlt_days)
'''
load_dotenv(override=True)
DB_USERNAME = os.getenv('RDS_USERNAME') 
DB_PASSWORD = os.getenv('RDS_PASSWORD') 
DB_HOST = os.getenv('RDS_ENDPOINT') 
DB_NAME = 'financial_data'
conn = connect_to_db(DB_NAME, DB_HOST, DB_USERNAME, DB_PASSWORD)

df = get_signal('./data/rolling_coint_result_csv/final_coint_stock_data_top_100.csv', config.STOCK_PRICE_CSV) # config.STOCK_COINT_RESULT_CSV
csv_as_tuple = list(df.itertuples(index=False, name=None))
create_stock_signal_table(conn)
insert_stock_signal_table(conn, csv_as_tuple)



'''TODO - add buy sell signal; add mc/segments for stock for more option'''
