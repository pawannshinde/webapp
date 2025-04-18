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

    # Custom CSS with modern gradient and animations
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        
        * {
            font-family: 'Poppins', sans-serif;
        }
        
        .main-container {
            max-width: 480px;
            margin: 2rem auto;
            padding: 2.5rem;
            border-radius: 16px;
            background: white;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
            position: relative;
            overflow: hidden;
        }
        
        .main-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 8px;
            background: linear-gradient(90deg, #4361ee, #3a0ca3, #7209b7);
        }
        
        .brand-header {
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .logo-container {
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 1rem;
        }
        
        .logo-circle {
            width: 70px;
            height: 70px;
            background: linear-gradient(135deg, #4361ee 0%, #3a0ca3 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 20px rgba(67, 97, 238, 0.3);
            margin-right: 12px;
        }
        
        .logo-text {
            color: white;
            font-size: 28px;
            font-weight: bold;
        }
        
        .brand-name {
            font-size: 28px;
            font-weight: 700;
            background: linear-gradient(90deg, #4361ee, #3a0ca3);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }
        
        .tagline {
            color: #6c757d;
            font-size: 14px;
            line-height: 1.6;
            margin-bottom: 0;
        }
        
        .highlight {
            color: #4361ee;
            font-weight: 500;
        }
        
        .stTabs [data-baseweb="tab-list"] {
            gap: 0;
        }
        
        .stTabs [data-baseweb="tab"] {
            flex: 1;
            padding: 0.75rem 1rem;
            background: #f8f9fa !important;
            border: none !important;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #4361ee 0%, #3a0ca3 100%) !important;
            color: white !important;
        }
        
        .stTabs [data-baseweb="tab"]:first-child {
            border-radius: 8px 0 0 8px !important;
        }
        
        .stTabs [data-baseweb="tab"]:last-child {
            border-radius: 0 8px 8px 0 !important;
        }
        
        .stTextInput>div>div>input {
            padding: 12px 16px !important;
            border-radius: 8px !important;
            border: 1px solid #e0e0e0 !important;
            transition: all 0.3s ease !important;
        }
        
        .stTextInput>div>div>input:focus {
            border-color: #4361ee !important;
            box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.15) !important;
        }
        
        .stButton>button {
            width: 100%;
            padding: 12px !important;
            border-radius: 8px !important;
            background: linear-gradient(135deg, #4361ee 0%, #3a0ca3 100%) !important;
            border: none !important;
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
            margin-top: 8px;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(67, 97, 238, 0.3) !important;
        }
        
        .career-section {
            text-align: center;
            margin-top: 2rem;
            padding-top: 1.5rem;
            border-top: 1px solid #f0f0f0;
        }
        
        .career-link {
            display: inline-flex;
            align-items: center;
            color: #4361ee !important;
            font-weight: 500;
            text-decoration: none;
            transition: all 0.3s ease;
        }
        
        .career-link:hover {
            color: #3a0ca3 !important;
            text-decoration: underline;
        }
        
        .career-link svg {
            margin-right: 6px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Main container
    st.markdown("""
        <div class="main-container">
            <div class="brand-header">
                <div class="logo-container">
                    <div class="logo-circle">
                        <div class="logo-text">SC</div>
                    </div>
                </div>
                <h1 class="brand-name">SmartCapital</h1>
                <p class="tagline">
                    AI-powered stock analysis and personal finance tools.<br>
                    Make smarter investment decisions with <span class="highlight">data-driven insights</span>.
                </p>
            </div>
    """, unsafe_allow_html=True)

    # Tabs - Sign Up first as requested
    tab1, tab2 = st.tabs(["Create Account", "Login"])

    with tab1:
        signup_email = st.text_input("📧 Email", key="signup_email_input")
        signup_password = st.text_input("🔑 Password", type="password", key="signup_password_input")
        if st.button("Get Started", key="signup_button"):
            if signup_email and signup_password:
                if signup(signup_email, signup_password):
                    st.success("Account created! Please log in.")
            else:
                st.warning("Please enter both email and password.")

    with tab2:
        login_email = st.text_input("📧 Email", key="login_email_input")
        login_password = st.text_input("🔑 Password", type="password", key="login_password_input")
        if st.button("Continue", key="login_button"):
            if login_email and login_password:
                if login(login_email, login_password):
                    st.success("Logged in successfully!")
                    st.experimental_rerun()
            else:
                st.warning("Please enter both email and password.")

    # Career opportunities section
    st.markdown("""
            <div class="career-section">
                <a href="https://your-careers-page.com" target="_blank" class="career-link">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M20 12H4M4 12L10 6M4 12L10 18" stroke="#4361ee" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    Explore career opportunities with us
                </a>
            </div>
        </div>
    """, unsafe_allow_html=True)

    return st.session_state.get("authenticated", False), st.session_state.get("user_email", "")
