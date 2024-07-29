import requests
import os
from dotenv import load_dotenv
import json
import pandas as pd
from sqlalchemy import create_engine

load_dotenv()
api_key = os.getenv('POLYGON_API') 
 
saved_file_name = "./sec_stock_tickers"
 
with open(f'{saved_file_name}.json', 'r') as file:
    data = json.load(file)


cik_str = []
ticker = []
title = []

for key, value in data.items():
    cik_str.append(value["cik_str"])
    ticker.append(value["ticker"])
    title.append(value["title"])
print(len(ticker))

# print("cik_str:", cik_str)
# print("ticker:", ticker)
# print("title:", title)