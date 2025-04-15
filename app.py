import streamlit as st
from login import login_ui, logout
from model_utils import get_data_from_alpha_vantage, train_and_return_model
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="📈 SmartCapital - Stock Analysis", layout="wide")

# Check authentication
authenticated, user_email = login_ui()

# Only allow access after login
if not authenticated:
    st.stop()

# App content after login
st.success(f"Welcome, {user_email} 👋")

st.markdown("## 📊 SmartCapital Dashboard")
st.markdown("""
SmartCapital uses state-of-the-art machine learning models to:
- 🔍 Analyze and forecast stock market prices
- 💰 Help you manage your personal finances
- 🧾 Provide an easy-to-use ITR calculator

**Explore your stock predictions below!**
""")

# Stock prediction section
st.subheader("Stock Price Prediction")
symbol = st.text_input("Enter Stock Symbol (e.g., AAPL for Apple):", "AAPL").upper()
if st.button("Predict"):
    try:
        # Load or train model
        model_path = f"{symbol}_model.h5"
        scaler_path = f"{symbol}_scaler.pkl"
        if os.path.exists(model_path):
            from tensorflow.keras.models import load_model
            import joblib
            model = load_model(model_path)
            scaler = joblib.load(scaler_path)
        else:
            df = get_data_from_alpha_vantage(symbol)
            model, scaler = train_and_return_model(df)
            model.save(model_path)
            import joblib
            joblib.dump(scaler, scaler_path)

        # Get recent data for prediction
        df = get_data_from_alpha_vantage(symbol)
        recent_data = df[['Open', 'High', 'Low', 'Close', 'Volume']].tail(60)
        scaled_data = scaler.transform(recent_data)
        X = scaled_data.reshape(1, 60, 5)
        prediction = model.predict(X)[0][0]
        st.write(f"Prediction for {symbol}: {'Up' if prediction > 0.5 else 'Down'} (Confidence: {prediction:.2f})")

        # Plot closing prices
        fig, ax = plt.subplots()
        df['Close'].tail(100).plot(ax=ax, title=f"{symbol} Closing Prices")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price (USD)")
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Error: {e}")

# Logout button
if st.button("Logout"):
    logout()


