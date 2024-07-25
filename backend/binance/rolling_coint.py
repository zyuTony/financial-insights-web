import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import coint

def rolling_cointegration(df, window_length):
    
    if len(df) < window_length:
        raise ValueError("The length of the time window is greater than the available df.")
    
    rolling_coint_scores = []
    rolling_p_values = []

    for end in range(window_length, len(df)):
        start = end - window_length
        
        coin1 = df.columns[1]
        coin2 = df.columns[2]
        series1 = df.iloc[start:end, 1]
        series2 = df.iloc[start:end, 2]
        
        score, p_value, _ = coint(series1, series2)
        
        rolling_coint_scores.append(score)
        rolling_p_values.append(p_value)
        print(f"working on index {start} to {end-1}")

    print(len(df.index[window_length:]), len(rolling_coint_scores))
    results = pd.DataFrame({
        'date': df.index[window_length:],
        'coint_score': rolling_coint_scores,
        'p_value': rolling_p_values
    }).set_index('date')
    
    return results


df = pd.read_csv('./btceth.csv')
df = df[:1450]
results = rolling_cointegration(df, 1400)

# Display the results
print(results)

# Save results to CSV if needed
results.to_csv('rolling_coint_results.csv')
