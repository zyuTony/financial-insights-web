import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose


# Convert the dictionary to a DataFrame
df = pd.read_csv('./BATS_IWM.csv')
# Convert time to a readable format if necessary
df['time'] = pd.to_datetime(df['time'], unit='s')

# Set time as index
df.set_index('time', inplace=True)

# Perform time series decomposition on the closing prices
decomposition = seasonal_decompose(df['close'], model='multiplicative', period=480)

# Accessing the components
trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid

# Combine the components into a single DataFrame
decomposed_df = pd.DataFrame({
    'Trend': trend,
    'Seasonality': seasonal,
    'Residual': residual
})

# Drop NaN values that result from the decomposition
decomposed_df.dropna(inplace=True)

# Save the decomposed components to a CSV file
decomposed_df.to_csv('decomposed_components.csv')

print("Decomposed components saved to 'decomposed_components.csv'")