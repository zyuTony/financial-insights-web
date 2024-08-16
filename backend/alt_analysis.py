from dotenv import load_dotenv
import os
from utils.db_utils import *
import config
from binance.client import Client
from utils.bn_utils import *
from utils.avan_utils import *
from utils.calc_utils import *

load_dotenv(override=True)
DB_USERNAME = os.getenv('RDS_USERNAME') 
DB_PASSWORD = os.getenv('RDS_PASSWORD') 
DB_HOST = os.getenv('RDS_ENDPOINT') 
DB_NAME = 'financial_data' 

bn_api_key = os.getenv('BINANCE_API')  
bn_api_secret = os.getenv('BINANCE_SECRET')  
cmc_api_key = os.getenv('CMC_API')  
avan_api_key = os.getenv('ALPHA_VANTAGE_PREM_API') 


tickers = ["BTC", "XRP", "ETH", "XLM", "BCH", "EOS", "LTC", "USDT", "BSV", "ADA", "XMR", "TRX", "MIOTA", "DASH", "XEM", "BNB", "NEO", "ETC", "ZEC", "BTG", "XTZ", "VET", "DOGE", "MKR", "ONT", "ZRX", "OMG",
"TUSD", "BAT", "QTUM", "USDC", "DCR", "PAX", "LSK", "BCD", "BCN", "DGB", "ZIL", "NANO", "AE", "BTS", "WAVES", "ICX", "AOA", "SC", "XVG", "LINK", "FCT", "STEEM", "NPXS", "REP", "PPT", "GNT",
"QASH", "STRAT", "MAID", "KMD", "ETN", "CHX", "SNT", "HOT", "MANA", "R", "DAI", "WAX", "ARDR", "NEXO", "IQ", "THETA", "ETP", "HT", "KCS", "BTCP", "MOAC", "INB", "ODE", "WTC", "GUSD", "MGO",
"MONA", "RVN", "GXS", "WAN", "ARK", "PIVX", "ELA", "RDD", "AION", "SRN", "HC", "BNT", "MITH", "LKY", "POLY", "ELF", "MCO", "CENNZ", "QKC", "XIN"]

dec2019_top200 = ["BTC", "ETH", "XRP", "USDT", "BCH", "LTC", "EOS", "BNB", "BSV", "XLM", "TRX", "ADA", "XMR", "LEO", "XTZ", "LINK",
"ATOM", "HT", "NEO", "MIOTA", "MKR", "DASH", "ETC", "USDC", "MIN", "VET", "XEM", "CRO", "INO", "DOGE", "BAT", "ZEC",
"PAX", "HEDG", "DCR", "INB", "SNX", "QTUM", "MXM", "TUSD", "ZRX", "CENNZ", "PZM", "HOT", "THX", "THR", "ALGO", "REP",
"NANO", "KBC", "BTQ", "RVN", "OMG", "CNX", "ABBC", "XIN", "VSYS", "SEELE", "EON", "ZB", "EKT", "DGB", "BTM", "LSK",
"KMD", "SAI", "LUNA", "KCS", "FTT", "QNT", "SXP", "BDX", "GAP", "BCD", "THETA", "ICX", "FST", "MATIC", "SC", "EVR",
"BTT", "MOF", "IOST", "MCO", "WAVES", "XVG", "MONA", "BTS", "BCN", "HC", "MAID", "NEXO", "ARDR", "DX", "OKB", "FXC",
"RLC", "MB", "BKK", "AE", "ENJ", "STEEM", "SLV", "BRZE", "ZIL", "VEST", "ZEN", "SOLVE", "CHZ", "NOAH", "LA", "BTMX",
"ETN", "ENG", "ILC", "NPXS", "CRPT", "GNT", "SNT", "ELF", "JWL", "FET", "BOTX", "NRG", "DGD", "EXMR", "EURS", "AOA",
"RIF", "CIX100", "BF", "XZC", "FAB", "GRIN", "NET", "VERI", "DGTX", "KNC", "REN", "STRAT", "ETP", "NEX", "NEW",
"BCZERO", "GXC", "TNT", "BTC2", "PPT", "USDK", "ELA", "IGNIS", "PLC", "BNK", "DTR", "RCN", "HPT", "LAMB", "MANA",
"EDC", "BEAM", "TT", "AION", "BZ", "WTC", "WICC", "LRC", "BRD", "FCT", "NULS", "FTM", "IOTX", "QBIT", "XMX", "YOU",
"NAS", "WAXP", "ARK", "RDD", "GNY", "ACVC", "HYN", "CVC", "WAN", "WIN", "LINA", "R", "PAI", "FSN", "FUN", "DPT",
"BHD", "LOOM", "XAC", "BUSD", "BHP", "TRUE", "LOKI", "QASH", "BNT"]

jan2018_top200 =  ["BTC", "XRP", "ETH", "BCH", "ADA", "XEM", "LTC", "TRX", "XLM", "MIOTA", "DASH", "EOS", "XMR", "NEO", "QTUM", "BTG",
"ETC", "LSK", "ICX", "NANO", "SC", "BCN", "ZEC", "XVG", "OMG", "BCC", "BTS", "PPT", "DOGE", "DCN", "BNB", "SNT",
"ARDR", "KCS", "STRAT", "STEEM", "USDT", "WAVES", "VEN", "DGB", "KMD", "DRGN", "HC", "KIN", "ETN", "QNT", "REP",
"VGX", "VERI", "ARK", "XP", "BAT", "RDD", "DCR", "QASH", "DENT", "LRC", "PAC", "SALT", "FUN", "NXS", "KNC", "PIVX",
"ZRX", "POWR", "FCT", "AION", "AE", "REQ", "ELF", "SUB", "XDN", "BTM", "WAXP", "NXT", "RHOC", "MAID", "GBYTE", "NAS",
"MONA", "ICN", "GAS", "BTCD", "SYS", "SAN", "QSP", "LINK", "ENG", "XZC", "TNB", "POE", "PAY", "ZCL", "WTC", "GNO",
"CVC", "DGD", "VEE", "RDN", "LEND", "GXC", "ACT", "DBC", "STORM", "STORJ", "ATM", "ENJ", "GAME", "NEBL", "SMART",
"VTC", "INK", "SKY", "NULS", "BTX", "XBY", "UKG", "BAY", "CND", "CNX", "UTK", "PHX", "MED", "PLR", "NAV", "UBQ",
"MCO", "BLOCK", "R", "ANT", "CTR", "BNT", "SNM", "CMT", "MANA", "COB", "AST", "DATA", "ITC", "EDG", "RCN", "SNGLS",
"TRIG", "DNT", "RLC", "AMB", "BRD", "EMC2", "PART", "ADX", "BURST", "ETP", "MOON", "WABI", "WINGS", "ECA", "FLASH",
"BCO", "EMC", "FUEL", "1ST", "OST", "THC", "PPP", "TNT", "SRN", "PPC", "XCP", "MGO", "XSH", "DCT", "ZEN", "LBC",
"XAS", "MOD", "MLN", "EDO", "AGRS", "RISE", "CDT", "MTL", "LA", "QRL", "WGR", "GVT", "CLOAK", "HST", "GTO", "NYC",
"PRL", "SPANK", "VIA", "GRS", "BCPT", "RVR", "YOYOW", "DPY", "NLG", "CFI"]
 
tickers = tickers + dec2019_top200 + jan2018_top200

'''BN->JSON'''
start_date='1 Jan, 2018'
end_date='1 July, 2022'
interval = Client.KLINE_INTERVAL_1DAY
interval_name = '1DAY'

bn_pull_input_coins_hist_price_json(tickers, bn_api_key, bn_api_secret, start_date, end_date, interval, interval_name)

# update old alts data
conn = connect_to_db(DB_NAME, DB_HOST, DB_USERNAME, DB_PASSWORD)
cursor = conn.cursor()
try:
    create_table_query = """
    CREATE TABLE IF NOT EXISTS alt_analysis_historical_price (
        symbol VARCHAR(20) NOT NULL,
        date TIMESTAMPTZ NOT NULL,
        open NUMERIC NOT NULL,
        high NUMERIC NOT NULL,
        low NUMERIC NOT NULL,
        close NUMERIC NOT NULL,
        volume NUMERIC NOT NULL,
        UNIQUE (symbol, date)
    );
    """
    cursor.execute(create_table_query)
    conn.commit()
    print(f"alt_analysis_historical_price_current created successfully.")
except Exception as e:
    print(f"Failed to create table: {str(e)}")
    conn.rollback()
finally:
    cursor.close()


alt_json_folder = DATA_FOLDER+'/alt_analysis_data/1DAY'
for filename in os.listdir(alt_json_folder):
    if filename.endswith('.json'):
        file_path = os.path.join(alt_json_folder, filename)
        try:
            cursor = conn.cursor()
            try:
                with open(file_path, 'r') as file:
                    data = json.load(file)

                    extracted_data = []
                    for entry in data:
                        symbol_name = os.path.splitext(os.path.basename(file_path))[0]
                        open_time = pd.to_datetime(entry[0], unit='ms').strftime('%Y-%m-%d')
                        open_price = entry[1]
                        high_price = entry[2]
                        low_price = entry[3]
                        close_price = entry[4]
                        volume = entry[5]
                        extracted_data.append([symbol_name, open_time, open_price, high_price, low_price, close_price, volume])
                    
                    # Insert data into the database
                    insert_query = """
                    INSERT INTO alt_analysis_historical_price (symbol, date, open, high, low, close, volume)
                    VALUES %s
                    ON CONFLICT (symbol, date)
                    DO UPDATE SET
                        open = EXCLUDED.open,
                        high = EXCLUDED.high,
                        low = EXCLUDED.low,
                        close = EXCLUDED.close,
                        volume = EXCLUDED.volume
                    """
                    execute_values(cursor, insert_query, extracted_data)
                    conn.commit()
            except Exception as e:
                print(f"Failed to insert data from {file_path}: {e}")
                conn.rollback()
            finally:
                cursor.close()
        except Exception as e:
            print(f'Error processing {filename}: {e}')
            continue
    print(f'Inserted {filename} historical price')


