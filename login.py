import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth

def init_session_state():
    """Initialize all session state variables"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user_email" not in st.session_state:
        st.session_state.user_email = ""
    if "login_email" not in st.session_state:
        st.session_state.login_email = ""
    if "login_password" not in st.session_state:
        st.session_state.login_password = ""

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
# In a real app, verify password with Firebase Auth
# In a real app, verify password with Firebase Auth
# In a real app, verify password with Firebase Auth
# In a real app, verify password with Firebase Auth
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
    # Initialize session state
    init_session_state()
    
    st.markdown("<h1 style='text-align: center;'>🔐 SmartCapital</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>We analyze and predict stocks using ML, assist with personal finance, and provide an ITR calculator.</p>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tablogin_1:
login_email = st.text_input("📧 Email", key="login_emaillogin_")
login_password = st.text_input("🔑 Password", type="password", key="login_password")
        if st.button("Lo, key="login_button"gin", key="login_button"):
            if lologin_gin(login_emalogin_il, login_password):
                st.rerun()

    with tab2:
        signup_email = st.text_input("📧 Email", key="signup_email")
        signup_password = st.text_input("🔑 Password", type="password", key="signup_password")
        if st.but, key="signup_button"ton(if "Create Account", key="signup_button"):
if signup(signup_ema:
                st.rerun()il, signup_password):
                st.rerun()

    return st.session_state["authenticated"], st.session_state["user_email"]
