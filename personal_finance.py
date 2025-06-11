import streamlit as st
import datetime
import requests
import yfinance as yf

# --- Attempt to load DeepSeek or fallback to OpenAI (modern) ---
generator = None
llm_mode = "none"

# Try DeepSeek
try:
    from transformers import pipeline
    generator = pipeline("text-generation", model="deepseek-ai/deepseek-llm-7b", device=0)
    llm_mode = "deepseek"
except Exception:
    # Try OpenAI (new API)
    try:
        import openai
        import os
        openai.api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))

        def openai_generate(prompt, max_tokens=250):
            chat = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a smart personal finance assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens
            )
            return chat.choices[0].message.content

        llm_mode = "openai"
    except Exception:
        def mock_response(prompt, max_tokens=250):
            return "(⚠️ No LLM available. Showing mock reply.)"
        llm_mode = "mock"

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
                if llm_mode == "deepseek":
                    ai_result = generator(prompt, max_length=150)[0]['generated_text']
                elif llm_mode == "openai":
                    ai_result = openai_generate(prompt)
                else:
                    ai_result = mock_response(prompt)

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
                prompt = f"You are a friendly and knowledgeable personal finance assistant. Answer the following: {user_query}"
                if llm_mode == "deepseek":
                    response = generator(prompt, max_length=250)[0]['generated_text']
                elif llm_mode == "openai":
                    response = openai_generate(prompt)
                else:
                    response = mock_response(prompt)
                st.success(response)
            except Exception as e:
                st.error(f"Bot error: {str(e)}")
