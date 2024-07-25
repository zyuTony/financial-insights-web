import json 
import os
from dotenv import load_dotenv
import json
import pandas as pd 
from cmc_utlis import * 
 
'''
1. get the cointegration of all coins historical data
    a. get historical daily/weekly price for top 10 MC coins
    b. sample different time frame to test to make sure each is good
    c. calculate cointegration for the 1000 combos

2. repeat above for 15m, 2h, 4h, 1D  
'''
top_n_coins = 100
interval = '24h' 
output_file = '../data/daily_coin_price.csv'


load_dotenv()
api_key = os.getenv('CMC_API') 
coins_data = []

data = pull_coin_list(top_n_coins, api_key)
ids, symbols= coin_list_json_to_array(data)
print(f'coins to pull: {symbols}')

for coin_id in ids:
    try:
        # Extract data
        with open('./hist_data/hist_price_{}_{}.json'.format(coin_id, interval), 'r') as file:
            data = json.load(file)
        
        for quote in data['data'][coin_id]['quotes']:
            coins_data.append({
                'id': coin_id,
                'symbol': data['data'][coin_id]['symbol'],
                'timestamp': quote['timestamp'],
                'price': quote['quote']['USD']['price']
            }) 

    except FileNotFoundError:
        print(f"Data file for coin ID {coin_id} not found.")
    except KeyError as e:
        print(f"Key error for coin ID {coin_id}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred for coin ID {coin_id}: {e}")

# transform the df    
df = pd.DataFrame(coins_data)
df_pivot = df.pivot(index='timestamp', columns='symbol', values='price')
df_pivot.rename(columns={'timestamp': 'date'}, inplace=True)
df_pivot.fillna(-1, inplace=True)

df_pivot.to_csv(output_file)
print(f'Finished! data saved to {output_file}')

 