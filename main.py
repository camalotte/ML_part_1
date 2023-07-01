import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf

# Load the data
data = pd.read_csv('raw_data/tick.csv')

# data['Time'] = pd.to_datetime(data['Time'])
# data['Time'] = data['Time'].astype('int64') // 10**9
# data['Time'] = data['Time'].astype('float64')

# Calculate 21 period moving average, assuming "Price" is the column you want to average
data['21_MA'] = (data['Price'].rolling(window=21).mean()).round(2)

# Calculate volume-weighted 21 period moving average
data['VWMA'] = (data['Price'] * data['Volume']).rolling(window=21).sum() / data['Volume'].rolling(window=21).sum()
data['VWMA'] = data['VWMA'].round(2)

# append the df with a return column
# data['return'] = data['Price'].pct_change()

# calculate the absolute price difference between the current price and the moving average
data['ma_pdif'] = abs(data['Price'] - data['21_MA']).round(2)

# calculate the absolute price difference between the current price and the previous rows price
data['abs_pdif'] = abs(data['Price'] - data['Price'].shift(1)).round(4)

# Calculate RSI
delta = data['Price'].diff()
gain = delta.where(delta > 0, 0)
loss = -delta.where(delta < 0, 0)
avg_gain = gain.rolling(window=14).mean()
avg_loss = loss.rolling(window=14).mean()
rs = avg_gain / avg_loss
data['RSI'] = 100 - (100 / (1 + rs)).round(2)

# # Calculate MACD
# exp1 = data['Price'].ewm(span=12, adjust=False).mean()
# exp2 = data['Price'].ewm(span=26, adjust=False).mean()
# data['MACD'] = exp1 - exp2
# data['Signal'] = (data['MACD'].ewm(span=9, adjust=False).mean())

# Calculate Bollinger Bands
data['MA20'] = data['Price'].rolling(window=20).mean().round(2)
data['20dSTD'] = (data['Price'].rolling(window=20).std()).round(2)
data['UpperBand'] = (data['MA20'] + (data['20dSTD'] * 2)).round(2)
data['LowerBand'] = (data['MA20'] - (data['20dSTD'] * 2)).round(2)

# Calculate momentum
data['Momentum'] = data['Price'].diff(periods=10).round(4)
# Calculate ROC
data['ROC'] = data['Price'].pct_change(periods=10).round(4)

# Drop first 21 rows
# data = data.drop(index=range(21))
data = data.iloc[21:]

# # resample to 5 second bars
# data = data.resample('5S').agg({'Price': 'ohlc', 'Volume': 'sum', '21_MA': 'last', 'VWMA': 'last', 'prc_ma_dif': 'last',
#                                 'abs_diff_prev': 'last', 'RSI': 'last', 'MA20': 'last', '20dSTD': 'last',
#                                 'UpperBand': 'last', 'LowerBand': 'last', 'Momentum': 'last', 'ROC': 'last'})

# Write the data with the new moving average column back to a CSV
data.to_csv('tick_features.csv', index=False)






# # Calculate descriptive statistics
# data.describe()
#
# # Calculate correlation matrix
# data.corr()

# Plot line chart
# plt.plot(data['Price'])
# plt.title('Price over time')
# plt.xlabel('Time')
# plt.ylabel('Price')
# plt.show()


# # Load the data
# data = pd.read_csv('tick_features.csv', index_col='Time', parse_dates=True)
#
# # Create the candlestick chart
# mpf.plot(data, type='candle', mav=(10, 20), volume=True)
#
# # print the row featuring the biggest abs_diff_prev
# print(data.loc[data['abs_diff_prev'].idxmax()])