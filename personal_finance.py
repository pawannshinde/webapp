import streamlit as st
import datetime
import requests
import yfinance as yf
from transformers import pipeline

# Load DeepSeek model or fallback
try:
    generator = pipeline("text-generation", model="deepseek-ai/deepseek-llm-7b", device=0)
    llm_available = True
except Exception:
    llm_available = False
    def generator(prompt, max_length=100):
        return [{"generated_text": "(⚠️ LLM not available. Showing mock reply.)"}]

def run_personal_finance():
    st.markdown('<div class="main-title">Personal Finance Tools</div>', unsafe_allow_html=True)

    # --- Return Estimator ---
    st.subheader("📊 Mutual Fund / Stock Return Estimator")
    asset_name = st.text_input("Enter Stock Ticker (e.g., RELIANCE.BO, INFY.BO, AAPL)")
    invest_amount = st.number_input("Investment Amount (₹)", min_value=100.0)
    years_ago = st.slider("Years Ago", min_value=1, max_value=10, value=3)

    if st.button("Estimate Returns") and asset_name:
        with st.spinner("Calculating with real data..."):
            try:
                today = datetime.date.today()
                past_date = today.replace(year=today.year - years_ago)
                ticker = yf.Ticker(asset_name)
                hist = ticker.history(start=past_date, end=today)

                if hist.empty:
                    st.error("No data found. Try a valid stock ticker (e.g., RELIANCE.BO for BSE stocks)")
                    return

                start_price = hist["Close"].iloc[0]
                end_price = hist["Close"].iloc[-1]
                growth = end_price / start_price
                returns = invest_amount * growth

                st.success(f"If you had invested ₹{invest_amount:.2f} in {asset_name} {years_ago} years ago,\n\n👉 Today it would be worth ₹{returns:.2f} (Growth: {growth:.2f}x)")

                # AI Insight
                prompt = f"User invested ₹{invest_amount} in {asset_name} stock {years_ago} years ago. The value grew by {growth:.2f}x. Summarize insight in one helpful paragraph."
                ai_result = generator(prompt, max_length=150)[0]['generated_text']
                st.info(ai_result)

            except Exception as e:
                st.error(f"Calculation error: {str(e)}")

    st.markdown("---")

    # --- AI Financial Assistant Chatbot ---
    st.subheader("🤖 Ask Finance Assistant Bot")
    user_query = st.text_area("Ask me anything about stocks, mutual funds, investing, or personal finance")
    if st.button("Ask Bot") and user_query:
        with st.spinner("Thinking..."):
            try:
                chat_prompt = f"You are a friendly and knowledgeable personal finance assistant. Answer the following: {user_query}"
                response = generator(chat_prompt, max_length=250)[0]['generated_text']
                st.success(response)
            except Exception as e:
                st.error(f"Bot error: {str(e)}")
