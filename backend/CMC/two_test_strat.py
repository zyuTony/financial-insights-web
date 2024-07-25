import pandas as pd
import numpy as np  
 

def calculate_indicators(df, bb_window=20, bb_std=2, rsi_window=14):
    # Calculate Bollinger Bands
    bb = BollingerBands(df['Close'], window=bb_window, window_dev=bb_std)
    df['bb_high'] = bb.bollinger_hband()
    df['bb_low'] = bb.bollinger_lband()

    # Calculate RSI
    rsi = RSIIndicator(df['Close'], window=rsi_window)
    df['rsi'] = rsi.rsi()

    # Calculate custom formula
    df['formula'] = 20.5 * df['ETH-USD'] - 5155.77 - df['BTC-USD']

    return df

def backtest_strategy(df):
    position = 0  # 0: no position, 1: long, -1: short
    entry_price = 0
    trades = []

    for i in range(1, len(df)):
        if position == 0:
            # Check for long entry
            if df['rsi'].iloc[i] < 30 and df['Close'].iloc[i] <= df['bb_low'].iloc[i]:
                position = 1
                entry_price = df['Close'].iloc[i]
                trades.append(('Enter Long', df.index[i], entry_price))
            # Check for short entry
            elif df['rsi'].iloc[i] > 70 and df['Close'].iloc[i] >= df['bb_high'].iloc[i]:
                position = -1
                entry_price = df['Close'].iloc[i]
                trades.append(('Enter Short', df.index[i], entry_price))
        elif position == 1:
            # Check for long exit
            if df['Close'].iloc[i] <= entry_price * 0.95 or df['formula'].iloc[i] <= 0:
                position = 0
                exit_price = df['Close'].iloc[i]
                trades.append(('Exit Long', df.index[i], exit_price))
        elif position == -1:
            # Check for short exit
            if df['Close'].iloc[i] >= entry_price * 1.05 or df['formula'].iloc[i] <= 0:
                position = 0
                exit_price = df['Close'].iloc[i]
                trades.append(('Exit Short', df.index[i], exit_price))

    return trades

def calculate_returns(trades):
    total_return = 0
    for i in range(0, len(trades), 2):
        if i + 1 < len(trades):
            entry = trades[i][2]
            exit = trades[i+1][2]
            if trades[i][0] == 'Enter Long':
                trade_return = (exit - entry) / entry
            else:  # Short trade
                trade_return = (entry - exit) / entry
            total_return += trade_return
    return total_return

# Main execution
start_date = '2020-01-01'
end_date = '2023-12-31'

eth_data = fetch_data('ETH-USD', start_date, end_date)
btc_data = fetch_data('BTC-USD', start_date, end_date)

# Merge ETH and BTC data
df = eth_data.join(btc_data['Close'], rsuffix='_BTC')
df = df.rename(columns={'Close': 'ETH-USD', 'Close_BTC': 'BTC-USD'})
df['Close'] = df['ETH-USD'] / df['BTC-USD']  # ETH/BTC ratio

# Set custom parameters
bb_window = 20
bb_std = 2
rsi_window = 14

df = calculate_indicators(df, bb_window, bb_std, rsi_window)
trades = backtest_strategy(df)

# Print results
print(f"Total trades: {len(trades) // 2}")
print(f"Total return: {calculate_returns(trades):.2%}")
for trade in trades:
    print(f"{trade[0]} at {trade[1]} - Price: {trade[2]:.6f}")