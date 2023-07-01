# step 1, resample the data to different timeframes.
# Alternatively you could request the data from the exchange at the desired timeframe but you may suffer redundancy by requesting the same data multiple times.

import os
import pandas as pd

# Load the data
data = pd.read_csv('raw_data/tick.csv')


def resample_data(file_name, resample_size):
    # Load the data
    data = pd.read_csv(file_name)

    # Convert the 'Time' column to datetime format
    data['Time'] = pd.to_datetime(data['Time'])

    # Set 'Time' as the index
    data.set_index('Time', inplace=True)

    # Resample the data
    resampled_data = data.resample(resample_size).agg({'Price': 'ohlc', 'Volume': 'sum'})

    # Flatten the column names
    resampled_data.columns = [' '.join(col).strip() for col in resampled_data.columns.values]

    # Create a new filename with the desired folder path
    base_name = os.path.basename(file_name).split(".")[0]  # get the base file name without extension
    new_file_name = f"resampled_data/{resample_size}.csv"

    # Check if directory exists, if not, create it
    if not os.path.exists('resampled_data'):
        os.makedirs('resampled_data')

    # Save to new csv
    resampled_data.to_csv(new_file_name)

    return resampled_data


resample_data('raw_data/tick.csv', '1S')
resample_data('raw_data/tick.csv', '5S')
resample_data('raw_data/tick.csv', '1T')
resample_data('raw_data/tick.csv', '5T')



# # Convert the 'Time' column to datetime format
# data['Time'] = pd.to_datetime(data['Time'])
#
# # Set 'Time' as the index
# data.set_index('Time', inplace=True)
#
# # Resample to 5 second bars
# resampled_data = data.resample('5S').agg({'Price': 'ohlc', 'Volume': 'sum'})
#
# # flatten the column names
# resampled_data.columns = [' '.join(col).strip() for col in resampled_data.columns.values]
#
# # Save to new csv
# resampled_data.to_csv('tick_5s.csv')
