'''
With a input of window length and a df with columns of date and series of stock data, it returns a rolling window cointegration score and p-value for all possible data pairs, each as one column.

return: pd.DataFrame; CSV file
'''
import os
import json
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import coint
import statsmodels.api as sm
from openpyxl.styles import Font

'''
Use criteria to select the most important cointegrated pairs
    1. must have continuous 30 days rolling coint period in last 360 days
    2. must have 20% coint history
Use the last 360 days of data 
'''
 
def min_cont_coint_check(df, x, threshold=0.05): 
    result = []
    for col in df.columns[1:]:
        series = df[col] <= threshold
        if any(series.rolling(window=x).sum() == x):
            result.append(col)
    return result

 
def min_coint_pct_check(df, pct_coint, pval=0.05):
    cols = []
    counts = []
    for col in df.columns[1:]:
          counts.append({col:int((df[col] <= pval).sum())})
          if int((df[col] <= pval).sum()) > pct_coint*len(df):
              cols.append(col)
          
    return cols, counts
 
df = pd.read_csv('../data/final_coint_stock_data_top_100.csv')
df = df.iloc[-180:] # use last -- days of rollling coint
x = 30 # at least -- days of continuous significant period
min_pct = 0.2   # at least -- % of significant rolling cointegration

min_length_coint_cols = min_cont_coint_check(df, x)
min_pct_coint_cols, min_pct_coint_counts = min_coint_pct_check(df, min_pct)
selected_cols = list(set(min_length_coint_cols) & set(min_pct_coint_cols))

print(f"Columns with continuous data < 0.05 for length {x}:")
print(min_length_coint_cols)
print("\nColumns with > 10 pct coint data in each column:")
print(min_pct_coint_cols)

# write to xlsx
df = pd.read_csv('../data/final_coint_stock_data_top_100.csv')
df[['date', *selected_cols]].to_excel('../data/high_coint_pairs_v2.xlsx', index=False)

'''
get OLS COEFF for selected important cointegrated pair - last 120 days data
'''
# return regression coefficient
def get_ols_coeff_from_csv(name1, name2, series1, series2):
    ols_result = sm.OLS(series1, sm.add_constant(series2)).fit()
    score, p_value, _ = coint(series1, series2)
    print(f'Finished cointegration test for {name1} and {name2}')
    return {
        'name1': name1, 
        'name2': name2,
        'Score': score, # Engle test score. 
        'P-Value': p_value, # p value of regression residual
        'OLS-constant': ols_result.params.iloc[0],  # Intercept
        'OLS-coeff': ols_result.params.iloc[1],  # coeff
        'R-squared': ols_result.rsquared,  # R-squared
        'Adjusted-R-squared': ols_result.rsquared_adj  # Adjusted R-squared
    }

df = pd.read_csv("../data/stock_agg_data.csv")
df = df.iloc[-270:] # use last 120 days to get coeff
df = df.drop('date', axis=1)
result = []
for pair in selected_cols:
    split_string = pair.split('_')
    name1 = split_string[0]
    name2 = split_string[1]
    series1 = df.loc[:, name1]
    series2 = df.loc[:, name2]
    result.append(get_ols_coeff_from_csv(name1, name2, series1, series2))

# write to xlsx
result = pd.DataFrame(result)
result.to_excel('../data/ols_coeff_for_key_pairs.xlsx', index=False)
 