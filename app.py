import streamlit as st
import os
import joblib
import pandas as pd
import numpy as np
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import plotly.graph_objects as go
from login import login_ui, logout
from model_utils import get_data_from_alpha_vantage, train_and_return_model
from tensorflow.keras.models import load_model

# Stock name-to-symbol dictionary
STOCKS = {
    "Reliance Industries": "RELIANCE.BSE",
    "Tata Consultancy Services": "TCS.BSE",
    "Infosys": "INFY.BSE",
    "State Bank of India": "SBIN.BSE",
    "HDFC Bank": "HDFCBANK.BSE",
    "Apple": "AAPL",
    "Google": "GOOGL",
    "Amazon": "AMZN"
}

st.set_page_config(page_title="SmartCapital.ai Dashboard", layout="wide")

authenticated, user_email = login_ui()
if not authenticated:
    st.stop()

# Sidebar
st.sidebar.image("https://i.imgur.com/1Q9Z1Zm.png", width=60)
st.sidebar.markdown("<h2 style='color:#2d7cff;'>SmartCapital.ai</h2>", unsafe_allow_html=True)
st.sidebar.markdown(f"**Welcome, {user_email} 👋**")
st.sidebar.markdown("---")

menu = st.sidebar.radio("Go to", [
    "📈 Stock Market Prediction",
    "💰 Personal Finance (Coming Soon)",
    "🧾 ITR Calculator (Coming Soon)",
    "ℹ️ About Us"
])

# Style
st.markdown("""
    <style>
    .main-title {
        font-size: 2rem; font-weight: bold; color: #2d7cff;
    }
    .section-title {
        font-size: 1.3rem; color: #2d7cff; margin-top: 2em;
    }
    .table-scroll {
        overflow-x: auto;
    }
    </style>
""", unsafe_allow_html=True)

if menu == "📈 Stock Market Prediction":
    st.markdown('<div class="main-title">Stock Market Prediction</div>', unsafe_allow_html=True)
    stock_name = st.selectbox("Select a Stock", list(STOCKS.keys()))
    symbol = STOCKS[stock_name]

    if st.button("Predict"):
        try:
            model_path = f"{symbol}_model.h5"
            scaler_path = f"{symbol}_scaler.pkl"

            if os.path.exists(model_path) and os.path.exists(scaler_path):
                model = load_model(model_path)
                scaler = joblib.load(scaler_path)
            else:
                df = get_data_from_alpha_vantage(symbol)
                model, scaler = train_and_return_model(df)
                model.save(model_path)
                joblib.dump(scaler, scaler_path)

            df = get_data_from_alpha_vantage(symbol)
            recent_data = df[['Open', 'High', 'Low', 'Close', 'Volume']].tail(60)
            scaled_data = scaler.transform(recent_data)
            X = scaled_data.reshape(1, 60, 5)
            prediction = model.predict(X)[0][0]

            # --- Prediction Summary Table
            prediction_result = "Up 📈" if prediction > 0.5 else "Down 📉"
            st.success(f"Prediction for {symbol}: **{prediction_result}** (Confidence: {prediction:.2f})")

            # --- Graphs
            st.markdown('<div class="section-title">Recent Closing Prices</div>', unsafe_allow_html=True)
            fig1 = go.Figure()
            fig1.add_trace(go.Scatter(y=df['Close'].tail(100), mode='lines', name='Close'))
            fig1.update_layout(title=f"{symbol} - Closing Prices", height=300)
            st.plotly_chart(fig1, use_container_width=True)

            st.markdown('<div class="section-title">Candlestick Chart</div>', unsafe_allow_html=True)
            fig2 = go.Figure(data=[go.Candlestick(
                x=df.index[-60:], open=df['Open'].tail(60), high=df['High'].tail(60),
                low=df['Low'].tail(60), close=df['Close'].tail(60)
            )])
            fig2.update_layout(title=f"{symbol} - Last 60 Days", height=350)
            st.plotly_chart(fig2, use_container_width=True)

            # --- Tables
            st.markdown('<div class="section-title">Recent OHLCV Data</div>', unsafe_allow_html=True)
            st.dataframe(df.tail(10).style.format("{:.2f}"))

            st.markdown('<div class="section-title">Prediction Summary</div>', unsafe_allow_html=True)
            st.table(pd.DataFrame({
                "Symbol": [symbol],
                "Prediction": [prediction_result],
                "Confidence": [f"{prediction:.2f}"],
                "Date": [datetime.now().strftime("%Y-%m-%d %H:%M")]
            }))

            # --- News (No API)
            st.markdown('<div class="section-title">Recent News</div>', unsafe_allow_html=True)
            try:
                news_url = f"https://www.google.com/search?q={symbol}+stock+news&tbm=nws"
                headers = {"User-Agent": "Mozilla/5.0"}
                news_page = requests.get(news_url, headers=headers)
                soup = BeautifulSoup(news_page.text, 'html.parser')
                articles = soup.find_all('div', class_='BVG0Nb', limit=5)
                for a in articles:
                    title = a.find('div', class_='n0jPhd ynAwRc MBeuO nDgy9d').text
                    link = a.find('a')['href']
                    st.markdown(f"🔗 [{title}]({link})")
            except:
                st.info("News not available right now.")

        except Exception as e:
            st.error(f"Error: {str(e)}")

elif menu == "💰 Personal Finance (Coming Soon)":
    st.markdown('<div class="main-title">Personal Finance</div>', unsafe_allow_html=True)
    st.info("Coming soon! You'll be able to track expenses, set budgets, and more.")

elif menu == "🧾 ITR Calculator (Coming Soon)":
    st.markdown('<div class="main-title">ITR Calculator</div>', unsafe_allow_html=True)
    st.info("ITR tools will be available soon!")

elif menu == "ℹ️ About Us":
    st.markdown('<div class="main-title">About Us</div>', unsafe_allow_html=True)
    st.markdown("""
    Welcome to **SmartCapital.ai**  
    We offer:
    - 📊 Stock Predictions using ML
    - 💸 Finance Tools
    - 🧾 ITR Calculator
    """)

# Logout
st.sidebar.markdown("---")
if st.sidebar.button("Logout"):
    logout()
    st.experimental_rerun()
