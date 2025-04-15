import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth

# Initialize Firebase only once
if not firebase_admin._apps:
    cred = credentials.Certificate("smartcapital-5d4ee-firebase-adminsdk-fbsvc-a46f6ce0c0.json")
    firebase_admin.initialize_app(cred)

# Function to initialize session state
def initialize_session_state():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user_email" not in st.session_state:
        st.session_state.user_email = ""
    if "signup_email" not in st.session_state:
        st.session_state.signup_email = ""
    if "signup_pass" not in st.session_state:
        st.session_state.signup_pass = ""

def signup(email, password):
    try:
        user = auth.create_user(email=email, password=password)
        st.success("✅ Account created! Please log in.")
    except Exception as e:
        st.error(f"❌ {e}")

def login(email, password):
    # NOTE: Firebase Admin SDK doesn't support verifying passwords.
    # This is a placeholder that assumes login is successful
    st.session_state.authenticated = True
    st.session_state.user_email = email

    # Only rerun the script if the user is successfully authenticated
    if st.session_state.authenticated:
        st.experimental_rerun()

def logout():
    st.session_state.authenticated = False
    st.session_state.user_email = ""
    st.experimental_rerun()

def login_ui():
    # Ensure session state is initialized
    initialize_session_state()

    st.markdown("<h1 style='text-align: center;'>🔐 SmartCapital</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>We analyze and predict stocks using ML, assist with personal finance, and provide an ITR calculator. We are Quants 💼📊</p>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        email = st.text_input("📧 Email")
        password = st.text_input("🔑 Password", type="password")
        if st.button("Login"):
            login(email, password)

    with tab2:
        email = st.text_input("📧 Email", key="signup_email")
        password = st.text_input("🔑 Password", type="password", key="signup_pass")
        if st.button("Create Account"):
            signup(email, password)

    return st.session_state.authenticated, st.session_state.user_email
