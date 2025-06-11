import streamlit as st
import datetime
import yfinance as yf
import os

# Try OpenAI GPT if available
try:
    import openai
    openai.api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))
    def generator(prompt, max_tokens=150):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a financial assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens
        )
        return response['choices'][0]['message']['content']
    llm_available = True
except Exception:
    llm_available = False
    def generator(prompt, max_tokens=150):
        return "(⚠️ LLM not available. Showing mock reply.)"

def run_personal_finance():
    st.markdown('<div class="main-title">Personal Finance Tools</div>', unsafe_allow_html=True)

    # --- Investment Return Estimator ---
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
                    st.error("❌ No data found. Try a valid stock ticker like RELIANCE.BO")
                    return

                start_price = hist["Close"].iloc[0]
                end_price = hist["Close"].iloc[-1]
                growth = end_price / start_price
                returns = invest_amount * growth

                st.success(f"💰 If you had invested ₹{invest_amount:.2f} in **{asset_name}** {years_ago} years ago,\n\n📈 Today it would be worth ₹{returns:.2f} (Growth: {growth:.2f}x)")

                prompt = f"A user invested ₹{invest_amount} in {asset_name} stock {years_ago} years ago. The value grew by {growth:.2f}x. Summarize in one useful finance insight."
                ai_result = generator(prompt)
                st.info(ai_result)

            except Exception as e:
                st.error(f"Calculation error: {str(e)}")

    st.markdown("---")

    # --- Chatbot Section ---
    st.subheader("🤖 Ask Our Finance Assistant Bot")
    user_query = st.text_area("Ask me anything about stocks, mutual funds, returns, taxes...")
    if st.button("Ask Bot") and user_query:
        with st.spinner("Thinking..."):
            try:
                chat_prompt = f"You are a smart and friendly financial assistant. Answer this question: {user_query}"
                response = generator(chat_prompt)
                st.success(response)
            except Exception as e:
                st.error(f"Bot error: {str(e)}")
