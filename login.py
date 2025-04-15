import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth

# Initialize Firebase only once
if not firebase_admin._apps:
    cred = credentials.Certificate("smartcapital-5d4ee-firebase-adminsdk-fbsvc-a46f6ce0c0.json")
    firebase_admin.initialize_app(cred)

# Initialize session state variables at the top level
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "user_email" not in st.session_state:
    st.session_state["user_email"] = ""
if "signup_email" not in st.session_state:
    st.session_state["signup_email"] = ""
if "signup_pass" not in st.session_state:
    st.session_state["signup_pass"] = ""

def signup(email, password):
    try:
        user = auth.create_user(email=email, password=password)
        st.success("✅ Account created! Please log in.")
        return True
    except Exception as e:
        st.error(f"❌ {str(e)}")
        return False

def login(email, password):
    try:
        # In a real app, verify password with Firebase Auth
        st.session_state["authenticated"] = True
        st.session_state["user_email"] = email
        return True
    except Exception as e:
        st.error(f"❌ {str(e)}")
        return False

def logout():
    st.session_state["authenticated"] = False
    st.session_state["user_email"] = ""

def login_ui():
    st.markdown("<h1 style='text-align: center;'>🔐 SmartCapital</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>We analyze and predict stocks using ML, assist with personal finance, and provide an ITR calculator.</p>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        login_email = st.text_input("📧 Email", key="login_email")
        login_password = st.text_input("🔑 Password", type="password", key="login_password")
        if st.button("Login", key="login_button"):
            if login(login_email, login_password):
                st.rerun()

    with tab2:
        signup_email = st.text_input("📧 Email", key="signup_email")
        signup_password = st.text_input("🔑 Password", type="password", key="signup_password")
        if st.button("Create Account", key="signup_button"):
            if signup(signup_email, signup_password):
                st.rerun()

    return st.session_state["authenticated"], st.session_state["user_email"]
