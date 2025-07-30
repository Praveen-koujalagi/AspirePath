import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
from core import assess_skills, select_goal, generate_roadmap, predict_career
from helpers import parse_resume, fetch_youtube_resources, store_quiz_results, validate_email, validate_password, validate_name  # Added validation functions
from project_suggester import suggest_projects
from quiz_engine import load_questions, run_quiz, fetch_questions_from_api
from pymongo import MongoClient
import hashlib
import requests
import json

# Initialize user_skills as an empty list
user_skills = []

# Function to load Lottie animations
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Function to cache resources for better performance
@st.cache_resource
def load_css_animations():
    return """
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
        100% { transform: translateY(0px); }
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .floating-card {
        animation: float 6s ease-in-out infinite;
    }
    
    .fade-in-up {
        animation: fadeInUp 0.8s ease-out;
    }
    """

st.set_page_config(
    page_title="AspirePath - Your Career Journey Starts Here",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["aspirepath"]
users_collection = db["users"]

# Enhanced styling for a professional and sophisticated UI
st.markdown(
    """
    <style>
    /* Hide Streamlit header and menu */
    header[data-testid="stHeader"] {
        height: 0;
        display: none;
    }
    
    /* Remove top padding */
    .block-container {
        padding-top: 0rem !important;
    }
    
    /* Professional main background with subtle pattern */
    .main {
        background: 
            radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(120, 119, 198, 0.15) 0%, transparent 50%),
            linear-gradient(135deg, #667eea 0%, #764ba2 50%, #6B73FF 100%);
        background-attachment: fixed;
        background-size: 100% 100%, 100% 100%, 100% 100%, 100% 100%;
        min-height: 100vh;
        position: relative;
    }
    
    /* Add subtle animated background overlay */
    .main::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.02) 50%, transparent 70%),
            linear-gradient(-45deg, transparent 30%, rgba(255,255,255,0.01) 50%, transparent 70%);
        background-size: 60px 60px, 60px 60px;
        animation: backgroundMove 20s linear infinite;
        pointer-events: none;
        z-index: -1;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
    }
    
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
        100% { transform: translateY(0px); }
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes bounceIn {
        0% { opacity: 0; transform: scale(0.3); }
        50% { opacity: 1; transform: scale(1.1); }
        100% { opacity: 1; transform: scale(1); }
    }
    
    .floating-card {
        animation: float 6s ease-in-out infinite;
    }
    
    .fade-in-up {
        animation: fadeInUp 0.8s ease-out;
    }
    
    .slide-in-left {
        animation: slideInLeft 0.6s ease-out;
    }
    
    .bounce-in {
        animation: bounceIn 0.8s ease-out;
    }
    
    /* Enhanced loading spinner */
    .loading-spinner {
        width: 40px;
        height: 40px;
        border: 4px solid rgba(255,255,255,0.3);
        border-left: 4px solid #667eea;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 20px auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Professional header with glass effect */
    .custom-header {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 1.5rem 2rem;
        margin: -1rem -1rem 2rem -1rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        position: relative;
    }
    
    .header-content {
        display: flex;
        align-items: center;
        justify-content: center;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .logo-section {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .logo-icon {
        font-size: 2.8rem;
        background: linear-gradient(45deg, #ffd700, #ffed4e, #fff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.3));
        animation: logoGlow 3s ease-in-out infinite alternate;
    }
    
    @keyframes logoGlow {
        0% { filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.3)); }
        100% { filter: drop-shadow(2px 2px 8px rgba(255,215,0,0.4)); }
    }
    
    .logo-text {
        font-size: 2.2rem;
        font-weight: 700;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .tagline {
        font-size: 0.95rem;
        color: rgba(255, 255, 255, 0.9);
        font-style: italic;
        margin: 0;
        font-weight: 300;
        letter-spacing: 0.5px;
    }
    
    /* Enhanced sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .css-1v0mbdj {
        color: white !important;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: rgba(255, 255, 255, 0.15);
        border-radius: 15px;
        padding: 15px;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 12px 24px;
        color: white !important;
        border: 2px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
        font-weight: 600;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
    }
    
    .stTabs [aria-selected="true"] {
        background: rgba(255, 255, 255, 0.25) !important;
        border: 2px solid rgba(255, 255, 255, 0.5) !important;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        color: white !important;
    }
    
    /* Enhanced container styling with glassmorphism */
    .auth-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        padding: 3rem;
        border-radius: 25px;
        box-shadow: 
            0 25px 50px rgba(0, 0, 0, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        margin: 2rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .auth-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
    }
    
    /* Professional card styling */
    .feature-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(15px);
        padding: 2.5rem;
        border-radius: 20px;
        text-align: center;
        height: 300px;
        box-shadow: 
            0 15px 35px rgba(0, 0, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, #ffd700, #ffed4e, #ffd700);
    }
    
    .feature-card:hover {
        transform: translateY(-10px);
        box-shadow: 
            0 25px 45px rgba(0, 0, 0, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
    }
    
    /* Improved text visibility */
    .auth-container h1,
    .auth-container h2,
    .auth-container h3 {
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
    }
    
    .auth-container p {
        color: rgba(255, 255, 255, 0.9) !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
    }
    
    /* Form styling */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.95) !important;
        border: 2px solid rgba(102, 126, 234, 0.3) !important;
        border-radius: 12px !important;
        padding: 0.75rem !important;
        transition: all 0.3s ease !important;
        color: #333 !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2) !important;
        background: white !important;
    }
    
    .stTextInput label {
        color: white !important;
        font-weight: 600 !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 30px rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, #5a6fd8, #6a42a0);
    }
    
    /* Validation feedback styling */
    .validation-text {
        font-size: 0.8rem;
        margin-top: 0.25rem;
        font-weight: 600;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
    }
    
    .valid {
        color: #4CAF50 !important;
    }
    
    .invalid {
        color: #ff6b6b !important;
    }
    
    /* Alert styling */
    .stAlert {
        border-radius: 15px !important;
        backdrop-filter: blur(5px) !important;
        font-weight: 600 !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3) !important;
    }
    
    .stSuccess {
        background: rgba(76, 175, 80, 0.9) !important;
        color: white !important;
    }
    
    .stError {
        background: rgba(244, 67, 54, 0.9) !important;
        color: white !important;
    }
    
    .stWarning {
        background: rgba(255, 152, 0, 0.9) !important;
        color: white !important;
    }
    
    /* Sidebar improvements */
    .css-1aumxhk {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Radio button styling */
    .stRadio > label {
        color: white !important;
        font-weight: 500;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.15) !important;
        border-radius: 10px !important;
        color: white !important;
        font-weight: 600 !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3) !important;
    }
    
    .streamlit-expanderContent {
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3) !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Custom header section
st.markdown("""
<div class="custom-header">
    <div class="header-content">
        <div class="logo-section">
            <div class="logo-icon">🚀</div>
            <div>
                <h1 class="logo-text">AspirePath</h1>
                <p class="tagline">Your Journey to Success Starts Here</p>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Enhanced Sidebar Navigation with Option Menu ---
with st.sidebar:
    # Add logo and branding
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0; margin-bottom: 1rem;">
        <div style="font-size: 3rem; margin-bottom: 0.5rem;">🚀</div>
        <h2 style="color: white; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">AspirePath</h2>
        <p style="color: rgba(255,255,255,0.8); margin: 0.5rem 0 0 0; font-size: 0.85rem;">Your Career Journey</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced option menu with better styling
    page = option_menu(
        menu_title=None,
        options=[
            "Home", 
            "Log In / Sign Up", 
            "Skill Quiz & Resume Upload", 
            "Career Roadmap", 
            "Peer Comparison", 
            "Progress Tracker", 
            "Progress Dashboard"
        ],
        icons=[
            "house-fill", 
            "person-circle", 
            "file-earmark-text", 
            "map", 
            "people-fill", 
            "graph-up-arrow", 
            "speedometer2"
        ],
        menu_icon="cast",
        default_index=0,
        orientation="vertical",
        styles={
            "container": {
                "padding": "0!important", 
                "background-color": "transparent",
                "border-radius": "15px"
            },
            "icon": {
                "color": "rgba(255,255,255,0.8)", 
                "font-size": "18px"
            },
            "nav-link": {
                "font-size": "14px",
                "text-align": "left",
                "margin": "2px",
                "padding": "12px 16px",
                "background-color": "rgba(255,255,255,0.1)",
                "color": "rgba(255,255,255,0.9)",
                "border-radius": "10px",
                "border": "1px solid rgba(255,255,255,0.2)",
                "backdrop-filter": "blur(10px)",
                "transition": "all 0.3s ease"
            },
            "nav-link-selected": {
                "background-color": "rgba(255,255,255,0.25)",
                "color": "white",
                "border": "1px solid rgba(255,255,255,0.4)",
                "box-shadow": "0 4px 15px rgba(0,0,0,0.2)",
                "transform": "translateX(5px)"
            },
        }
    )

    # Add enhanced tip section with animation
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, rgba(255,255,255,0.15), rgba(255,255,255,0.05)); border-radius: 15px; margin: 1rem 0; border: 1px solid rgba(255,255,255,0.2); backdrop-filter: blur(10px);">
        <div style="font-size: 2rem; margin-bottom: 0.5rem; animation: pulse 2s infinite;">💡</div>
        <h4 style="color: white; margin-bottom: 0.5rem; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">Pro Tip</h4>
        <p style="color: rgba(255,255,255,0.9); font-size: 0.8rem; margin: 0; line-height: 1.4;">
            Upload your resume to unlock AI-powered skill analysis and get personalized career recommendations!
        </p>
    </div>
    """, unsafe_allow_html=True)

# Legacy navigation (to be replaced)
# --- Sidebar Navigation ---
st.sidebar.markdown("""
<div style="text-align: center; padding: 1rem 0; margin-bottom: 1rem;">
    <h2 style="color: white; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">🧭 Navigation</h2>
    <p style="color: rgba(255,255,255,0.8); margin: 0.5rem 0 0 0; font-size: 0.85rem;">Choose your destination</p>
</div>
""", unsafe_allow_html=True)

# page = st.sidebar.radio(
# Commented out legacy navigation - replaced with option menu above
#     [
#         "🏠 Home", 
#         "🔐 Log In / Sign Up", 
#         "📊 Skill Quiz & Resume Upload", 
#         "🎯 Career Roadmap", 
#         "🤝 Peer Comparison", 
#         "📈 Progress Tracker", 
        "� Progress Dashboard"
    ],
    index=0,  # Default to Home
#     label_visibility="collapsed"
# )

# # Add some additional sidebar content
# st.sidebar.markdown("---")
# st.sidebar.markdown("""
# <div style="text-align: center; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 15px; margin: 1rem 0;">
#     <h4 style="color: white; margin-bottom: 0.5rem;">💡 Quick Tip</h4>
#     <p style="color: rgba(255,255,255,0.9); font-size: 0.8rem; margin: 0;">
#         Upload your resume to get instant skill analysis and personalized career recommendations!
#     </p>
# </div>
""", unsafe_allow_html=True)

# Legacy navigation has been replaced with modern option menu above
# Clean up the page variable for logic consistency
page_clean = page

# Log In / Sign Up Section
if page_clean == "Log In / Sign Up":
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("# 🔐 Authentication")
        st.markdown("---")

    # Tabs for Log In and Sign Up
    tab1, tab2 = st.tabs(["🔑 Log In", "📝 Sign Up"])

    with tab1:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### Welcome Back!")
            st.markdown("Please enter your credentials to continue")
            
            login_email = st.text_input("📧 Email Address", key="login_email", placeholder="your.email@example.com")
            login_password = st.text_input("🔒 Password", type="password", key="login_password", placeholder="Enter your password")

            if st.button("🚀 Log In", key="login_btn"):
                if login_email and login_password:
                    if not validate_email(login_email):
                        st.error("❌ Please enter a valid email address.")
                    else:
                        hashed_password = hashlib.sha256(login_password.encode()).hexdigest()
                        user = users_collection.find_one({"email": login_email, "password": hashed_password})
                        if user:
                            st.success(f"🎉 Welcome back, {user['name']}!")
                            st.balloons()
                        else:
                            st.error("❌ Invalid email or password.")
                else:
                    st.warning("⚠️ Please enter both email and password.")

    with tab2:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### Create Your Account")
            st.markdown("Join AspirePath to start your career journey!")
            
            # Name input with validation
            signup_name = st.text_input("👤 Full Name", key="signup_name", placeholder="Enter your full name")
            if signup_name:
                if validate_name(signup_name):
                    st.markdown('<p class="validation-text valid">✅ Valid name</p>', unsafe_allow_html=True)
                else:
                    st.markdown('<p class="validation-text invalid">❌ Name must be at least 2 characters and contain only letters</p>', unsafe_allow_html=True)
            
            # Email input with validation
            signup_email = st.text_input("📧 Email Address", key="signup_email", placeholder="your.email@example.com")
            if signup_email:
                if validate_email(signup_email):
                    st.markdown('<p class="validation-text valid">✅ Valid email format</p>', unsafe_allow_html=True)
                else:
                    st.markdown('<p class="validation-text invalid">❌ Please enter a valid email address</p>', unsafe_allow_html=True)
            
            # Password input with validation
            signup_password = st.text_input("🔒 Password", type="password", key="signup_password", placeholder="Create a strong password")
            if signup_password:
                is_valid, message = validate_password(signup_password)
                if is_valid:
                    st.markdown('<p class="validation-text valid">✅ Strong password</p>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<p class="validation-text invalid">❌ {message}</p>', unsafe_allow_html=True)
            
            # Confirm password
            confirm_password = st.text_input("🔒 Confirm Password", type="password", key="confirm_password", placeholder="Confirm your password")
            if confirm_password and signup_password:
                if signup_password == confirm_password:
                    st.markdown('<p class="validation-text valid">✅ Passwords match</p>', unsafe_allow_html=True)
                else:
                    st.markdown('<p class="validation-text invalid">❌ Passwords do not match</p>', unsafe_allow_html=True)
            
            # Password requirements info
            with st.expander("🔍 Password Requirements"):
                st.markdown("""
                Your password must contain:
                - At least 8 characters
                - At least one uppercase letter (A-Z)
                - At least one lowercase letter (a-z)
                - At least one digit (0-9)
                - At least one special character (!@#$%^&*(),.?":{}|<>)
                """)

            if st.button("🎯 Create Account", key="signup_btn"):
                # Comprehensive validation
                validation_errors = []
                
                if not signup_name:
                    validation_errors.append("Name is required")
                elif not validate_name(signup_name):
                    validation_errors.append("Name must be at least 2 characters and contain only letters")
                
                if not signup_email:
                    validation_errors.append("Email is required")
                elif not validate_email(signup_email):
                    validation_errors.append("Please enter a valid email address")
                
                if not signup_password:
                    validation_errors.append("Password is required")
                else:
                    is_valid, password_error = validate_password(signup_password)
                    if not is_valid:
                        validation_errors.append(password_error)
                
                if not confirm_password:
                    validation_errors.append("Please confirm your password")
                elif signup_password != confirm_password:
                    validation_errors.append("Passwords do not match")
                
                if validation_errors:
                    for error in validation_errors:
                        st.error(f"❌ {error}")
                else:
                    # Check if user already exists
                    if users_collection.find_one({"email": signup_email}):
                        st.error("❌ An account with this email already exists. Please use a different email or try logging in.")
                    else:
                        try:
                            hashed_password = hashlib.sha256(signup_password.encode()).hexdigest()
                            user_data = {
                                "name": signup_name.strip(),
                                "email": signup_email.lower().strip(),
                                "password": hashed_password,
                                "created_at": st.session_state.get("current_time", "2024-01-01")
                            }
                            users_collection.insert_one(user_data)
                            st.success("🎉 Account created successfully! You can now log in.")
                            st.balloons()
                            
                            # Clear the form
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ An error occurred while creating your account. Please try again.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Home Section - Professional and sophisticated
if page_clean == "Home":
    # Hero section with professional glassmorphism
    st.markdown("""
    <div class="hero-section" style="
        text-align: center; 
        padding: 4rem 2rem; 
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 30px; 
        margin: 2rem 0; 
        border: 1px solid rgba(255,255,255,0.2);
        box-shadow: 
            0 25px 50px rgba(0, 0, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        position: relative;
        overflow: hidden;
    ">
        <div style="position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, transparent, #ffd700, transparent);"></div>
        <div style="font-size: 4rem; margin-bottom: 1.5rem; animation: heroGlow 3s ease-in-out infinite alternate;">🌟</div>
        <h1 style="
            font-size: 3.2rem; 
            margin-bottom: 1.5rem; 
            background: linear-gradient(45deg, #ffd700, #ffed4e, #fff); 
            -webkit-background-clip: text; 
            -webkit-text-fill-color: transparent; 
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            font-weight: 800;
            letter-spacing: -1px;
        ">
            Transform Your Career Journey
        </h1>
        <p style="
            font-size: 1.5rem; 
            color: white; 
            margin-bottom: 1rem; 
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            font-weight: 300;
            letter-spacing: 0.5px;
        ">
            Discover your potential, build your skills, achieve your dreams
        </p>
        <p style="
            font-size: 1.1rem; 
            color: rgba(255,255,255,0.9); 
            margin-bottom: 2.5rem;
            font-weight: 300;
        ">
            Start your personalized career development journey today
        </p>
        <div style="display: flex; justify-content: center; gap: 1.5rem; flex-wrap: wrap;">
            <div style="
                background: rgba(255,255,255,0.15); 
                padding: 0.75rem 1.5rem; 
                border-radius: 25px; 
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255,255,255,0.2);
                transition: all 0.3s ease;
            ">
                <span style="color: #ffd700; font-weight: 600; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">✨ AI-Powered</span>
            </div>
            <div style="
                background: rgba(255,255,255,0.15); 
                padding: 0.75rem 1.5rem; 
                border-radius: 25px; 
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255,255,255,0.2);
                transition: all 0.3s ease;
            ">
                <span style="color: #ffd700; font-weight: 600; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">🎯 Personalized</span>
            </div>
            <div style="
                background: rgba(255,255,255,0.15); 
                padding: 0.75rem 1.5rem; 
                border-radius: 25px; 
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255,255,255,0.2);
                transition: all 0.3s ease;
            ">
                <span style="color: #ffd700; font-weight: 600; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">🚀 Results-Driven</span>
            </div>
        </div>
    </div>
    
    <style>
    @keyframes heroGlow {
        0% { 
            filter: drop-shadow(0 0 10px rgba(255, 215, 0, 0.3)); 
            transform: scale(1);
        }
        100% { 
            filter: drop-shadow(0 0 20px rgba(255, 215, 0, 0.6)); 
            transform: scale(1.05);
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # Professional feature cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div style="font-size: 3.5rem; margin-bottom: 1.5rem; color: #ffd700; filter: drop-shadow(0 4px 8px rgba(0,0,0,0.2));">🎯</div>
            <h3 style="color: white; margin-bottom: 1rem; font-size: 1.4rem; font-weight: 600; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">Personalized Guidance</h3>
            <p style="color: rgba(255,255,255,0.9); font-size: 1rem; line-height: 1.6; font-weight: 300;">Get tailored career roadmaps based on your skills and aspirations</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div style="font-size: 3.5rem; margin-bottom: 1.5rem; color: #ffd700; filter: drop-shadow(0 4px 8px rgba(0,0,0,0.2));">📊</div>
            <h3 style="color: white; margin-bottom: 1rem; font-size: 1.4rem; font-weight: 600; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">Skill Assessment</h3>
            <p style="color: rgba(255,255,255,0.9); font-size: 1rem; line-height: 1.6; font-weight: 300;">Take comprehensive quizzes to identify your strengths and improvement areas</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div style="font-size: 3.5rem; margin-bottom: 1.5rem; color: #ffd700; filter: drop-shadow(0 4px 8px rgba(0,0,0,0.2));">📈</div>
            <h3 style="color: white; margin-bottom: 1rem; font-size: 1.4rem; font-weight: 600; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">Progress Tracking</h3>
            <p style="color: rgba(255,255,255,0.9); font-size: 1rem; line-height: 1.6; font-weight: 300;">Monitor your learning journey with detailed analytics and insights</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Getting started section
    st.markdown("""
    <div style="background: rgba(255,255,255,0.9); padding: 2rem; border-radius: 15px; margin: 2rem 0;">
        <h2 style="color: #333; text-align: center; margin-bottom: 2rem;">🌟 Why Choose AspirePath?</h2>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; margin: 2rem 0;">
            <div style="padding: 1rem; background: linear-gradient(135deg, #667eea, #764ba2); color: white; border-radius: 10px;">
                <h4>🎯 AI-Powered Recommendations</h4>
                <p style="margin: 0; font-size: 0.9rem;">Smart algorithms analyze your profile to suggest the best career paths</p>
            </div>
            <div style="padding: 1rem; background: linear-gradient(135deg, #f093fb, #f5576c); color: white; border-radius: 10px;">
                <h4>📚 Curated Learning Resources</h4>
                <p style="margin: 0; font-size: 0.9rem;">Access handpicked tutorials, courses, and project ideas</p>
            </div>
            <div style="padding: 1rem; background: linear-gradient(135deg, #4facfe, #00f2fe); color: white; border-radius: 10px;">
                <h4>🤝 Peer Comparison</h4>
                <p style="margin: 0; font-size: 0.9rem;">Benchmark your skills against industry standards and peers</p>
            </div>
            <div style="padding: 1rem; background: linear-gradient(135deg, #43e97b, #38f9d7); color: white; border-radius: 10px;">
                <h4>📊 Real-time Analytics</h4>
                <p style="margin: 0; font-size: 0.9rem;">Track your progress with detailed insights and visualizations</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # How to get started
    st.markdown("""
    <div style="background: rgba(255,255,255,0.9); padding: 2rem; border-radius: 15px; margin: 2rem 0;">
        <h2 style="color: #333; text-align: center; margin-bottom: 2rem;">📖 How to Get Started?</h2>
        
        <div style="display: flex; justify-content: space-around; flex-wrap: wrap; gap: 2rem;">
            <div style="flex: 1; min-width: 200px; text-align: center;">
                <div style="width: 60px; height: 60px; background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem; color: white; font-size: 1.5rem; font-weight: bold;">1</div>
                <h4 style="color: #333;">Create Account</h4>
                <p style="color: #666; font-size: 0.9rem;">Sign up to start your personalized career journey</p>
            </div>
            <div style="flex: 1; min-width: 200px; text-align: center;">
                <div style="width: 60px; height: 60px; background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem; color: white; font-size: 1.5rem; font-weight: bold;">2</div>
                <h4 style="color: #333;">Assess Skills</h4>
                <p style="color: #666; font-size: 0.9rem;">Upload your resume or take our skill assessment quiz</p>
            </div>
            <div style="flex: 1; min-width: 200px; text-align: center;">
                <div style="width: 60px; height: 60px; background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem; color: white; font-size: 1.5rem; font-weight: bold;">3</div>
                <h4 style="color: #333;">Get Roadmap</h4>
                <p style="color: #666; font-size: 0.9rem;">Receive a personalized learning path to your goals</p>
            </div>
            <div style="flex: 1; min-width: 200px; text-align: center;">
                <div style="width: 60px; height: 60px; background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem; color: white; font-size: 1.5rem; font-weight: bold;">4</div>
                <h4 style="color: #333;">Track Progress</h4>
                <p style="color: #666; font-size: 0.9rem;">Monitor your growth and celebrate achievements</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Call to action
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea, #764ba2); padding: 3rem; border-radius: 20px; text-align: center; margin: 3rem 0;">
        <h2 style="color: white; margin-bottom: 1rem;">Ready to Transform Your Career?</h2>
        <p style="color: rgba(255,255,255,0.9); font-size: 1.1rem; margin-bottom: 2rem;">Start your personalized career development journey with AspirePath</p>
        <a href="#" style="background: white; color: #667eea; padding: 1rem 2rem; border-radius: 25px; text-decoration: none; font-weight: 600; display: inline-block; transition: transform 0.3s ease;">
            Get Started Today 🚀
        </a>
    </div>
    """, unsafe_allow_html=True)

    # Pro tip section
    st.markdown("""
    <div style="background: rgba(255,255,255,0.9); padding: 2rem; border-radius: 15px; border-left: 5px solid #667eea; margin: 2rem 0;">
        <h3 style="color: #333; margin-bottom: 1rem;">💡 Pro Tip</h3>
        <p style="color: #666; margin: 0; font-size: 1rem;">
            Regularly update your skills and revisit AspirePath to stay on track with your career goals! 
            Set aside time each week to review your progress and discover new learning opportunities.
        </p>
    </div>
    """, unsafe_allow_html=True)

elif page_clean == "Skill Quiz & Resume Upload":
    st.header("📄 Upload Resume & Take Skill Quiz")

    # Resume Upload Section
    uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

    if uploaded_file:
        resume_text = parse_resume(uploaded_file)
        user_skills = assess_skills(resume_text)
        st.success(f"Extracted Skills: {', '.join(user_skills)}")

    st.markdown("Or manually enter your current skills (comma separated):")
    manual_input = st.text_input("Example: Python, SQL, Power BI")
    if manual_input:
        user_skills = [skill.strip() for skill in manual_input.split(",")]
        st.success(f"Using manual skills: {', '.join(user_skills)}")

    # Skill Quiz Section
    if user_skills:
        st.subheader("📝 Skill Assessment Quiz")
        st.write("Debug: User skills detected:", user_skills)  # Debug log

        # Fetch questions dynamically from the API
        questions = fetch_questions_from_api(user_skills)

        if not questions:
            st.warning("No questions could be fetched from the API. Please try again later.")
        else:
            with st.form("quiz_form"):
                user_answers = {}

                for idx, question in enumerate(questions):
                    st.markdown(f"**Q{idx + 1}: {question['question']}**")
                    user_answers[question['id']] = st.radio(
                        "Select an answer:",
                        options=question['options'],
                        key=f"q{idx + 1}"
                    )

                submitted = st.form_submit_button("Submit Quiz")

            # Store quiz results after submission
            if submitted:
                score = sum(1 for q in questions if user_answers.get(q['id']) == q['answer'])
                total = len(questions)
                wrong_qs = [q for q in questions if user_answers.get(q['id']) != q['answer']]

                # Save quiz results to the database
                store_quiz_results(user_id="user123", quiz_results={
                    "score": score,
                    "total": total,
                    "wrong_answers": wrong_qs
                })

                st.success(f"✅ You scored {score} out of {total}")

                if wrong_qs:
                    st.subheader("🔍 Review Incorrect Answers")
                    for q in wrong_qs:
                        st.markdown(f"**Q:** {q['question']}")
                        st.markdown(f"❌ Your Answer: {user_answers.get(q['id'])}")
                        st.markdown(f"✅ Correct Answer: **{q['answer']}**")
    else:
        st.warning("No skills found. Please upload a resume or enter skills manually.")

elif page_clean == "Career Roadmap":
    st.header("🎯 Choose Your Career Goal")

    # Input for user skills
    user_input_skills = st.text_input("Enter your skills (comma-separated, e.g., Python, SQL, Power BI):")

    if user_input_skills:
        user_skills = [skill.strip() for skill in user_input_skills.split(",")]
        predicted_career = predict_career(user_skills)

        st.subheader(f"🔮 Predicted Career Goal: {predicted_career}")

        st.subheader("📚 Personalized Learning Roadmap")
        roadmap, all_required = generate_roadmap(user_skills, predicted_career)

        # Debugging logs to trace data flow
        st.write("Debug: User input skills:", user_input_skills)
        st.write("Debug: Predicted career goal:", predicted_career)
        st.write("Debug: Generated roadmap:", roadmap)

        if not roadmap:
            st.warning("No roadmap could be generated. Please check your input skills or try a different set of skills.")
        else:
            for step in roadmap:
                st.markdown(f"✅ {step}")

        # Generate a step-by-step learning roadmap
        st.subheader("📘 Step-by-Step Learning Roadmap")
        if roadmap:
            for idx, step in enumerate(roadmap, start=1):
                st.markdown(f"{idx}. {step}")
        else:
            st.success("You already have all the required skills for this career goal!")

        st.subheader("🎥 Curated YouTube Tutorials")
        for skill in roadmap:
            query = skill.replace("Learn ", "")
            st.markdown(f"**{query}**:")
            for link in fetch_youtube_resources(query):
                st.markdown(f"- [Watch Tutorial]({link})")

        st.subheader("📘 Suggested Tutorials and Courses")

        # Example curated resources
        resources = [
            {"title": "Python for Everybody", "platform": "Coursera", "link": "https://www.coursera.org/specializations/python"},
            {"title": "Full-Stack Web Development", "platform": "Udemy", "link": "https://www.udemy.com/course/the-web-developer-bootcamp/"},
            {"title": "Machine Learning", "platform": "edX", "link": "https://www.edx.org/course/machine-learning"},
            {"title": "Data Science Professional Certificate", "platform": "IBM on Coursera", "link": "https://www.coursera.org/professional-certificates/ibm-data-science"},
            {"title": "Cybersecurity Fundamentals", "platform": "Pluralsight", "link": "https://www.pluralsight.com/courses/cyber-security-fundamentals"}
        ]

        for resource in resources:
            st.markdown(f"- **{resource['title']}** on {resource['platform']}: [Link]({resource['link']})")
    else:
        st.warning("Please enter your skills to generate a career roadmap.")

elif page_clean == "Peer Comparison":
    st.header("🤝 Peer Skill Comparison Based on Resumes")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Person 1")
        person1_resume = st.file_uploader("Upload Resume (PDF or DOCX):", type=["pdf", "docx"], key="person1_resume")
        person1_skills = []
        if person1_resume:
            person1_text = parse_resume(person1_resume)
            person1_skills = assess_skills(person1_text)
            st.success(f"Extracted Skills: {', '.join(person1_skills)}")

    with col2:
        st.subheader("Person 2")
        person2_resume = st.file_uploader("Upload Resume (PDF or DOCX):", type=["pdf", "docx"], key="person2_resume")
        person2_skills = []
        if person2_resume:
            person2_text = parse_resume(person2_resume)
            person2_skills = assess_skills(person2_text)
            st.success(f"Extracted Skills: {', '.join(person2_skills)}")

    if person1_skills and person2_skills:
        st.subheader("🔍 Comparison Results")

        common_skills = set(person1_skills) & set(person2_skills)
        unique_to_person1 = set(person1_skills) - set(person2_skills)
        unique_to_person2 = set(person2_skills) - set(person1_skills)

        st.markdown("**Common Skills:**")
        st.write(common_skills if common_skills else "None")

        st.markdown("**Unique to Person 1:**")
        st.write(unique_to_person1 if unique_to_person1 else "None")

        st.markdown("**Unique to Person 2:**")
        st.write(unique_to_person2 if unique_to_person2 else "None")

# Progress Tracking Section
if page_clean == "Progress Tracker":
    st.header("📈 Weekly Progress Tracker")

    # Input for weekly achievements
    st.subheader("🏆 Log Your Weekly Achievements")
    weekly_achievements = st.text_area("Enter your achievements for this week (e.g., completed Python course, built a project):")

    # Store weekly achievements in the database
    progress_collection = db["progress"]

    if st.button("Submit Achievements"):
        if weekly_achievements:
            # Example structure for storing data
            progress_data = {
                "user_id": "user123",  # Replace with dynamic user ID if available
                "date": pd.Timestamp.now(),
                "achievements": weekly_achievements,
                "skills_learned": len(weekly_achievements.split(',')),  # Example logic
                "projects_completed": weekly_achievements.lower().count("project")  # Example logic
            }
            progress_collection.insert_one(progress_data)
            st.success("Your achievements have been logged successfully!")
        else:
            st.warning("Please enter your achievements before submitting.")

    # Suggestions based on achievements
    st.subheader("💡 Suggestions for Next Week")
    if weekly_achievements:
        st.markdown("Based on your achievements, here are some suggestions:")
        st.markdown("- Continue learning advanced Python topics.")
        st.markdown("- Start a new project using the skills you've learned.")
        st.markdown("- Explore related fields like Data Analysis or Machine Learning.")
    else:
        st.info("Log your achievements to receive personalized suggestions.")

# Progress Dashboard Section
if page_clean == "Progress Dashboard":
    st.header("📊 Progress Dashboard")

    # Example data for progress tracking
    import pandas as pd
    import altair as alt

    data = pd.DataFrame({
        'Week': ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
        'Skills Learned': [3, 5, 2, 4],
        'Projects Completed': [1, 2, 1, 3]
    })

    # Line chart for skills learned
    st.subheader("📈 Skills Learned Over Time")
    skills_chart = alt.Chart(data).mark_line(point=True).encode(
        x='Week',
        y='Skills Learned',
        tooltip=['Week', 'Skills Learned']
    ).properties(width=700, height=400)
    st.altair_chart(skills_chart)

    # Bar chart for projects completed
    st.subheader("📊 Projects Completed Over Time")
    projects_chart = alt.Chart(data).mark_bar().encode(
        x='Week',
        y='Projects Completed',
        tooltip=['Week', 'Projects Completed']
    ).properties(width=700, height=400)
    st.altair_chart(projects_chart)

    st.info("Update your weekly achievements in the Progress Tracker to see your progress here!")
