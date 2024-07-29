import requests
import os
from dotenv import load_dotenv
import json
import pandas as pd
from sqlalchemy import create_engine

load_dotenv()
api_key = os.getenv('POLYGON_API') 
username = os.getenv('RDS_USERNAME') 
password = os.getenv('RDS_PASSWORD') 
endpoint = os.getenv('RDS_ENDPOINT') 
db_name = 'financial_data' 


# API data retrieval
# function =
# ticker =
# timeframe =
if api_key is None:
    raise ValueError("API key is missing. Please set it in the .env file.")
# url = f'https://api.polygon.io/v2/reference/news?ticker=GPS&limit=10&apiKey={api_key}'
url = f'https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&limit=100&apiKey={api_key}'
saved_file_name = "polygon_tickers"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    with open(f'{saved_file_name}.json', 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Data saved to {saved_file_name}")
else:
    print(f"Error fetching data: {response.status_code}")

# save to sql database
# timeframe = "Weekly Adjusted Time Series"
# with open('./alpha_vantage_data.json', 'r') as file:
#     data = json.load(file)

# time_series = data.get(timeframe, {})
# records = []
# for timestamp, values in time_series.items():
#     record = {
#         "timestamp": timestamp,
#         "open": float(values["1. open"]),
#         "high": float(values["2. high"]),
#         "low": float(values["3. low"]),
#         "close": float(values["4. close"]),
#         "adjusted_close": float(values["5. adjusted close"]),
#         "volume": int(values["6. volume"]),
#         "dividend_amount": float(values["7. dividend amount"])
#     }
#     records.append(record)
# df = pd.DataFrame(records)

# db_uri = f'postgresql://{username}:{password}@{endpoint}:5432/{db_name}' 
# engine = create_engine(db_uri)
# df.to_sql('gap_full_weekly', engine, if_exists='replace', index=False)
# print("Data saved to PostgreSQL database on AWS.")
