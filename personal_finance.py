import streamlit as st
import datetime
from serpapi import GoogleSearch
import openai
import os

# --- GPT Setup (using Streamlit Cloud secrets) ---
openai.api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))

# --- SerpAPI Setup (using Streamlit Cloud secrets) ---
SERPAPI_KEY = st.secrets.get("SERPAPI_KEY", os.getenv("SERPAPI_KEY"))

def run_personal_finance():
    st.markdown('<div class="main-title">Personal Finance Tools</div>', unsafe_allow_html=True)

    # --- Investment Interest Estimator ---
    st.subheader("📈 Investment Return Estimator")
    stock_price = st.number_input("Stock Price at Purchase (₹)", min_value=1.0)
    current_price = st.number_input("Current Stock Price (₹)", min_value=1.0)
    shares = st.number_input("Number of Shares Bought", min_value=1)
    purchase_date = st.date_input("Purchase Date", max_value=datetime.date.today())

    if st.button("Calculate Returns"):
        investment = stock_price * shares
        current_value = current_price * shares
        profit = current_value - investment
        st.success(f"Investment Value: ₹{investment:.2f}")
        st.success(f"Current Value: ₹{current_value:.2f}")
        st.info(f"Total Profit/Loss: ₹{profit:.2f}")

    st.markdown("---")

    # --- AI Financial Chat Assistant ---
    st.subheader("🤖 Ask our AI Financial Assistant")
    user_query = st.text_input("Type your query (e.g., Best mutual funds under ₹5000)")
    if st.button("Ask Bot") and user_query:
        with st.spinner("Searching online..."):
            try:
                search = GoogleSearch({
                    "q": user_query,
                    "api_key": SERPAPI_KEY
                })
                results = search.get_dict()
                snippet = results.get("organic_results", [{}])[0].get("snippet", "No result found.")

                gpt_response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a financial assistant."},
                        {"role": "user", "content": f"{user_query} (hint: use context - {snippet})"}
                    ]
                )
                reply = gpt_response["choices"][0]["message"]["content"]
                st.success(reply)
            except Exception as e:
                st.error(f"Error: {str(e)}")
