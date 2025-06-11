import streamlit as st
import datetime
import yfinance as yf
import pandas as pd

def run_personal_finance():
    st.markdown('<div class="main-title">💬 Smart Finance Assistant</div>', unsafe_allow_html=True)

    st.subheader("🤖 Choose Your Query")
    query_type = st.selectbox("What would you like to know?", [
        "📈 Stock Price & Stats",
        "💰 Investment Return Estimator",
        "📊 Compare 2 Stocks"
    ])

    if query_type == "📈 Stock Price & Stats":
        symbol = st.text_input("Enter Stock Ticker (e.g., INFY.BO, AAPL, TSLA)", value="INFY.BO")
        if st.button("Get Info"):
            try:
                stock = yf.Ticker(symbol)
                info = stock.info
                hist = stock.history(period="6mo")

                if hist.empty:
                    st.warning("⚠️ No data found. Try another ticker.")
                    return

                st.write(f"**Name**: {info.get('shortName', '-')}")
                st.write(f"**Market Cap**: ₹{info.get('marketCap', 'N/A')}")
                st.write(f"**Current Price**: ₹{info.get('currentPrice', 'N/A')}")
                st.line_chart(hist["Close"])

            except Exception as e:
                st.error(f"⚠️ Error: {str(e)}")

    elif query_type == "💰 Investment Return Estimator":
        symbol = st.text_input("Stock Ticker (e.g., RELIANCE.BO)", value="RELIANCE.BO")
        amount = st.number_input("Investment Amount (₹)", min_value=100.0)
        years = st.slider("Years Ago", 1, 10, 3)

        if st.button("Estimate Returns"):
            try:
                today = datetime.date.today()
                past = today.replace(year=today.year - years)
                data = yf.Ticker(symbol).history(start=past, end=today)

                if data.empty:
                    st.warning("⚠️ No data for this stock.")
                    return

                start_price = data["Close"].iloc[0]
                end_price = data["Close"].iloc[-1]
                growth = end_price / start_price
                final = amount * growth

                st.success(f"₹{amount:.2f} → ₹{final:.2f} in {years} years ({growth:.2f}x growth)")
                st.line_chart(data["Close"])

            except Exception as e:
                st.error(f"⚠️ Error: {str(e)}")

    elif query_type == "📊 Compare 2 Stocks":
        stock1 = st.text_input("First Ticker", value="RELIANCE.BO")
        stock2 = st.text_input("Second Ticker", value="TCS.BO")
        period = st.selectbox("Comparison Period", ["3mo", "6mo", "1y"], index=1)

        if st.button("Compare"):
            try:
                df1 = yf.Ticker(stock1).history(period=period)["Close"]
                df2 = yf.Ticker(stock2).history(period=period)["Close"]
                df = pd.DataFrame({stock1: df1, stock2: df2})
                st.line_chart(df)
                st.caption(f"Comparison for {period.upper()}")
            except Exception as e:
                st.error(f"⚠️ Error: {str(e)}")

    st.markdown("---")
    st.caption("Simple Finance Bot - powered by yfinance & Python only. No API keys needed.")
