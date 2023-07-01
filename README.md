# ML_data_prep
A well sequenced tutorial how to prepare data for machine learning, using realtime tick data on a stock. Replace the raw data as required.

Notes: main.py is old, ignore it. 

1. The first step aggregates realtime tick data to desired timeframes, creating o,h,l,c,v. Logic is designed in a function to allow easy outputs of different time. Keep in mind the tick data is only a few hours long so there will only be enough data for very short tiem frames.
2. The second step engineers features that may be useful in later machine learning models. Features (columns) can be dropped in the ML codebase to not interfere with the sequence here.
3. The third step splits the dataframe into training and testing at an early stage to ensure isolation and enabling normalisaion on just the training data.
4. An extra script that applied statistsic calculations on the training data to analyse each columns distribution. This can help apply the correct scaler to each feature. This is more of a consulting script, but should be used. 
5. The fourth script applied normalisaion to the columns as preperation for machine learning. Different models may call for different normalisations. For decision tree models, no normalisation may be required. A varient without normalisaion will be added.

Improvements coming.
