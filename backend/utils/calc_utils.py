import pandas as pd
from statsmodels.tsa.stattools import coint
import os
import json
from statsmodels.tsa.stattools import coint
import config
from utils.calc_utils import *

def rolling_cointegration(name1, data1, name2, data2, window_length):
    
    if len(data1) < window_length or len(data1) != len(data2) :
        raise ValueError("The length of the time window is greater than the available df, OR data lengths differ.")
    
    rolling_coint_scores = []
    rolling_p_values = []

    for end in range(window_length, len(data1)):
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

def get_multi_pairs_rolling_coint(price_data, top_n_data, checkpoint_file, result_file):
    df = pd.read_csv(price_data)
    df['date'] = pd.to_datetime(df['date'])

    start_date_index = df.index[df['date'] >= config.ROLLING_COINT_START_DATE][0]
    adjusted_start_date_index = max(0, start_date_index - config.ROLLING_COINT_WINDOW)

    df = df.iloc[adjusted_start_date_index:]
    date = df['date'][config.ROLLING_COINT_WINDOW:].reset_index(drop=True)
    df = df.drop('date', axis=1)
    df = df.iloc[:,:top_n_data]

    # save progress of analyzed coin pairs
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'r') as file:
            checkpoint_data = json.load(file)
    else:
        checkpoint_data = []
    results = pd.DataFrame(date)
    # get rolling coint for all possible pairs
    for i in range(df.shape[1]):
        name1 = df.columns[i]
        data1 = df.iloc[:, i]
        print(f'--- {name1}')
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
                res = rolling_cointegration(name1, data1, name2, data2, config.ROLLING_COINT_WINDOW)
                results = pd.concat([results, res], axis=1)
                checkpoint_data.append([name1, name2])
            except Exception as e:
                print(f'Error processing {name1} X {name2}: {e}')
                continue
        try:
            # periodically save all results to csv and checkpoint file
            with open(checkpoint_file, 'w') as file:
                json.dump(checkpoint_data, file, indent=4)
            try:
                results.to_csv(result_file, index=False)
            except Exception as e:  
                print(f"Error: {e} but continue")    
        except Exception as e:
            print(f"Error: {e} but continue")
            continue

    # save final results to csv
    with open(checkpoint_file, 'w') as file:
                json.dump(checkpoint_data, file, indent=4)
    results.to_csv(result_file, index=False)