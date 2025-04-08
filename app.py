import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from model_utils import get_data_from_alpha_vantage, train_and_return_model

st.set_page_config(page_title="📈 Stock LSTM Predictor", layout="centered")
st.title("📈 LSTM Stock Predictor using Alpha Vantage by Pawan shinde ")

# Let user select stock
stock_dict = {
    "Reliance": "RELIANCE.BSE",
    "SBI": "SBIN.BSE"
}

stock_name = st.selectbox("Choose a stock:", list(stock_dict.keys()))
symbol = stock_dict[stock_name]

# Fetch data & train model
@st.cache_data(show_spinner=True)
def get_data_and_model(symbol):
    df = get_data_from_alpha_vantage(symbol)
    model, scaler = train_and_return_model(df)
    return df, model, scaler

with st.spinner("Fetching data and training model..."):
    df, model, scaler = get_data_and_model(symbol)

# Show latest prices using matplotlib for better control
st.subheader("📊 Latest Close Prices (Last 100 days)")
fig, ax = plt.subplots()
ax.plot(df["Close"].tail(100).values, color='skyblue', linewidth=2)
ax.set_title(f"{stock_name} Closing Prices (Last 100 Days)", fontsize=12)
ax.set_ylabel("Price")
ax.set_xlabel("Days")
ax.grid(True)
st.pyplot(fig)

# Make prediction
features = ['Open', 'High', 'Low', 'Close', 'Volume']
scaled = scaler.transform(df[features])
last_seq = np.expand_dims(scaled[-60:], axis=0)
pred = model.predict(last_seq)[0][0]
direction = "📈 Up" if pred > 0.5 else "📉 Down/Flat"

# Show prediction
st.subheader("📅 Prediction for Tomorrow")
st.metric(label="Predicted Direction", value=direction, delta=f"{pred * 100:.2f}% confidence")

import pandas as pd
from sklearn.model_selection import train_test_split

# Create sequences
X, y = [], []
time_step = 60
scaled_features = scaler.transform(df[features])
for i in range(time_step, len(scaled_features)):
    X.append(scaled_features[i-time_step:i])
    y.append(df['Target'].values[i])
X = np.array(X)
y = np.array(y)

# Split again to get test data for display
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# Predict on test set
y_pred = (model.predict(X_test) > 0.5).astype(int)

# Prepare results_df
results_df = df.iloc[-len(y_test):].copy()
results_df = results_df[['Close']].copy()
results_df['Actual_Target'] = y_test
results_df['Predicted_Target'] = y_pred.flatten()
results_df['Actual_Direction'] = results_df['Actual_Target'].map({0: 'Down/Flat', 1: 'Up'})
results_df['Predicted_Direction'] = results_df['Predicted_Target'].map({0: 'Down/Flat', 1: 'Up'})

# Show table
st.subheader("📋 Actual vs Predicted Table")
st.dataframe(results_df.tail(10))
# --- Trend Detection Table ---
df['Prev_Close'] = df['Close'].shift(1)
df['Prev_Low'] = df['Low'].shift(1)
df['Prev_Volume'] = df['Volume'].shift(1)

conditions = [
    df['Close'] < df['Prev_Low'],
    (df['Close'] > df['Prev_Close']) & (df['Volume'] > df['Prev_Volume'])
]
choices = ['Downtrend', 'Uptrend']
df['Trend'] = np.select(conditions, choices, default='No Trend')

trend_table = df[['Close', 'Prev_Close', 'Prev_Low', 'Volume', 'Prev_Volume', 'Trend']].dropna()

# Display in Streamlit
st.subheader("📊 Trend Detection Table")
st.dataframe(trend_table.tail(10))


