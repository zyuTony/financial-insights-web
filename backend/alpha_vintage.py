import requests
import os
from dotenv import load_dotenv
import json
import pandas as pd
from sqlalchemy import create_engine

load_dotenv()
api_key = os.getenv('ALPHA_VANTAGE_FREE_API') 
username = os.getenv('RDS_USERNAME') 
password = os.getenv('RDS_PASSWORD') 
endpoint = os.getenv('RDS_ENDPOINT') 
db_name = 'financial_data' 

# function =
# ticker =
# timeframe =

if api_key is None:
    raise ValueError("API key is missing. Please set it in the .env file.")
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey={api_key}'

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    with open('alpha_vantage_data.json', 'w') as file:
        json.dump(data, file, indent=4)
    print("Data saved to alpha_vantage_data.json")
else:
    print(f"Error fetching data: {response.status_code}")

timeframe = "Time Series (5min)"
if response.status_code == 200:
    data = response.json()
    time_series = data.get(timeframe, {})
    
    records = []
    for timestamp, values in time_series.items():
        high = float(values["2. high"])
        low = float(values["3. low"])
        close = float(values["4. close"])
        hlc3 = (high + low + close) / 3
        records.append({"timestamp": timestamp, "hlc3": hlc3})
    
    df = pd.DataFrame(records)
    
    db_uri = f'postgresql://{username}:{password}@{endpoint}:5432/{db_name}' 
    engine = create_engine(db_uri)
    df.to_sql('ibm_data_5min', engine, if_exists='replace', index=False)
    print("Data saved to PostgreSQL database on AWS.")
else:
    print(f"Error fetching data: {response.status_code}")