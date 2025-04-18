import streamlit as st
import os
import matplotlib.pyplot as plt
import joblib
from login import login_ui, logout
from model_utils import get_data_from_alpha_vantage, train_and_return_model

st.set_page_config(page_title="SmartCapital.ai Dashboard", layout="wide")

# Authentication
authenticated, user_email = login_ui()
if not authenticated:
    st.stop()

# --- Sidebar Navigation ---
st.sidebar.image("https://i.imgur.com/1Q9Z1Zm.png", width=60)  # Optional: your logo
st.sidebar.markdown(
    "<h2 style='color:#2d7cff; font-family:Segoe UI,Arial,sans-serif;'>SmartCapital.ai</h2>",
    unsafe_allow_html=True
)
st.sidebar.markdown(f"**Welcome, {user_email} 👋**")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Go to",
    [
        "📈 Stock Market Prediction",
        "💰 Personal Finance (Coming Soon)",
        "🧾 ITR Calculator (Coming Soon)",
        "ℹ️ About Us"
    ]
)

st.markdown(
    """
    <style>
    .main-title {
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 2.2rem;
        font-weight: bold;
        color: #2d7cff;
        letter-spacing: 2px;
        margin-bottom: 0.2em;
    }
    .section-title {
        font-size: 1.3rem;
        color: #2d7cff;
        margin-top: 1.5em;
        margin-bottom: 0.7em;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Main Content ---
if menu == "📈 Stock Market Prediction":
    st.markdown('<div class="main-title">Stock Market Prediction</div>', unsafe_allow_html=True)
    st.markdown(
        "Use our ML-powered engine to forecast stock trends. Enter a stock symbol below to get started."
    )
    symbol = st.text_input("Enter Stock Symbol (e.g., AAPL for Apple):", "AAPL").upper()
    if st.button("Predict"):
        try:
            # Load or train model
            model_path = f"{symbol}_model.h5"
            scaler_path = f"{symbol}_scaler.pkl"
            if os.path.exists(model_path) and os.path.exists(scaler_path):
                from tensorflow.keras.models import load_model
                model = load_model(model_path)
                scaler = joblib.load(scaler_path)
            else:
                df = get_data_from_alpha_vantage(symbol)
                model, scaler = train_and_return_model(df)
                model.save(model_path)
                joblib.dump(scaler, scaler_path)

            # Get recent data for prediction
            df = get_data_from_alpha_vantage(symbol)
            recent_data = df[['Open', 'High', 'Low', 'Close', 'Volume']].tail(60)
            scaled_data = scaler.transform(recent_data)
            X = scaled_data.reshape(1, 60, 5)
            prediction = model.predict(X)[0][0]

            st.success(f"Prediction for {symbol}: **{'Up' if prediction > 0.5 else 'Down'}** (Confidence: {prediction:.2f})")

            # Plot closing prices
            st.markdown('<div class="section-title">Recent Closing Prices</div>', unsafe_allow_html=True)
            fig, ax = plt.subplots()
            df['Close'].tail(100).plot(ax=ax, title=f"{symbol} Closing Prices")
            ax.set_xlabel("Date")
            ax.set_ylabel("Price (USD)")
            st.pyplot(fig)

        except Exception as e:
            st.error(f"Error: {str(e)}")

elif menu == "💰 Personal Finance (Coming Soon)":
    st.markdown('<div class="main-title">Personal Finance</div>', unsafe_allow_html=True)
    st.info("Personal finance tools are coming soon! You'll be able to track expenses, set budgets, and get personalized insights.")

elif menu == "🧾 ITR Calculator (Coming Soon)":
    st.markdown('<div class="main-title">ITR Calculator</div>', unsafe_allow_html=True)
    st.info("Our ITR (Income Tax Return) calculator and filing assistant will be available soon!")

elif menu == "ℹ️ About Us":
    st.markdown('<div class="main-title">About Us</div>', unsafe_allow_html=True)
    st.markdown("""
    Welcome to **SmartCapital.ai**!  
    We are your all-in-one platform for:
    - Stock market analysis and prediction using advanced machine learning
    - Personal finance management tools
    - ITR (Income Tax Return) calculator
    - Career opportunities in the world of finance and technology

    Our mission is to empower you with data-driven insights and tools for smarter financial decisions.
    """)

# --- Logout Button ---
st.sidebar.markdown("---")
if st.sidebar.button("Logout"):
    logout()
    st.experimental_rerun()
