import streamlit as st
import datetime
from serpapi import GoogleSearch
import openai
import os

# --- GPT Setup (Streamlit Cloud secrets or fallback to env) ---
from openai import OpenAI
client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY")))

# --- SerpAPI Setup ---
SERPAPI_KEY = st.secrets.get("SERPAPI_KEY", os.getenv("SERPAPI_KEY"))

def run_personal_finance():
    st.markdown('<div class="main-title">Personal Finance Tools</div>', unsafe_allow_html=True)

    # --- AI-powered Investment Insight Tool ---
    st.subheader("📊 Mutual Fund / Stock Return Estimator")

    asset_name = st.text_input("Enter Mutual Fund or Stock Name (e.g., RIL, Tata Digital India Fund)")
    invest_amount = st.number_input("Investment Amount (₹)", min_value=100.0)
    years_ago = st.slider("How many years ago?", min_value=1, max_value=10, value=3)

    if st.button("Estimate Returns") and asset_name:
        with st.spinner("Calculating returns..."):
            try:
                # Use SerpAPI to simulate price discovery (mocked context for GPT)
                search = GoogleSearch({"q": f"{asset_name} price {years_ago} years ago", "api_key": SERPAPI_KEY})
                results = search.get_dict()
                snippet = results.get("organic_results", [{}])[0].get("snippet", "No price data found.")

                # Ask GPT to simulate return estimation from historical data context
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a financial assistant who estimates returns based on asset performance."},
                        {"role": "user", "content": f"If I had invested ₹{invest_amount} in {asset_name} {years_ago} years ago, how much would it be worth now? Context: {snippet}"}
                    ]
                )
                reply = response.choices[0].message.content
                st.success(reply)
            except Exception as e:
                st.error(f"Error fetching data or AI response: {str(e)}")

    st.markdown("---")

    # --- AI Financial Query Bot ---
    st.subheader("🤖 Ask our AI Financial Assistant")
    user_query = st.text_input("Type your query (e.g., Top ELSS mutual funds 2024)")
    if st.button("Ask Bot") and user_query:
        with st.spinner("Searching online..."):
            try:
                search = GoogleSearch({"q": user_query, "api_key": SERPAPI_KEY})
                results = search.get_dict()
                snippet = results.get("organic_results", [{}])[0].get("snippet", "No result found.")

                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful financial assistant."},
                        {"role": "user", "content": f"{user_query}. Use this context: {snippet}"}
                    ]
                )
                reply = response.choices[0].message.content
                st.success(reply)
            except Exception as e:
                st.error(f"Error during AI response: {str(e)}")
