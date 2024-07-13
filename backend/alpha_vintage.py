import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()
api_key = os.getenv('ALPHA_VANTAGE_FREE_API') 

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