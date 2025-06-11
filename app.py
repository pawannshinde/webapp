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

def fetch_stock_news(symbol):
    try:
        query = symbol.replace('.', '-')
        url = f"https://www.google.com/search?q={query}+stock+news"
        headers = {"User-Agent": "Mozilla/5.0"}
        page = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(page.text, "html.parser")

        news = []
        for div in soup.select('div.BVG0Nb')[:2]:
            title = div.get_text()
            source_tag = div.find_parent().find_next('div')
            source = source_tag.get_text() if source_tag else 'Unknown Source'
            news.append(f"• **{title}** ({source})")

        return news if news else ["No news found."]
    except Exception as e:
        return [f"News fetch error: {str(e)}"]

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

            prediction_result = "Up 📈" if prediction > 0.5 else "Down 📉"
            st.success(f"Prediction for {symbol}: **{prediction_result}** (Confidence: {prediction:.2f})")

            if not df.empty:
                st.markdown('<div class="section-title">Recent Closing Prices</div>', unsafe_allow_html=True)
                fig1 = go.Figure()
                fig1.add_trace(go.Scatter(x=df.index[-100:], y=df['Close'].tail(100), mode='lines', name='Close'))
                fig1.update_layout(title=f"{symbol} - Closing Prices", height=300)
                st.plotly_chart(fig1, use_container_width=True)

                # Plot predicted vs actual for last 10 days
                st.markdown('<div class="section-title">Actual vs Predicted (Last 10 Days)</div>', unsafe_allow_html=True)
                df_recent = df.tail(70).copy()
                scaled_recent = scaler.transform(df_recent[['Open', 'High', 'Low', 'Close', 'Volume']])
                X_all, y_all = [], []
                for i in range(60, len(scaled_recent)):
                    X_all.append(scaled_recent[i-60:i])
                    y_all.append(df_recent['Target'].iloc[i])

                X_all = np.array(X_all)
                y_all = np.array(y_all)
                preds = model.predict(X_all).flatten()
                df_plot = pd.DataFrame({
                    "Date": df_recent.index[60:],
                    "Actual": y_all,
                    "Predicted": preds
                })
                fig3 = go.Figure()
                fig3.add_trace(go.Scatter(x=df_plot['Date'], y=df_plot['Actual'], mode='lines+markers', name='Actual'))
                fig3.add_trace(go.Scatter(x=df_plot['Date'], y=df_plot['Predicted'], mode='lines+markers', name='Predicted'))
                fig3.update_layout(title="Model Prediction vs Actual (last 10 days)", height=300)
                st.plotly_chart(fig3, use_container_width=True)
            else:
                st.warning("No data available to plot.")

            st.markdown('<div class="section-title">Recent OHLCV Data</div>', unsafe_allow_html=True)
            st.dataframe(df.tail(10).style.format("{:.2f}"))

            st.markdown('<div class="section-title">Prediction Summary</div>', unsafe_allow_html=True)
            st.table(pd.DataFrame({
                "Symbol": [symbol],
                "Prediction": [prediction_result],
                "Confidence": [f"{prediction:.2f}"],
                "Date": [datetime.now().strftime("%Y-%m-%d %H:%M")]
            }))

            st.markdown('<div class="section-title">Recent News</div>', unsafe_allow_html=True)
            news_list = fetch_stock_news(symbol)
            for news in news_list:
                st.markdown(news)

        except Exception as e:
            st.error(f"Error: {str(e)}")

elif menu == "💰 Personal Finance":
    from personal_finance import run_personal_finance
    run_personal_finance()


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
