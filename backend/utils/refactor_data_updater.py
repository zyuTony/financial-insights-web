from abc import ABC, abstractmethod
import os
import json
import pandas as pd
import psycopg2
from psycopg2 import OperationalError
from psycopg2.extras import execute_values
from config import *
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)8s | %(message)s',
    datefmt='%Y-%m-%d %H:%M' #datefmt='%Y-%m-%d %H:%M:%S'
)

def convert_to_float(value):
    if value is None or value == "" or value == "None" or value == "-":
        return None
    try:
        return float(value)
    except (ValueError, TypeError) as e:
        logging.error(f"Error converting to float: {e}")
        return None

def convert_to_int(value):
    if value is None or value == "" or value == "None" or value == "-":
        return None
    try:
        return int(value)
    except (ValueError, TypeError) as e:
        logging.error(f"Error converting to int: {e}")
        return None
    
def convert_to_date(value):
    if value in ("None", '-'):
        return None
    try:
        return datetime.strptime(value, '%Y-%m-%d').date()
    except ValueError as e:
        logging.error(f"Error converting to date: {e}")
        return None

def convert_to_datetime(date_str):
    try:
        return datetime.fromisoformat(date_str.replace("Z", ""))
    except ValueError as e:
        logging.error(f"Error converting to datetime: {e}")
        return None
    
def truncate_string(value, length):
    try:
        if value and len(value) > length:
            logging.warning(f'Truncating {value} at {length}')
        return value[:length] if value and len(value) > length else value
    except Exception as e:
        logging.error(f"Error truncating string: {e}")
        return None


class db_refresher(ABC): 
    '''object that 1) connect to db 2) transform and insert json data depends on source.
       template for coin_gecko_db and avan_stock_db'''
    def __init__(self, db_name, db_host, db_username, db_password, table_name):
        self.db_name = db_name
        self.db_host = db_host
        self.db_username = db_username
        self.db_password = db_password
        self.conn = None
        self.table_name = table_name  
        self.table_creation_script = None  # This will be set in child classes
        self.data_insertion_script = None  # This will be set in child classes
         
    def connect(self):
        try:
            self.conn = psycopg2.connect(
                host=self.db_host,
                database=self.db_name,
                user=self.db_username,
                password=self.db_password)
            print(f"Connected to {self.db_host} {self.db_name}!")
        except OperationalError as e:
            print(f"Error connecting to database: {e}")
            self.conn = None

    def close(self):
        if self.conn:
            self.conn.close()
            print("Database connection closed.")
      
    def create_table(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute(self.table_creation_script)
            self.conn.commit()
            logging.info(f"{self.table_name} created successfully.")
        except Exception as e:
            logging.error(f"Failed to create table: {str(e)}")
            self.conn.rollback()
        finally:
            cursor.close()
    
    @abstractmethod
    def _data_transformation(self, file_path):
        pass
    
    def insert_data(self, file_path):
        time_series_data = self._data_transformation(file_path)
        cursor = self.conn.cursor()
        try:
            execute_values(cursor, self.data_insertion_script, time_series_data)
            self.conn.commit()
            logging.debug(f"Inserted into {self.table_name} from {file_path}")
        except Exception as e:
            logging.error(f"Failed to insert data from {file_path}: {e}")
            self.conn.rollback()
        finally:
            cursor.close()

class coin_gecko_OHLC_db_refresher(db_refresher):
    '''handle all data insertion from OHLC data via coin gecko api'''
    def __init__(self, *args):
        super().__init__(*args)
        
        self.table_creation_script = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            symbol VARCHAR(20) NOT NULL,
            date TIMESTAMPTZ NOT NULL,
            open NUMERIC NOT NULL,
            high NUMERIC NOT NULL,
            low NUMERIC NOT NULL,
            close NUMERIC NOT NULL,
            PRIMARY KEY (symbol, date)
        );
        """
        
        self.data_insertion_script = f"""
        INSERT INTO {self.table_name} (symbol, date, open, high, low, close)
        VALUES %s
        ON CONFLICT (symbol, date)
        DO UPDATE SET
            open = EXCLUDED.open,
            high = EXCLUDED.high,
            low = EXCLUDED.low,
            close = EXCLUDED.close
        WHERE {self.table_name}.open <> EXCLUDED.open
            OR {self.table_name}.high <> EXCLUDED.high
            OR {self.table_name}.low <> EXCLUDED.low
            OR {self.table_name}.close <> EXCLUDED.close;
        """
        
    def _data_transformation(self, file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
            symbol = os.path.splitext(os.path.basename(file_path))[0]
            outputs = []
            seen_dates = set()
            
            for entry in data:
                date = pd.to_datetime(entry[0], unit='ms').strftime('%Y-%m-%d')
                open_price  = entry[1]
                high = entry[2]
                low = entry[3]
                close = entry[4]
                               
                if date not in seen_dates:# this is to deal with gc duplicated data that cause errors sometimes
                    outputs.append([symbol, date, open_price, high, low, close])
                    seen_dates.add(date)  
            return outputs     
        except Exception as e:
            logging.debug(f"Data transformation failed for {symbol}: {e}")
            return None
            
class coin_gecko_OHLC_hourly_db_refresher(coin_gecko_OHLC_db_refresher):
    '''small tweak to store by minutes timestamp compared to parent''' 
    def _data_transformation(self, file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
            symbol = os.path.splitext(os.path.basename(file_path))[0]
            outputs = []
            seen_dates = set()
            
            for entry in data:
                date = pd.to_datetime(entry[0], unit='ms').strftime('%Y-%m-%d %H:%M')
                open_price  = entry[1]
                high = entry[2]
                low = entry[3]
                close = entry[4]
                               
                if date not in seen_dates:# this is to deal with gc duplicated data that cause errors sometimes
                    outputs.append([symbol, date, open_price, high, low, close])
                    seen_dates.add(date)  
            return outputs     
        except Exception as e:
            logging.debug(f"Data transformation failed for {symbol}: {e}")
            return None
     
class avan_stock_OHLC_db_refresher(db_refresher):
    '''handle all data insertion from OHLC data via alpha vantage api'''
    def __init__(self, *args):
        super().__init__(*args)
        
        self.table_creation_script = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            symbol VARCHAR(10) NOT NULL,
            date TIMESTAMPTZ NOT NULL,
            open NUMERIC NOT NULL,
            high NUMERIC NOT NULL,
            low NUMERIC NOT NULL,
            close NUMERIC NOT NULL,
            volume BIGINT NOT NULL,
            PRIMARY KEY (symbol, date)
        );
        """
        
        self.data_insertion_script = f"""
        INSERT INTO {self.table_name} (symbol, date, open, high, low, close, volume)
            VALUES %s
            ON CONFLICT (symbol, date)
            DO UPDATE SET 
                open = EXCLUDED.open,
                high = EXCLUDED.high,
                low = EXCLUDED.low,
                close = EXCLUDED.close,
                volume = EXCLUDED.volume
            WHERE {self.table_name}.open <> EXCLUDED.open
               OR {self.table_name}.high <> EXCLUDED.high
               OR {self.table_name}.low <> EXCLUDED.low
               OR {self.table_name}.close <> EXCLUDED.close
               OR {self.table_name}.volume <> EXCLUDED.volume;
        """
    
    def _data_transformation(self, file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
            
            symbol = data["Meta Data"]["2. Symbol"]
            time_series_data = data["Time Series (Daily)"]
            
            outputs = []
            for date_str, metrics in time_series_data.items():
                output = (
                    symbol,
                    datetime.strptime(date_str, '%Y-%m-%d'),
                    float(metrics["1. open"]),
                    float(metrics["2. high"]),
                    float(metrics["3. low"]),
                    float(metrics["4. close"]),
                    int(metrics["6. volume"])
                )
                outputs.append(output)
            return outputs 
        except Exception as e:
            logging.debug(f"Data transformation failed: {e}")
            return None
       
class coin_gecko_overview_db_refresher(db_refresher):
    '''handle all data insertion from OHLC data via coin gecko api'''
    def __init__(self, *args):
        super().__init__(*args)
        self.table_creation_script = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            symbol VARCHAR(10) NOT NULL,
            name VARCHAR(255),
            current_price DECIMAL(20, 8),  
            market_cap BIGINT,
            market_cap_rank INT,
            fully_diluted_valuation BIGINT,
            total_volume BIGINT,
            high_24h DECIMAL(20, 8),  
            low_24h DECIMAL(20, 8),  
            price_change_24h DECIMAL(20, 8),  
            price_change_percentage_24h DECIMAL(10, 6),  
            market_cap_change_24h BIGINT,
            market_cap_change_percentage_24h DECIMAL(10, 6),  
            circulating_supply DECIMAL(30, 10),  
            total_supply DECIMAL(30, 10),  
            max_supply DECIMAL(30, 10),  
            ath DECIMAL(20, 8),  
            ath_date TIMESTAMP,
            atl DECIMAL(20, 8),  
            atl_date TIMESTAMP,
            last_updated TIMESTAMP,
            PRIMARY KEY (symbol, name)
        );
        """
        
        self.data_insertion_script = f"""
        INSERT INTO {self.table_name} (
            symbol, name, current_price, market_cap, market_cap_rank,
            fully_diluted_valuation, total_volume, high_24h, low_24h, price_change_24h, price_change_percentage_24h, market_cap_change_24h, market_cap_change_percentage_24h,
            circulating_supply, total_supply, max_supply, ath, ath_date,
            atl, atl_date, last_updated
        ) VALUES %s
        ON CONFLICT (symbol, name)
        DO UPDATE SET
            current_price = EXCLUDED.current_price,
            market_cap = EXCLUDED.market_cap,
            market_cap_rank = EXCLUDED.market_cap_rank,
            fully_diluted_valuation = EXCLUDED.fully_diluted_valuation,
            total_volume = EXCLUDED.total_volume,
            high_24h = EXCLUDED.high_24h,
            low_24h = EXCLUDED.low_24h,
            price_change_24h = EXCLUDED.price_change_24h,
            price_change_percentage_24h = EXCLUDED.price_change_percentage_24h,
            market_cap_change_24h = EXCLUDED.market_cap_change_24h,
            market_cap_change_percentage_24h = EXCLUDED.market_cap_change_percentage_24h,
            circulating_supply = EXCLUDED.circulating_supply,
            total_supply = EXCLUDED.total_supply,
            max_supply = EXCLUDED.max_supply,
            ath = EXCLUDED.ath,
            ath_date = EXCLUDED.ath_date,
            atl = EXCLUDED.atl,
            atl_date = EXCLUDED.atl_date,
            last_updated = EXCLUDED.last_updated
        """
        
    def _data_transformation(self, file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
            outputs = []
            for entry in data:
                output = (
                    entry.get("symbol").upper(),
                    entry.get("name"),
                    convert_to_float(entry.get("current_price")),
                    convert_to_int(entry.get("market_cap")),
                    convert_to_int(entry.get("market_cap_rank")),
                    convert_to_int(entry.get("fully_diluted_valuation")),
                    convert_to_int(entry.get("total_volume")),
                    convert_to_float(entry.get("high_24h")),
                    convert_to_float(entry.get("low_24h")),
                    convert_to_float(entry.get("price_change_24h")),
                    convert_to_float(entry.get("price_change_percentage_24h")),
                    convert_to_int(entry.get("market_cap_change_24h")),
                    convert_to_float(entry.get("market_cap_change_percentage_24h")),
                    convert_to_float(entry.get("circulating_supply")),
                    convert_to_float(entry.get("total_supply")),
                    convert_to_float(entry.get("max_supply")),
                    convert_to_float(entry.get("ath")),
                    convert_to_datetime(entry.get("ath_date")),
                    convert_to_float(entry.get("atl")),
                    convert_to_datetime(entry.get("atl_date")),
                    convert_to_datetime(entry.get("last_updated"))
                ) 
                outputs.append(output)
                return outputs
        except Exception as e:
            logging.debug(f"Data transformation failed for {self.table_name}: {e}")
            return None
      
class avan_stock_overview_db_refresher(db_refresher):
    '''handle all data insertion from OHLC data via coin gecko api'''
    def __init__(self, *args):
        super().__init__(*args)
        self.table_creation_script = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            Symbol VARCHAR(10) PRIMARY KEY,
            AssetType VARCHAR(50),
            Name VARCHAR(255),
            Description TEXT,
            CIK VARCHAR(10),
            Exchange VARCHAR(10),
            Currency VARCHAR(10),
            Country VARCHAR(50),
            Sector VARCHAR(50),
            Industry VARCHAR(255),
            Address VARCHAR(255),
            FiscalYearEnd VARCHAR(20),
            LatestQuarter DATE,
            MarketCapitalization BIGINT,
            EBITDA BIGINT,
            PERatio DECIMAL(10, 2),
            PEGRatio DECIMAL(10, 3),
            BookValue DECIMAL(10, 2),
            DividendPerShare DECIMAL(10, 2),
            DividendYield DECIMAL(10, 4),
            EPS DECIMAL(10, 2),
            RevenuePerShareTTM DECIMAL(10, 2),
            ProfitMargin DECIMAL(10, 3),
            OperatingMarginTTM DECIMAL(10, 3),
            ReturnOnAssetsTTM DECIMAL(10, 3),
            ReturnOnEquityTTM DECIMAL(10, 3),
            RevenueTTM BIGINT,
            GrossProfitTTM BIGINT,
            DilutedEPSTTM DECIMAL(10, 2),
            QuarterlyEarningsGrowthYOY DECIMAL(10, 3),
            QuarterlyRevenueGrowthYOY DECIMAL(10, 3),
            AnalystTargetPrice DECIMAL(10, 2),
            AnalystRatingStrongBuy INT,
            AnalystRatingBuy INT,
            AnalystRatingHold INT,
            AnalystRatingSell INT,
            AnalystRatingStrongSell INT,
            TrailingPE DECIMAL(10, 2),
            ForwardPE DECIMAL(10, 2),
            PriceToSalesRatioTTM DECIMAL(10, 3),
            PriceToBookRatio DECIMAL(10, 2),
            EVToRevenue DECIMAL(10, 3),
            EVToEBITDA DECIMAL(10, 2),
            Beta DECIMAL(10, 3),
            High52Week DECIMAL(10, 2),
            Low52Week DECIMAL(10, 2),
            MovingAverage50Day DECIMAL(10, 2),
            MovingAverage200Day DECIMAL(10, 2),
            SharesOutstanding BIGINT,
            DividendDate DATE,
            ExDividendDate DATE
        );
        """
        
        self.data_insertion_script = f"""
        INSERT INTO {self.table_name} (
            Symbol, AssetType, Name, Description, CIK, Exchange, Currency, Country, Sector, Industry, Address, FiscalYearEnd, LatestQuarter, 
            MarketCapitalization, EBITDA, PERatio, PEGRatio, BookValue, DividendPerShare, DividendYield, EPS, RevenuePerShareTTM, ProfitMargin, 
            OperatingMarginTTM, ReturnOnAssetsTTM, ReturnOnEquityTTM, RevenueTTM, GrossProfitTTM, DilutedEPSTTM, QuarterlyEarningsGrowthYOY, 
            QuarterlyRevenueGrowthYOY, AnalystTargetPrice, AnalystRatingStrongBuy, AnalystRatingBuy, AnalystRatingHold, AnalystRatingSell, 
            AnalystRatingStrongSell, TrailingPE, ForwardPE, PriceToSalesRatioTTM, PriceToBookRatio, EVToRevenue, EVToEBITDA, Beta, High52Week, 
            Low52Week, MovingAverage50Day, MovingAverage200Day, SharesOutstanding, DividendDate, ExDividendDate
        ) VALUES %s
        ON CONFLICT (Symbol) DO UPDATE SET
            AssetType = EXCLUDED.AssetType,
            Name = EXCLUDED.Name,
            Description = EXCLUDED.Description,
            CIK = EXCLUDED.CIK,
            Exchange = EXCLUDED.Exchange,
            Currency = EXCLUDED.Currency,
            Country = EXCLUDED.Country,
            Sector = EXCLUDED.Sector,
            Industry = EXCLUDED.Industry,
            Address = EXCLUDED.Address,
            FiscalYearEnd = EXCLUDED.FiscalYearEnd,
            LatestQuarter = EXCLUDED.LatestQuarter,
            MarketCapitalization = EXCLUDED.MarketCapitalization,
            EBITDA = EXCLUDED.EBITDA,
            PERatio = EXCLUDED.PERatio,
            PEGRatio = EXCLUDED.PEGRatio,
            BookValue = EXCLUDED.BookValue,
            DividendPerShare = EXCLUDED.DividendPerShare,
            DividendYield = EXCLUDED.DividendYield,
            EPS = EXCLUDED.EPS,
            RevenuePerShareTTM = EXCLUDED.RevenuePerShareTTM,
            ProfitMargin = EXCLUDED.ProfitMargin,
            OperatingMarginTTM = EXCLUDED.OperatingMarginTTM,
            ReturnOnAssetsTTM = EXCLUDED.ReturnOnAssetsTTM,
            ReturnOnEquityTTM = EXCLUDED.ReturnOnEquityTTM,
            RevenueTTM = EXCLUDED.RevenueTTM,
            GrossProfitTTM = EXCLUDED.GrossProfitTTM,
            DilutedEPSTTM = EXCLUDED.DilutedEPSTTM,
            QuarterlyEarningsGrowthYOY = EXCLUDED.QuarterlyEarningsGrowthYOY,
            QuarterlyRevenueGrowthYOY = EXCLUDED.QuarterlyRevenueGrowthYOY,
            AnalystTargetPrice = EXCLUDED.AnalystTargetPrice,
            AnalystRatingStrongBuy = EXCLUDED.AnalystRatingStrongBuy,
            AnalystRatingBuy = EXCLUDED.AnalystRatingBuy,
            AnalystRatingHold = EXCLUDED.AnalystRatingHold,
            AnalystRatingSell = EXCLUDED.AnalystRatingSell,
            AnalystRatingStrongSell = EXCLUDED.AnalystRatingStrongSell,
            TrailingPE = EXCLUDED.TrailingPE,
            ForwardPE = EXCLUDED.ForwardPE,
            PriceToSalesRatioTTM = EXCLUDED.PriceToSalesRatioTTM,
            PriceToBookRatio = EXCLUDED.PriceToBookRatio,
            EVToRevenue = EXCLUDED.EVToRevenue,
            EVToEBITDA = EXCLUDED.EVToEBITDA,
            Beta = EXCLUDED.Beta,
            High52Week = EXCLUDED.High52Week,
            Low52Week = EXCLUDED.Low52Week,
            MovingAverage50Day = EXCLUDED.MovingAverage50Day,
            MovingAverage200Day = EXCLUDED.MovingAverage200Day,
            SharesOutstanding = EXCLUDED.SharesOutstanding,
            DividendDate = EXCLUDED.DividendDate,
            ExDividendDate = EXCLUDED.ExDividendDate
        """
        
    def _data_transformation(self, file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
            
            # Check if the file is empty (i.e., the overview does not exist)
            if not data:
                logging.info(f"Overview does not exist for {file_path}")
                return None

            required_keys = ["Symbol", "AssetType", "Name", "Description", "CIK", "Exchange", "Currency", "Country", "Sector", "Industry", "Address", "FiscalYearEnd", "LatestQuarter", "MarketCapitalization", "EBITDA", "PERatio", "PEGRatio", "BookValue", "DividendPerShare", "DividendYield", "EPS", "RevenuePerShareTTM", "ProfitMargin", "OperatingMarginTTM", "ReturnOnAssetsTTM", "ReturnOnEquityTTM", "RevenueTTM", "GrossProfitTTM", "DilutedEPSTTM", 
            "QuarterlyEarningsGrowthYOY", "QuarterlyRevenueGrowthYOY", "AnalystTargetPrice", 
            "AnalystRatingStrongBuy", "AnalystRatingBuy", "AnalystRatingHold", "AnalystRatingSell", 
            "AnalystRatingStrongSell", "TrailingPE", "ForwardPE", "PriceToSalesRatioTTM", 
            "PriceToBookRatio", "EVToRevenue", "EVToEBITDA", "Beta", "52WeekHigh", "52WeekLow", 
            "50DayMovingAverage", "200DayMovingAverage", "SharesOutstanding", "DividendDate", "ExDividendDate"]
            missing_keys = [key for key in required_keys if key not in data]

            if missing_keys:
                raise KeyError(f"Missing keys in the JSON data: {', '.join(missing_keys)}")
            
            outputs = []
            output = (
                truncate_string(data["Symbol"], 10),
                truncate_string(data["AssetType"], 50),
                truncate_string(data["Name"], 255),
                data["Description"],  
                truncate_string(data["CIK"], 10),
                truncate_string(data["Exchange"], 10),
                truncate_string(data["Currency"], 10),
                truncate_string(data["Country"], 50),
                truncate_string(data["Sector"], 50),
                truncate_string(data["Industry"], 255),
                truncate_string(data["Address"], 255),
                truncate_string(data["FiscalYearEnd"], 20),
                convert_to_date(data["LatestQuarter"]),
                convert_to_int(data["MarketCapitalization"]),
                convert_to_int(data["EBITDA"]),
                convert_to_float(data["PERatio"]),
                convert_to_float(data["PEGRatio"]),
                convert_to_float(data["BookValue"]),
                convert_to_float(data["DividendPerShare"]),
                convert_to_float(data["DividendYield"]),
                convert_to_float(data["EPS"]),
                convert_to_float(data["RevenuePerShareTTM"]),
                convert_to_float(data["ProfitMargin"]),
                convert_to_float(data["OperatingMarginTTM"]),
                convert_to_float(data["ReturnOnAssetsTTM"]),
                convert_to_float(data["ReturnOnEquityTTM"]),
                convert_to_int(data["RevenueTTM"]),
                convert_to_int(data["GrossProfitTTM"]),
                convert_to_float(data["DilutedEPSTTM"]),
                convert_to_float(data["QuarterlyEarningsGrowthYOY"]),
                convert_to_float(data["QuarterlyRevenueGrowthYOY"]),
                convert_to_float(data["AnalystTargetPrice"]),
                convert_to_int(data["AnalystRatingStrongBuy"]),
                convert_to_int(data["AnalystRatingBuy"]),
                convert_to_int(data["AnalystRatingHold"]),
                convert_to_int(data["AnalystRatingSell"]),
                convert_to_int(data["AnalystRatingStrongSell"]),
                convert_to_float(data["TrailingPE"]),
                convert_to_float(data["ForwardPE"]),
                convert_to_float(data["PriceToSalesRatioTTM"]),
                convert_to_float(data["PriceToBookRatio"]),
                convert_to_float(data["EVToRevenue"]),
                convert_to_float(data["EVToEBITDA"]),
                convert_to_float(data["Beta"]),
                convert_to_float(data["52WeekHigh"]),
                convert_to_float(data["52WeekLow"]),
                convert_to_float(data["50DayMovingAverage"]),
                convert_to_float(data["200DayMovingAverage"]),
                convert_to_int(data["SharesOutstanding"]),
                convert_to_date(data["DividendDate"]),
                convert_to_date(data["ExDividendDate"])
            )
            outputs.append(output)    
            return outputs
        
        except Exception as e:
            logging.debug(f"Data transformation failed for {file_path}: {e}")
            return None
      