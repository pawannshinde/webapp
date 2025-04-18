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

    # Enhanced CSS with modern styling
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        * {
            font-family: 'Inter', sans-serif;
        }
        
        .main-container {
            max-width: 480px;
            margin: 0 auto;
            padding: 2rem 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 24px rgba(0,0,0,0.08);
            background: white;
            position: relative;
            top: 50%;
            transform: translateY(10%);
        }
        
        .brand-header {
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .logo {
            width: 64px;
            height: 64px;
            background: linear-gradient(135deg, #4361ee 0%, #3a0ca3 100%);
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 1rem;
            box-shadow: 0 4px 12px rgba(67, 97, 238, 0.2);
        }
        
        .logo-text {
            color: white;
            font-size: 24px;
            font-weight: 700;
            letter-spacing: 1px;
        }
        
        .app-name {
            font-size: 28px;
            font-weight: 700;
            color: #2b2d42;
            margin-bottom: 0.5rem;
            background: linear-gradient(135deg, #4361ee 0%, #3a0ca3 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .app-tagline {
            font-size: 14px;
            color: #6c757d;
            margin-bottom: 2rem;
            line-height: 1.5;
        }
        
        .stTextInput>div>div>input {
            padding: 12px 16px !important;
            border-radius: 8px !important;
            border: 1px solid #dee2e6 !important;
        }
        
        .stTextInput>div>div>input:focus {
            border-color: #4361ee !important;
            box-shadow: 0 0 0 2px rgba(67, 97, 238, 0.2) !important;
        }
        
        .stButton>button {
            width: 100%;
            padding: 12px !important;
            border-radius: 8px !important;
            background: linear-gradient(135deg, #4361ee 0%, #3a0ca3 100%) !important;
            border: none !important;
            font-weight: 500 !important;
            transition: all 0.2s ease !important;
        }
        
        .stButton>button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(67, 97, 238, 0.3) !important;
        }
        
        .stButton>button:active {
            transform: translateY(0) !important;
        }
        
        .tab-container {
            margin-bottom: 1.5rem;
        }
        
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            flex: 1;
            padding: 0.5rem;
            border-radius: 8px;
            background: #f8f9fa !important;
            transition: all 0.2s ease;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #4361ee 0%, #3a0ca3 100%) !important;
            color: white !important;
        }
        
        .footer {
            text-align: center;
            margin-top: 2rem;
            font-size: 12px;
            color: #6c757d;
        }
        
        .footer a {
            color: #4361ee;
            text-decoration: none;
            font-weight: 500;
        }
        </style>
    """, unsafe_allow_html=True)

    # Main container
    st.markdown("""
        <div class="main-container">
            <div class="brand-header">
                <div class="logo">
                    <div class="logo-text">SC</div>
                </div>
                <div class="app-name">SmartCapital</div>
                <div class="app-tagline">
                    AI-powered stock analysis and personal finance tools.<br>
                    Make smarter investment decisions with data-driven insights.
                </div>
            </div>
    """, unsafe_allow_html=True)

    # Tabs for Login/Signup
    tab1, tab2 = st.tabs(["Login", "Create Account"])

    with tab1:
        login_email = st.text_input("Email", key="login_email_input")
        login_password = st.text_input("Password", type="password", key="login_password_input")
        if st.button("Sign In", key="login_button"):
            if login_email and login_password:
                if login(login_email, login_password):
                    st.success("Logged in successfully!")
                    st.experimental_rerun()
            else:
                st.warning("Please enter both email and password.")

    with tab2:
        signup_email = st.text_input("Email", key="signup_email_input")
        signup_password = st.text_input("Password", type="password", key="signup_password_input")
        if st.button("Create Account", key="signup_button"):
            if signup_email and signup_password:
                if signup(signup_email, signup_password):
                    st.success("Account created! Please log in.")
            else:
                st.warning("Please enter both email and password.")

    st.markdown("""
            <div class="footer">
                By continuing, you agree to our <a href="#">Terms</a> and <a href="#">Privacy Policy</a>
            </div>
        </div>
    """, unsafe_allow_html=True)

    return st.session_state.get("authenticated", False), st.session_state.get("user_email", "")
