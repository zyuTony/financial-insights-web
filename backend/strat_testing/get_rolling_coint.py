'''
With a input of window length and a df with columns of date and series of stock data, it returns a rolling window cointegration score and p-value for all possible data pairs, each as one column.

return: pd.DataFrame; CSV file
'''

import os
import json
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import coint

def rolling_cointegration(name1, data1, name2, data2, window_length):
    
    if len(df) < window_length:
        raise ValueError("The length of the time window is greater than the available df.")
    
    rolling_coint_scores = []
    rolling_p_values = []

    for end in range(window_length, len(df)):
        start = end - window_length
        series1 = data1[start:end]
        series2 = data2[start:end]
        
        score, p_value, _ = coint(series1, series2)
        
        rolling_coint_scores.append(score)
        rolling_p_values.append(p_value) 

    # results = pd.DataFrame({
    #     'coint_score': rolling_coint_scores,
    #     'p_value': rolling_p_values
    # })
    # results.columns = [f'{name1}_{name2}_coint_score', f'{name1}_{name2}_p_val']
    
    results = pd.DataFrame({
        'p_value': rolling_p_values
    })
    results.columns = [f'{name1}_{name2}_p_val']

    return results


'''
BINANCE data
'''
# window_length = 180
# df = pd.read_csv("../data/binance_agg_data.csv")
# date = df['date'][window_length:]
# df = df.drop('date', axis=1)
# df = df.iloc[:,:11]

# # save progress of analyzed coin pairs
# checkpoint_file = '../data/coint_pair_checkpoint.json'
# if os.path.exists(checkpoint_file):
#     with open(checkpoint_file, 'r') as file:
#         checkpoint_data = json.load(file)
# else:
#     checkpoint_data = []
# results = pd.DataFrame()

# # get rolling coint for all possible pairs
# for i in range(df.shape[1]):
#     for j in range(i+1, df.shape[1]):
#         # save progress
#         name1 = df.columns[i]
#         name2 = df.columns[j]
#         if [name1, name2] in checkpoint_data:
#             print(f"Skip pair {name1} X {name2} since already ran")
#             continue
        
#         # try rolling cointegration
#         try:
#             data1 = df.iloc[:, i]
#             data2 = df.iloc[:, j]
#             print(f'Working on {name1} X {name2}')
#             res = rolling_cointegration(name1, data1, name2, data2, window_length)
#             results = pd.concat([results, res], axis=1)
#             checkpoint_data.append([name1, name2])
#         except Exception as e:
#             print(f'Error processing {name1} X {name2}: {e}')
#             continue

# # save results to csv
# results = pd.concat([date.reset_index(drop=True), results], axis=1)
# results.to_csv('../data/final_coint_binance_data.csv', index=False)
# with open(checkpoint_file, 'w') as file:
#         json.dump(checkpoint_data, file, indent=4)
        

'''
stock data
'''
window_length = 180
df = pd.read_csv("../data/stock_agg_data.csv")
date = df['date'][window_length:].reset_index(drop=True)
df = df.drop('date', axis=1)
df = df.iloc[5000:,:100]

# save progress of analyzed coin pairs
checkpoint_file = '../data/stock_pair_checkpoint.json'
if os.path.exists(checkpoint_file):
    with open(checkpoint_file, 'r') as file:
        checkpoint_data = json.load(file)
else:
    checkpoint_data = []
results = pd.DataFrame()

# get rolling coint for all possible pairs
for i in range(df.shape[1]):
    name1 = df.columns[i]
    data1 = df.iloc[:, i]
    print(f'--- Start with {name1}')
    for j in range(i+1, df.shape[1]):
        # save progress
        name2 = df.columns[j]      
        if [name1, name2] in checkpoint_data:
            print(f"Skip pair {name1} X {name2} since already ran")
            continue
        # try rolling cointegration
        try:
            data2 = df.iloc[:, j]
            print(f'Working on {name1} X {name2}')
            res = rolling_cointegration(name1, data1, name2, data2, window_length)
            results = pd.concat([results, res], axis=1)
            checkpoint_data.append([name1, name2])
        except Exception as e:
            print(f'Error processing {name1} X {name2}: {e}')
            continue
    try:
        print(f'--- Saving all {name1} pairs')
        with open(checkpoint_file, 'w') as file:
            json.dump(checkpoint_data, file, indent=4)
        try:
            results.to_csv('../data/final_coint_stock_data_top_100.csv', index=False)
        except Exception as e:  
            print(f"Error: {e} but continue")    
    except Exception as e:
        print(f"Error: {e} but continue")
        continue
# save results to csv
results = pd.concat([date, results.reset_index(drop=True)], axis=1)
results.to_csv('../data/final_coint_stock_data_top_100.csv', index=False)
