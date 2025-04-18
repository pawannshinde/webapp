import streamlit as st
import pyrebase
from firebase_config import firebase_config

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

def init_session_state():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if "user_email" not in st.session_state:
        st.session_state["user_email"] = ""
    if "id_token" not in st.session_state:
        st.session_state["id_token"] = ""
    if "login_email" not in st.session_state:
        st.session_state["login_email"] = ""
    if "login_password" not in st.session_state:
        st.session_state["login_password"] = ""

def signup(email, password):
    try:
        auth.create_user_with_email_and_password(email, password)
        st.success("✅ Account created! Please log in.")
        # Auto-fill login fields after signup
        st.session_state.login_email = email
        st.session_state.login_password = ""
        return True
    except Exception as e:
        st.error(f"❌ {str(e)}")
        return False

def login(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        st.session_state["authenticated"] = True
        st.session_state["user_email"] = email
        st.session_state["id_token"] = user['idToken']
        return True
    except Exception as e:
        st.error("❌ Invalid email or password")
        return False

def logout():
    st.session_state["authenticated"] = False
    st.session_state["user_email"] = ""
    st.session_state["id_token"] = ""
    st.session_state["login_email"] = ""
    st.session_state["login_password"] = ""

def login_ui():
    init_session_state()

    # Custom CSS for clean white & blue theme
    st.markdown("""
        <style>
        .main-title {
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 2.8rem;
            font-weight: bold;
            color: #2d7cff;
            letter-spacing: 2px;
            text-align: center;
            margin-bottom: 0.2em;
        }
        .subtitle {
            font-size: 1.1rem;
            color: #2d7cff;
            text-align: center;
            margin-bottom: 1.2em;
        }
        .brand-circle {
            width: 80px;
            height: 80px;
            background: #fff;
            border: 3px solid #2d7cff;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 1em auto;
            box-shadow: 0 4px 16px rgba(45,124,255,0.08);
        }
        .brand-circle span {
            color: #2d7cff;
            font-size: 2.5rem;
            font-weight: bold;
            font-family: 'Segoe UI', Arial, sans-serif;
            letter-spacing: 1px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="brand-circle"><span>SC</span></div>
        <div class="main-title">SmartCapital.ai</div>
        <div class="subtitle">
            We analyze and predict stocks using ML, assist with personal finance, and provide an ITR calculator.
        </div>
    """, unsafe_allow_html=True)

    # Tabs: Sign Up first, then Login
    tab2, tab1 = st.tabs(["Create Account", "Login"])

    with tab2:
        signup_email = st.text_input("📧 Email", key="signup_email_input")
        signup_password = st.text_input("🔑 Password", type="password", key="signup_password_input")
        if st.button("Create Account", key="signup_button"):
            if signup_email and signup_password:
                if signup(signup_email, signup_password):
                    st.success("Account created! Please log in.")
            else:
                st.warning("Please enter both email and password.")

    with tab1:
        login_email = st.text_input("📧 Email", key="login_email_input")
        login_password = st.text_input("🔑 Password", type="password", key="login_password_input")
        if st.button("Login", key="login_button"):
            if login_email and login_password:
                if login(login_email, login_password):
                    st.success("Logged in successfully!")
                    st.experimental_rerun()
            else:
                st.warning("Please enter both email and password.")

    return st.session_state.get("authenticated", False), st.session_state.get("user_email", "")
