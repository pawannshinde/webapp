import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth
import os

# Initialize Firebase Admin SDK only once
if not firebase_admin._apps:
    cred = credentials.Certificate("smartcapital-5d4ee-firebase-adminsdk-fbsvc-a46f6ce0c0.json")  # Make sure this path is correct
    firebase_admin.initialize_app(cred)

def signup(email, password):
    try:
        user = auth.create_user(email=email, password=password)
        return f"✅ Account created for {email}"
    except Exception as e:
        return f"❌ {e}"

def login_ui():
    # Branding and app intro
    st.markdown("""
        <div style='text-align: center; padding: 1rem 0'>
            <h1 style='color:#4CAF50;'>SmartCapital</h1>
            <p style='font-size:16px;'>
                <em>We analyze and predict stocks using Machine Learning.</em><br>
                Personal finance tools, ITR calculator & more — powered by Quants.
            </p>
        </div>
    """, unsafe_allow_html=True)

    menu = st.radio("Choose an option", ["Login", "Sign Up"], horizontal=True)

    email = st.text_input("📧 Email", key="email_input")
    password = st.text_input("🔒 Password", type="password", key="pass_input")

    if menu == "Sign Up":
        if st.button("Create Account"):
            if email and password:
                message = signup(email, password)
                if "✅" in message:
                    st.success(message)
                else:
                    st.error(message)
            else:
                st.warning("Please enter both email and password.")

    elif menu == "Login":
        st.warning("🔐 Login not implemented yet")
        st.info("Login feature with Firebase token verification is coming soon.")

    # No user session yet
    return None
