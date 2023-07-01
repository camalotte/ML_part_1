import pandas as pd
import matplotlib.pyplot as plt


def calculate_stats(input_file, output_file):
    # Load the data
    data = pd.read_csv(input_file)

    # Drop timestamp column
    data = data.drop(columns=['Timestamp'])

    # Calculate descriptive statistics
    stats = data.describe()

    # Loop through each column
    for column in data.columns:
        # Plot a histogram of the column's values
        plt.hist(data[column], bins=20)
        plt.title(f'Distribution of {column}')
        plt.xlabel(column)
        plt.ylabel('Frequency')
        plt.show()

    # Round all columns to 3 decimal places, ROC to 4
    stats = stats.round({
        'open': 3,
        'high': 3,
        'low': 3,
        'close': 3,
        'volume': 3,
        'VWMA': 3,
        'ma_pdif': 3,
        'abs_pdif': 3,
        'RSI': 3,
        'MACD': 3,
        'Signal': 3,
        'MA20': 3,
        '20dSTD': 3,
        'UpperBand': 3,
        'LowerBand': 3,
        'Momentum': 3,
        'ROC': 4
    })

    # Save stats to CSV
    stats.to_csv(output_file)


calculate_stats('./train_test_data/5S_train.csv', './statistics/5S_stats.csv')
