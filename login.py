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

    # CSS for brand
    st.markdown("""
        <style>
        .brand-title {
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 2.5rem;
            font-weight: bold;
            color: #2d7cff;
            letter-spacing: 2px;
            text-align: center;
            margin-bottom: 0.3em;
        }
        .subtitle {
            font-size: 1.15rem;
            color: #2d7cff;
            text-align: center;
            margin-bottom: 1.5em;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-weight: 500;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="brand-title">SmartCapital.ai</div>', unsafe_allow_html=True)
   
    # About Us section (expand/collapse)
    with st.expander("About Us"):
        st.markdown("""
        Welcome, new user!  
        **SmartCapital.ai** is your all-in-one platform for:
        - We analyze and predict stocks using machine learning algorithms
        - Get personalized stock recommendations based on your portfolio
        - We also use machine learnig to learn and automate from the excel sheets you upload.
        - Assist with personal finance
        - Provide an ITR calculator and filling assistance
        - Help you find career opportunities

        Our mission is to empower you with data-driven insights and tools for smarter financial decisions.
        """)

    # Tabs: Sign Up first, then Login
    tab2, tab1 = st.tabs(["Create Account", "Login"])

    with tab2:
        st.markdown("#### Welcome, new user! Create your account below:")
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
