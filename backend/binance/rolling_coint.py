'''
With a input of window length and a df with columns of date and series of stock data, it returns a rolling window cointegration score and p-value for all possible data pairs, each as one column.

return: pd.DataFrame; CSV file
'''

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
        print(f"working on index {start} to {end-1}")

    results = pd.DataFrame({
        'coint_score': rolling_coint_scores,
        'p_value': rolling_p_values
    })
    results.columns = [f'{name1}_{name2}_coint_score', f'{name1}_{name2}_p_val']
    
    return results

window_length = 100

df = pd.read_csv("../data/daily_coin_price.csv")
df = df[:120]
date = df['timestamp'][window_length:]
df = df.drop('timestamp', axis=1)

results = pd.DataFrame()
n = df.shape[1]
for i in range(n):
    for j in range(i+1, n):
        name1 = df.columns[i]
        name2 = df.columns[j]
        data1 = df.iloc[:, i]
        data2 = df.iloc[:, j]

        res = rolling_cointegration(name1, data1, name2, data2, window_length)
        results = pd.concat([results, res], axis=1)

results = pd.concat([date.reset_index(drop=True), results], axis=1)
results.to_csv('../data/final_coint.csv', index=False)