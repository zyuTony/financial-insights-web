from abc import ABC, abstractmethod
import json
from config import *
import logging
from datetime import datetime
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import requests
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)8s | %(message)s',
    datefmt='%Y-%m-%d %H:%M' #datefmt='%Y-%m-%d %H:%M:%S'
)
 
class api_getter(ABC): 
    def __init__(self, api_key, data_save_path):
        self.api_key = api_key
        self.data_save_path = data_save_path
    
    @abstractmethod
    def _get_download_symbol_list(self):
        pass
    
    @abstractmethod
    def download_data(self):
        pass
    
class coin_gecko_daily_ohlc_api_getter(api_getter):
    
    def __init__(self, api_key, data_save_path, start_date, end_date):
        super().__init__(api_key, data_save_path)
        self.num_download_symbols = 300 
        self.start_date = start_date if start_date is not None else datetime.strptime('2018-02-10', '%Y-%m-%d')
        self.end_date = end_date if end_date is not None else datetime.now() 
        self.overview_save_path = GECKO_JSON_PATH+'/mapping/top_symbol_by_mc.json'
        
    def _get_unix_from_date_object(self, date_object):
        return int(date_object.timestamp())
       
    def _pull_coin_list_ranking(self, page_num):
        url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=250&page={page_num}"
        headers = {
            "accept": "application/json",
            "x-cg-pro-api-key": self.api_key
        }
        try:
            response = requests.get(url, headers=headers)
            data = response.json()

            with open(self.overview_save_path, 'w') as file:
                json.dump(data, file, indent=4)
            
            return data
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)
            return -1
 
    def _get_download_symbol_list(self):
        # get top coins
        symbols_ranking = []
        for page_num in range(1, 6): # pull top 1500 coins just in case
            symbols_ranking.extend(self._pull_coin_list_ranking(page_num))

        ids = [item["id"] for item in symbols_ranking][:self.num_download_symbols]
        symbols = [item["symbol"].upper() for item in symbols_ranking][:self.num_download_symbols]
        return ids, symbols
    
    def download_data(self):
        ids, symbols = self._get_download_symbol_list()
        
        unix_start = self._get_unix_from_date_object(self.start_date)
        unix_end = self._get_unix_from_date_object(self.end_date)
        logging.debug(f"start downloading symbol list:{symbols}") 
        
        for id, symbol in zip(ids, symbols):
            all_data = []    
            current_start = unix_start
            while current_start < unix_end:
                current_end = min(current_start + DAYS_PER_API_LIMIT * 24 * 60 * 60, unix_end)
                try:
                    url = f"https://pro-api.coingecko.com/api/v3/coins/{id}/ohlc/range?vs_currency=usd&from={current_start}&to={current_end}&interval=daily"
                    headers = {
                        "accept": "application/json",
                        "x-cg-pro-api-key": self.api_key
                    }            
                    response = requests.get(url, headers=headers)
                    if response.status_code == 200:
                        all_data.extend(response.json())  
                        logging.debug(f"Downloaded data for {symbol} from {current_start} to {current_end}")
                    else:
                        logging.error(f"Failed to download data for {symbol} from {current_start} to {current_end}: {response.status_code} {response.text}")
                    
                    current_start = current_end + 1
                except Exception as e:
                    logging.exception(f"Exception occurred while downloading data for {symbol} from {unix_start} to {current_end}: {e}")
                    break

            with open(self.data_save_path+f'/{symbol}.json', 'w') as file:
                json.dump(all_data, file, indent=4)
            logging.info(f"Saved full data for {symbol} to {symbol}.json")
         
class coin_gecko_hourly_ohlc_api_getter(coin_gecko_daily_ohlc_api_getter):     
    '''slight change of download_data from daily ohlc api'''
    def download_data(self):
        ids, symbols = self._get_download_symbol_list()
        
        unix_start = self._get_unix_from_date_object(self.start_date)
        unix_end = self._get_unix_from_date_object(self.end_date)
        logging.debug(f"start downloading symbol list:{symbols}") 
        
        for id, symbol in zip(ids, symbols):
            all_data = []    
            current_start = unix_start
            while current_start < unix_end:
                current_end = min(current_start + DAYS_PER_API_LIMIT_HOURLY * 24 * 60 * 60, unix_end)
                try:
                    url = f"https://pro-api.coingecko.com/api/v3/coins/{id}/ohlc/range?vs_currency=usd&from={current_start}&to={current_end}&interval=hourly"
                    headers = {
                        "accept": "application/json",
                        "x-cg-pro-api-key": self.api_key
                    }            
                    response = requests.get(url, headers=headers)
                    if response.status_code == 200:
                        all_data.extend(response.json())  
                        logging.debug(f"Downloaded data for {symbol} from {current_start} to {current_end}")
                    else:
                        logging.error(f"Failed to download data for {symbol} from {current_start} to {current_end}: {response.status_code} {response.text}")
                    
                    current_start = current_end + 1
                except Exception as e:
                    logging.exception(f"Exception occurred while downloading data for {symbol} from {unix_start} to {current_end}: {e}")
                    break

            with open(self.data_save_path+f'/{symbol}.json', 'w') as file:
                json.dump(all_data, file, indent=4)
            logging.info(f"Saved full data for {symbol} to {symbol}.json")

class avan_stock_daily_ohlc_api_getter(api_getter):
    
    def __init__(self, api_key, data_save_path, start_date, end_date, additional_tickers=None):
        super().__init__(api_key, data_save_path)
        self.num_download_symbols = 2000 
        self.top_symbols_list_path = SEC_STOCK_TICKERS
        self.start_date = None
        self.end_date = None 
        self.additional_tickers = additional_tickers
       
    def _get_download_symbol_list(self):
        with open(self.top_symbols_list_path, 'r') as file:
            data = json.load(file)
        symbols = []
        for _, value in data.items():
            symbols.append(value["ticker"])
        if self.additional_tickers:
            symbols.extend(self.additional_tickers)
        return symbols[:self.num_download_symbols]

    def download_data(self):
        symbols = self._get_download_symbol_list()
        for symbol in symbols:
            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&outputsize=full&apikey={self.api_key}'

            response = requests.get(url)
            json_file_path = self.data_save_path + f'/{symbol}.json'
            if response.status_code == 200:
                data = response.json()
                with open(json_file_path, 'w') as file:
                    json.dump(data, file, indent=4)
                logging.info(f"{symbol} saved to {json_file_path}")
            else:
                logging.error(f"Error fetching {symbol}: {response.status_code}")
            time.sleep(AVAN_SLEEP_TIME)      
        
class avan_stock_overview_api_getter(avan_stock_daily_ohlc_api_getter):
    def download_data(self):
        symbols = self._get_download_symbol_list()
        for symbol in symbols:
            url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={self.api_key}'

            response = requests.get(url)
            json_file_path = self.data_save_path + f'/{symbol}.json'
            if response.status_code == 200:
                data = response.json()
                with open(json_file_path, 'w') as file:
                    json.dump(data, file, indent=4)
                logging.info(f"{symbol} saved to {json_file_path}")
            else:
                logging.error(f"Error fetching {symbol}: {response.status_code}")
            time.sleep(AVAN_SLEEP_TIME)  