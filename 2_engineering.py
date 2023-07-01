# This file engineers technical features and outputs a new csv file to the engineered_data folder
# Features can be later droped at the ML stage if they are not useful

import pandas as pd
import os


# this file engineers features such as RSI and outputs a new csv file to the engineered_data folder
def calculate_features(input_file_path, output_folder_path='engineered_data', index_col=None):
    # Check if output directory exists, if not, create it
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    # Load the data
    data = pd.read_csv(input_file_path, index_col=index_col)

    # Rename column names
    new_names = {
        'Time': 'Timestamp',
        'Price open': 'open',
        'Price high': 'high',
        'Price low': 'low',
        'Price close': 'close',
        'Volume Volume': 'volume'
    }
    data = data.rename(columns=new_names)

    # Volume-weighted 21 period moving average
    data['VWMA'] = (data['close'] * data['volume']).rolling(window=21).sum() / data[
        'volume'].rolling(window=21).sum()
    data['VWMA'] = data['VWMA'].round(2)

    # Absolute price difference between the current price and the VWMA
    data['ma_pdif'] = abs(data['close'] - data['VWMA']).round(2)

    # Absolute price difference between the current price and the previous price
    data['abs_pdif'] = abs(data['close'] - data['close'].shift(1)).round(4)

    # append return column
    data['return'] = (data['close'].pct_change()) * 100

    # RSI
    delta = data['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    data['RSI'] = 100 - (100 / (1 + rs)).round(2)

    # MACD
    exp1 = data['close'].ewm(span=12, adjust=False).mean()
    exp2 = data['close'].ewm(span=26, adjust=False).mean()
    data['MACD'] = (exp1 - exp2).round(2)
    data['Signal'] = (data['MACD'].ewm(span=9, adjust=False).mean()).round(2)

    # Bollinger Bands
    data['MA20'] = data['close'].rolling(window=20).mean().round(2)
    data['20dSTD'] = (data['close'].rolling(window=20).std()).round(2)
    data['UpperBand'] = (data['MA20'] + (data['20dSTD'] * 2)).round(2)
    data['LowerBand'] = (data['MA20'] - (data['20dSTD'] * 2)).round(2)

    # Momentum
    data['Momentum'] = data['close'].diff(periods=10).round(4)

    # ROC
    data['ROC'] = data['close'].pct_change(periods=10).round(4)

    # Drop first 21 rows
    data = data.iloc[21:]

    # Construct output file path
    base_name = os.path.basename(input_file_path).split(".")[0]  # get the base file name without extension
    output_file_path = os.path.join(output_folder_path, f'{base_name}_eng.csv')

    # save to new csv
    data.to_csv(output_file_path, index=False)

    print(f"Data saved to {output_file_path}")

# enter the path to the csv file you want to engineer (from resampled_data folder)
calculate_features('./resampled_data/5S.csv')
