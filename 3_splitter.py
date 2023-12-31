# Description: Splits the data into training and testing sets

import pandas as pd
from sklearn.model_selection import train_test_split

data = pd.read_csv('./engineered_data/5S_eng.csv')

# Split your data into training and testing sets
train, test = train_test_split(data, test_size=0.3, shuffle=False)

# Save to csv to train_test_data folder
train.to_csv('./train_test_data/5S_train.csv', index=False)
test.to_csv('./train_test_data/5S_test.csv', index=False)

print('Data split into training and testing sets and files saved to train_test_data folder.')
print('Consider: Run xtra_statistics.py')
print('Next: Run 4_normaliser.py')
