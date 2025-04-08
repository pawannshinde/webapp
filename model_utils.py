import pandas as pd
import requests
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.model_selection import train_test_split

API_KEY = 'XPOBZSFA1A8EI8F9'

def get_data_from_alpha_vantage(symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=full&apikey={API_KEY}'
    response = requests.get(url)
    data = response.json()

    ts_data = data.get("Time Series (Daily)")
    if not ts_data:
        raise ValueError("Invalid response from Alpha Vantage API.")

    df = pd.DataFrame.from_dict(ts_data, orient='index').astype(float)
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()  # Full history, sorted

    df = df.rename(columns={
        "1. open": "Open",
        "2. high": "High",
        "3. low": "Low",
        "4. close": "Close",
        "5. volume": "Volume"
    })

    df["Tomorrow"] = df["Close"].shift(-1)
    df["Target"] = (df["Tomorrow"] > df["Close"]).astype(int)
    return df.dropna()

def create_sequences(X, y, time_step=60):
    X_seq, y_seq = [], []
    for i in range(time_step, len(X)):
        X_seq.append(X[i-time_step:i])
        y_seq.append(y[i])
    return np.array(X_seq), np.array(y_seq)

def train_and_return_model(df):
    features = ['Open', 'High', 'Low', 'Close', 'Volume']
    scaler = MinMaxScaler()
    scaled_features = scaler.fit_transform(df[features])

    X, y = create_sequences(scaled_features, df['Target'].values)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )

    model = Sequential()
    model.add(LSTM(64, return_sequences=True, input_shape=(X.shape[1], X.shape[2])))
    model.add(Dropout(0.3))
    model.add(LSTM(64, return_sequences=False))
    model.add(Dropout(0.3))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    model.fit(
        X_train, y_train,
        epochs=25,
        batch_size=32,
        validation_split=0.1,
        verbose=1
    )

    return model, scaler
