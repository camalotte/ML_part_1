# Description: Normalise the data using MinMaxScaler, StandardScaler and RobustScaler based on statistical properties
# Or normalise the whole dataset using MinMaxScaler and save the scaler

import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler
import joblib

# Load the data
data = pd.read_csv('./train_test_data/5S_train.csv')

# initialise scaler
scaler_m = MinMaxScaler()
scaler_s = StandardScaler()
scaler_r = RobustScaler()

# Convert Timestamp column to datetime format
data['Timestamp'] = pd.to_datetime(data['Timestamp'])
# Convert Timestamp column to string format without hyphens and colons
data['Timestamp'] = data['Timestamp'].dt.strftime('%Y%m%d%H%M%S')

# scale open, high, low, close columns using MinMaxScaler as price data is not normally distributed
data[['open', 'high', 'low', 'close', 'return']] = scaler_m.fit_transform(data[['open', 'high', 'low', 'close', 'return']])

# scale volume column using RobustScaler as volume data is not normally distributed and has outliers
data['volume'] = scaler_r.fit_transform(data[['volume']])

# scale VWMA, ma_pdif, abs_pdif, MACD, Signal, MA20, 20dSTD, UpperBand, LowerBand, Momentum with StandardScaler
data[['VWMA', 'ma_pdif', 'abs_pdif', 'MACD', 'Signal', 'MA20', '20dSTD', 'UpperBand', 'LowerBand', 'Momentum']] = \
    scaler_s.fit_transform(data[['VWMA', 'ma_pdif', 'abs_pdif', 'MACD', 'Signal', 'MA20', '20dSTD', 'UpperBand',
                                 'LowerBand', 'Momentum']])

# no need to scale RSI and ROC as they are already in the range

data = data.round(4)

# save data to csv
data.to_csv('./normalised_data/5S_norm.csv', index=False)

print('Normalised data saved to normalised_data folder')


# Save the scalers
joblib.dump(scaler_m, './scalers/scaler_m.pkl')
joblib.dump(scaler_s, './scalers/scaler_s.pkl')
joblib.dump(scaler_r, './scalers/scaler_r.pkl')

# # Code to load the scalers when required
# scaler_m = joblib.load('./scalers/scaler_m.pkl')
# scaler_s = joblib.load('./scalers/scaler_s.pkl')
# scaler_r = joblib.load('./scalers/scaler_r.pkl')

# ///// OR /////
# Scale the entire dataset

# scaled_data = scaler_m.fit_transform(data)
#
# # Create a new DataFrame with scaled data
# scaled_df = pd.DataFrame(scaled_data, columns=data.columns)
# # round scaled_df to 4 decimal places
# scaled_df = scaled_df.round(2) # does not work
#
# # save to csv to normalised_data folder
# data.to_csv('./normalised_data/mm_5S_norm.csv', index=False)


# Save the scaler
# joblib.dump(scaler_m, './scalers/mm_scaler_m.pkl')

