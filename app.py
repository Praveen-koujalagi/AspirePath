import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
from core import assess_skills, select_goal, generate_roadmap, predict_career, get_career_matches
from helpers_session import (
    parse_resume, fetch_youtube_resources, store_quiz_results, 
    validate_email, validate_password, validate_name, store_progress_achievement,
    create_user, authenticate_user, find_user_by_email, get_session_stats, 
    init_session_state_db, get_user_progress_stats
)
from project_suggester import suggest_projects
from quiz_engine import load_questions, run_quiz, fetch_questions_from_api
import hashlib
import requests
import json

# Initialize session state for authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'user_email' not in st.session_state:
    st.session_state.user_email = ""

# Initialize session state database
init_session_state_db()

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

# Complete black theme for full visibility
st.markdown(
    """
    <style>
    /* FORCE BLACK BACKGROUND EVERYWHERE */
    .main, .block-container, div[data-testid="stAppViewContainer"], 
    div[data-testid="stMain"], section[data-testid="stSidebar"] {
        background-color: #000000 !important;
        color: white !important;
    }
    
    /* SIDEBAR - Complete black theme */
    .css-1d391kg, .css-1aumxhk, div[data-testid="stSidebar"] > div,
    .sidebar .sidebar-content, section[data-testid="stSidebar"] * {
        background-color: #000000 !important;
        color: white !important;
    }
    
    /* SIDEBAR specific elements */
    section[data-testid="stSidebar"] {
        background-color: #000000 !important;
    }
    
    section[data-testid="stSidebar"] > div:first-child {
        background-color: #000000 !important;
    }
    
    /* ALL TEXT ELEMENTS - Force white */
    *, p, div, span, label, li, td, th, a, 
    .stMarkdown, .stText, .element-container {
        color: white !important;
        background-color: transparent !important;
    }
    
    /* HEADERS - Gold color for visibility */
    h1, h2, h3, h4, h5, h6, .stTitle {
        color: #FFD700 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8) !important;
        background-color: transparent !important;
    }
    
    /* BUTTONS - Dark with gold border */
    .stButton > button {
        background-color: #1a1a1a !important;
        color: white !important;
        border: 2px solid #FFD700 !important;
        border-radius: 10px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: bold !important;
    }
    
    .stButton > button:hover {
        background-color: #FFD700 !important;
        color: black !important;
        transform: scale(1.05);
    }
    
    /* INPUT FIELDS - Dark theme */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select, .stNumberInput > div > div > input {
        background-color: #1a1a1a !important;
        color: white !important;
        border: 2px solid #444444 !important;
        border-radius: 8px !important;
    }
    
    .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
        border-color: #FFD700 !important;
        box-shadow: 0 0 0 2px rgba(255, 215, 0, 0.3) !important;
    }
    
    /* INPUT LABELS */
    .stTextInput label, .stTextArea label, .stSelectbox label,
    .stNumberInput label, .stFileUploader label {
        color: #FFD700 !important;
        font-weight: bold !important;
    }
    
    /* TABS - Dark theme */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #1a1a1a !important;
        border-radius: 10px !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #333333 !important;
        color: white !important;
        border: 1px solid #666666 !important;
        border-radius: 5px !important;
        margin: 0 2px !important;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #FFD700 !important;
        color: black !important;
        font-weight: bold !important;
    }
    
    /* OPTION MENU - Force dark theme */
    .nav-link, .nav-link-selected, div[data-testid="stSidebar"] .nav-link {
        color: white !important;
        background-color: #1a1a1a !important;
    }
    
    .nav-link-selected {
        background-color: #FFD700 !important;
        color: black !important;
    }
    
    /* STREAMLIT SPECIFIC ELEMENTS */
    .stAlert, .stSuccess, .stError, .stWarning, .stInfo {
        color: white !important;
        font-weight: bold !important;
    }
    
    .stSuccess {
        background-color: #006600 !important;
        border: 1px solid #00AA00 !important;
    }
    
    .stError {
        background-color: #660000 !important;
        border: 1px solid #AA0000 !important;
    }
    
    .stWarning {
        background-color: #663300 !important;
        border: 1px solid #AA5500 !important;
    }
    
    .stInfo {
        background-color: #003366 !important;
        border: 1px solid #0055AA !important;
    }
    
    /* CARDS AND CONTAINERS */
    .element-container, .stContainer, .stColumn {
        background-color: transparent !important;
    }
    
    /* FILE UPLOADER */
    .stFileUploader {
        background-color: #1a1a1a !important;
        border: 2px dashed #666666 !important;
        border-radius: 10px !important;
        color: white !important;
    }
    
    /* SELECTBOX */
    .stSelectbox > div > div {
        background-color: #1a1a1a !important;
        color: white !important;
    }
    
    /* RADIO BUTTONS */
    .stRadio > label {
        color: white !important;
    }
    
    /* CHECKBOX */
    .stCheckbox > label {
        color: white !important;
    }
    
    /* SLIDER */
    .stSlider > label {
        color: #FFD700 !important;
    }
    
    /* EXPANDER */
    .streamlit-expanderHeader {
        background-color: #1a1a1a !important;
        color: white !important;
        border: 1px solid #444444 !important;
    }
    
    .streamlit-expanderContent {
        background-color: #0d0d0d !important;
        color: white !important;
        border: 1px solid #444444 !important;
    }
    
    /* METRIC */
    .metric-container {
        background-color: #1a1a1a !important;
        color: white !important;
        border: 1px solid #444444 !important;
        border-radius: 10px !important;
        padding: 1rem !important;
    }
    
    /* DATAFRAME */
    .stDataFrame {
        background-color: #1a1a1a !important;
        color: white !important;
    }
    
    /* ENSURE NO WHITE BACKGROUNDS */
    div, section, article, main, header, footer {
        background-color: transparent !important;
    }
    
    /* FORCE VISIBILITY FOR ALL CONTENT */
    .main .block-container * {
        color: white !important;
    }
    
    /* SIDEBAR CONTENT OVERRIDE */
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* MARKDOWN CONTENT */
    .stMarkdown, .stText {
        color: white !important;
    }
    
    /* SPECIAL STYLING FOR FEATURE CARDS */
    .feature-card, .card {
        background-color: #1a1a1a !important;
        border: 2px solid #333333 !important;
        border-radius: 15px !important;
        padding: 1.5rem !important;
        margin: 1rem 0 !important;
        color: white !important;
    }
    
    /* AUTH CONTAINER - Fix the white box issue */
    .auth-container {
        background-color: #1a1a1a !important;
        border: 2px solid #333333 !important;
        border-radius: 20px !important;
        padding: 2rem !important;
        margin: 2rem auto !important;
        color: white !important;
        max-width: 800px !important;
    }
    
    .auth-container * {
        color: white !important;
        background-color: transparent !important;
    }
    
    /* FORCE DARK BACKGROUND FOR ALL TAB CONTENT */
    .stTabs [data-baseweb="tab-panel"], 
    .stTabs [data-baseweb="tab-panel"] *,
    .stTabs [data-baseweb="tab-panel"] > div,
    .stTabs [data-baseweb="tab-panel"] > div > div {
        background-color: transparent !important;
        color: white !important;
    }
    
    /* OVERRIDE STREAMLIT'S WHITE BACKGROUNDS */
    div[data-stale="false"], 
    .element-container div,
    .stForm,
    .block-container > div,
    .main .block-container > div > div,
    .main .block-container > div > div > div {
        background-color: transparent !important;
        color: white !important;
    }
    
    /* SPECIFIC FIX FOR WHITE CONTAINERS */
    .stContainer, .stContainer > div,
    .css-1kyxreq, .css-12ttj6m, .css-1d391kg,
    .css-1aumxhk, .css-k1vhr4, .css-1v0mbdj {
        background-color: transparent !important;
        color: white !important;
    }
    
    .auth-container h1, .auth-container h2, .auth-container h3 {
        color: #FFD700 !important;
    }
    
    /* TAB CONTENT - Ensure visibility */
    .stTabs [data-baseweb="tab-panel"] {
        background-color: transparent !important;
        color: white !important;
    }
    
    .stTabs [data-baseweb="tab-panel"] * {
        color: white !important;
    }
    
    /* COLUMNS inside auth container */
    .auth-container .element-container {
        background-color: transparent !important;
    }
    
    /* Specific fixes for login/signup forms */
    .auth-container .stTextInput label {
        color: #FFD700 !important;
        font-weight: bold !important;
    }
    
    .auth-container .stTextInput input {
        background-color: #2a2a2a !important;
        color: white !important;
        border: 2px solid #444444 !important;
    }
    
    .auth-container .stButton button {
        background-color: #333333 !important;
        color: white !important;
        border: 2px solid #FFD700 !important;
    }
    
    /* Force white text in all auth sections */
    div[class*="auth"] * {
        color: white !important;
    }
    
    /* CSS for validation messages */
    .validation-text {
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        margin-top: 0.25rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    .validation-text.valid {
        color: #4CAF50 !important;
    }
    
    .validation-text.invalid {
        color: #FF6B6B !important;
    }
    
    /* ADDITIONAL FORCE OVERRIDES FOR STREAMLIT ELEMENTS */
    .stTabs, .stTabs > div, .stTabs > div > div {
        background-color: transparent !important;
    }
    
    /* OVERRIDE ANY REMAINING WHITE AREAS */
    .css-1544g2n, .css-18e3th9, .css-1d391kg, 
    .css-12ttj6m, .css-1aumxhk, .css-k1vhr4 {
        background-color: transparent !important;
        color: white !important;
    }
    
    /* LATEST STREAMLIT CLASSES - FORCE TRANSPARENT */
    .st-emotion-cache-16txtl3, .st-emotion-cache-1y4p8pa, 
    .st-emotion-cache-12w0qpk, .st-emotion-cache-1r6slb0,
    .st-emotion-cache-1wmy9hl, .st-emotion-cache-nahz7x,
    .st-emotion-cache-ocqkz7, .st-emotion-cache-1y5z0bw {
        background-color: transparent !important;
        background: transparent !important;
        color: white !important;
    }
    
    /* STREAMLIT TAB OVERRIDES */
    .st-emotion-cache-1kyxreq, .st-emotion-cache-1v0mbdj,
    .st-emotion-cache-16txtl3 > div,
    .st-emotion-cache-1y4p8pa > div,
    [data-baseweb="tab-list"] {
        background-color: #1a1a1a !important;
        background: #1a1a1a !important;
    }
    
    [data-baseweb="tab"] {
        background-color: #333333 !important;
        background: #333333 !important;
        color: white !important;
        border: 1px solid #666666 !important;
    }
    
    [data-baseweb="tab"][aria-selected="true"] {
        background-color: #ffd700 !important;
        background: #ffd700 !important;
        color: black !important;
    }
    
    [data-baseweb="tab-panel"] {
        background-color: transparent !important;
        background: transparent !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True
)

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
    
    # Show user status if authenticated
    if st.session_state.authenticated:
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 10px; margin-bottom: 1rem;">
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">👤</div>
            <h4 style="color: white; margin: 0; font-size: 0.9rem;">Welcome back!</h4>
            <p style="color: rgba(255,255,255,0.8); margin: 0; font-size: 0.8rem;">{st.session_state.user_name}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Enhanced option menu with authentication-based access
    if st.session_state.authenticated:
        # Show full menu for authenticated users
        page = option_menu(
            menu_title=None,
            options=[
                "Home", 
                "Skill Quiz & Resume Upload", 
                "Career Roadmap", 
                "Peer Comparison", 
                "Progress Tracker", 
                "Progress Dashboard",
                "Logout"
            ],
            icons=[
                "house-fill", 
                "file-earmark-text", 
                "map", 
                "people-fill", 
                "graph-up-arrow", 
                "speedometer2",
                "box-arrow-right"
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
        
        # Handle logout
        if page == "Logout":
            st.session_state.authenticated = False
            st.session_state.user_name = ""
            st.session_state.user_email = ""
            st.rerun()
            
    else:
        # Show limited menu for non-authenticated users
        # Check if user clicked get started to redirect to login
        redirect_to_login = st.session_state.get('redirect_to_login', False)
        
        page = option_menu(
            menu_title=None,
            options=[
                "Home", 
                "Log In / Sign Up"
            ],
            icons=[
                "house-fill", 
                "person-circle"
            ],
            menu_icon="cast",
            default_index=1 if redirect_to_login else 0,  # Redirect to login if button clicked
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

# Legacy navigation commented out - replaced with option menu
# Clean up the page variable for logic consistency
page_clean = page

# Log In / Sign Up Section
if page_clean == "Log In / Sign Up":
    # Reset redirect flag when user reaches login page
    if st.session_state.get('redirect_to_login', False):
        st.session_state.redirect_to_login = False
    
    # Enhanced header section with better branding
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; margin-bottom: 2rem;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">🚀</div>
        <h1 style="font-size: 2.8rem; background: linear-gradient(45deg, #ffd700, #ffed4e, #fff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; margin-bottom: 0.5rem;">Connect to AspirePath</h1>
        <p style="font-size: 1.2rem; color: rgba(255,255,255,0.9); margin-bottom: 0;">Your gateway to career transformation and success</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Apply ultra-aggressive CSS just for this page
    st.markdown("""
    <style>
    /* ULTRA AGGRESSIVE OVERRIDES FOR AUTH PAGE */
    .element-container:has(.stTabs), 
    .stTabs,
    .stTabs > div,
    .stTabs [data-baseweb="tab-list"],
    .stTabs [data-baseweb="tab-panel"],
    .stTabs [data-baseweb="tab-panel"] > div,
    .block-container > div:has(.stTabs),
    div:has(.stTabs) {
        background-color: transparent !important;
        background: transparent !important;
    }
    
    /* TARGET ALL POSSIBLE STREAMLIT CONTAINERS */
    [data-testid="column"] > div,
    [data-testid="column"] > div > div,
    [data-testid="column"] > div > div > div,
    .element-container > div,
    .element-container > div > div,
    .stForm,
    .stForm > div,
    .row-widget,
    .row-widget > div {
        background-color: transparent !important;
        background: transparent !important;
        color: white !important;
    }
    
    /* FORCE TRANSPARENT ON ALL STREAMLIT WIDGETS */
    .stTextInput,
    .stTextInput > div,
    .stTextInput > div > div,
    .stButton,
    .stButton > div,
    .stRadio,
    .stRadio > div,
    .stExpander,
    .stExpander > div {
        background-color: transparent !important;
        background: transparent !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create a custom HTML container that overrides Streamlit completely
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #000000, #1a1a1a) !important;
        border: 3px solid #ffd700 !important;
        border-radius: 25px !important;
        padding: 3rem !important;
        margin: 2rem auto !important;
        color: white !important;
        max-width: 900px !important;
        box-shadow: 0 20px 50px rgba(0,0,0,0.8) !important;
        position: relative !important;
        z-index: 1000 !important;
    ">
        <div style="text-align: center; margin-bottom: 2rem;">
            <h2 style="color: #ffd700; font-size: 2rem; margin-bottom: 1rem;">Choose Your Action</h2>
            <p style="color: white; font-size: 1.1rem;">Sign in to your account or create a new one</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Create manual tabs using buttons instead of st.tabs
    col1, col2 = st.columns(2)
    
    with col1:
        login_tab = st.button("🔑 Sign In", use_container_width=True, key="login_tab_btn")
    
    with col2:
        signup_tab = st.button("🌟 Join AspirePath", use_container_width=True, key="signup_tab_btn")
    
    # Initialize tab state
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = 'login'
    
    if login_tab:
        st.session_state.active_tab = 'login'
    elif signup_tab:
        st.session_state.active_tab = 'signup'
    
    # Show content based on active tab
    if st.session_state.active_tab == 'login':
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #1a1a1a, #2a2a2a) !important;
            border: 2px solid #444444 !important;
            border-radius: 15px !important;
            padding: 2rem !important;
            margin: 1rem 0 !important;
            color: white !important;
        ">
            <div style="text-align: center; margin-bottom: 2rem;">
                <h3 style="color: #ffd700; font-size: 1.8rem; margin-bottom: 0.5rem;">Welcome Back! 👋</h3>
                <p style="color: white; font-size: 1rem;">Sign in to continue your career journey</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            login_email = st.text_input("📧 Email Address", key="login_email", placeholder="your.email@example.com")
            login_password = st.text_input("🔒 Password", type="password", key="login_password", placeholder="Enter your password")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🚀 Sign In to AspirePath", key="login_btn", use_container_width=True):
                if login_email and login_password:
                    if not validate_email(login_email):
                        st.error("❌ Please enter a valid email address.")
                    else:
                        user = authenticate_user(login_email, login_password)
                        if user:
                            # Set session state for authentication
                            st.session_state.authenticated = True
                            st.session_state.user_name = user['name']
                            st.session_state.user_email = user['email']
                            st.success(f"🎉 Welcome back, {user['name']}!")
                            st.balloons()
                            st.rerun()  # Refresh the app to show authenticated menu
                        else:
                            st.error("❌ Invalid email or password.")
                else:
                    st.warning("⚠️ Please enter both email and password.")

    else:  # signup tab
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #1a1a1a, #2a2a2a) !important;
            border: 2px solid #444444 !important;
            border-radius: 15px !important;
            padding: 2rem !important;
            margin: 1rem 0 !important;
            color: white !important;
        ">
            <div style="text-align: center; margin-bottom: 2rem;">
                <h3 style="color: #ffd700; font-size: 1.8rem; margin-bottom: 0.5rem;">Start Your Journey! 🌟</h3>
                <p style="color: white; font-size: 1rem;">Create your account and unlock your career potential</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            # Name input with validation
            signup_name = st.text_input("👤 Full Name", key="signup_name", placeholder="Enter your full name")
            if signup_name:
                if validate_name(signup_name):
                    st.markdown('<p style="color: #4CAF50; font-size: 0.85rem;">✅ Valid name</p>', unsafe_allow_html=True)
                else:
                    st.markdown('<p style="color: #FF6B6B; font-size: 0.85rem;">❌ Name must be at least 2 characters and contain only letters</p>', unsafe_allow_html=True)
            
            # Email input with validation
            signup_email = st.text_input("📧 Email Address", key="signup_email", placeholder="your.email@example.com")
            if signup_email:
                if validate_email(signup_email):
                    st.markdown('<p style="color: #4CAF50; font-size: 0.85rem;">✅ Valid email format</p>', unsafe_allow_html=True)
                else:
                    st.markdown('<p style="color: #FF6B6B; font-size: 0.85rem;">❌ Please enter a valid email address</p>', unsafe_allow_html=True)
            
            # Password input with validation
            signup_password = st.text_input("🔒 Password", type="password", key="signup_password", placeholder="Create a strong password")
            if signup_password:
                is_valid, message = validate_password(signup_password)
                if is_valid:
                    st.markdown('<p style="color: #4CAF50; font-size: 0.85rem;">✅ Strong password</p>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<p style="color: #FF6B6B; font-size: 0.85rem;">❌ {message}</p>', unsafe_allow_html=True)
            
            # Confirm password
            confirm_password = st.text_input("🔒 Confirm Password", type="password", key="confirm_password", placeholder="Confirm your password")
            if confirm_password and signup_password:
                if signup_password == confirm_password:
                    st.markdown('<p style="color: #4CAF50; font-size: 0.85rem;">✅ Passwords match</p>', unsafe_allow_html=True)
                else:
                    st.markdown('<p style="color: #FF6B6B; font-size: 0.85rem;">❌ Passwords do not match</p>', unsafe_allow_html=True)
            
            st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
            
            # Password requirements info
            with st.expander("🔍 Password Requirements"):
                st.markdown("""
                **Your password must contain:**
                - ✅ At least 8 characters
                - ✅ At least one uppercase letter (A-Z)
                - ✅ At least one lowercase letter (a-z)
                - ✅ At least one digit (0-9)
                - ✅ At least one special character (!@#$%^&*(),.?":{}|<>)
                """)

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🎯 Join AspirePath Now", key="signup_btn", use_container_width=True):
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
                    # Check if user already exists using session state
                    if find_user_by_email(signup_email):
                        st.error("❌ An account with this email already exists. Please use a different email or try logging in.")
                    else:
                        try:
                            # Create user using session state
                            success, message = create_user(signup_name.strip(), signup_email.lower().strip(), signup_password)
                            
                            if success:
                                # Automatically authenticate the new user
                                st.session_state.authenticated = True
                                st.session_state.user_name = signup_name.strip()
                                st.session_state.user_email = signup_email.lower().strip()
                                
                                st.success("🎉 Account created successfully! Welcome to AspirePath!")
                                st.balloons()
                                st.rerun()  # Refresh to show authenticated menu
                            else:
                                st.error(f"❌ {message}")
                        except Exception as e:
                            st.error(f"❌ An error occurred while creating your account. Please try again.")
    
    # Force styling with JavaScript
    st.markdown("""
    <script>
    // Force dark styling on all elements
    setTimeout(function() {
        const elements = document.querySelectorAll('*');
        elements.forEach(el => {
            if (el.style) {
                if (el.style.backgroundColor === 'white' || el.style.backgroundColor === '#ffffff' || 
                    el.style.backgroundColor === 'rgb(255, 255, 255)') {
                    el.style.backgroundColor = 'transparent';
                }
                if (el.style.color === 'black' || el.style.color === '#000000' || 
                    el.style.color === 'rgb(0, 0, 0)') {
                    el.style.color = 'white';
                }
            }
        });
    }, 100);
    </script>
    </div>
    """, unsafe_allow_html=True)

# Home Section - Clean and properly formatted
if page_clean == "Home":
    # Show personalized content for authenticated users
    if st.session_state.authenticated:
        st.markdown(f"""
        <div style="text-align: center; padding: 2rem; background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(20px); border-radius: 20px; margin: 2rem 0; border: 1px solid rgba(255,255,255,0.2);">
            <h2 style="color: white; margin-bottom: 1rem;">Welcome back, {st.session_state.user_name}! 🎉</h2>
            <p style="color: rgba(255,255,255,0.9); font-size: 1.1rem;">Ready to continue your career journey? Explore the tools available to advance your skills.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Hero section with clean HTML
    st.markdown("""
    <div style="text-align: center; padding: 4rem 2rem; background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(20px); border-radius: 30px; margin: 2rem 0; border: 1px solid rgba(255,255,255,0.2); box-shadow: 0 25px 50px rgba(0, 0, 0, 0.1), inset 0 1px 0 rgba(255, 255, 255, 0.2);">
        <div style="font-size: 4rem; margin-bottom: 1.5rem;">🌟</div>
        <h1 style="font-size: 3.2rem; margin-bottom: 1.5rem; background: linear-gradient(45deg, #ffd700, #ffed4e, #fff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800;">Transform Your Career Journey</h1>
        <p style="font-size: 1.5rem; color: white; margin-bottom: 1rem; font-weight: 300;">Discover your potential, build your skills, achieve your dreams</p>
        <p style="font-size: 1.1rem; color: rgba(255,255,255,0.9); margin-bottom: 2.5rem;">Start your personalized career development journey today</p>
        <div style="display: flex; justify-content: center; gap: 1.5rem; flex-wrap: wrap;">
            <div style="background: rgba(255,255,255,0.15); padding: 0.75rem 1.5rem; border-radius: 25px; color: #ffd700; font-weight: 600;">✨ AI-Powered</div>
            <div style="background: rgba(255,255,255,0.15); padding: 0.75rem 1.5rem; border-radius: 25px; color: #ffd700; font-weight: 600;">🎯 Personalized</div>
            <div style="background: rgba(255,255,255,0.15); padding: 0.75rem 1.5rem; border-radius: 25px; color: #ffd700; font-weight: 600;">🚀 Results-Driven</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Feature cards with simplified HTML
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: rgba(255,255,255,0.1); border-radius: 20px; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2);">
            <div style="font-size: 3.5rem; margin-bottom: 1.5rem;">🎯</div>
            <h3 style="color: white; margin-bottom: 1rem; font-size: 1.4rem; font-weight: 600;">Personalized Guidance</h3>
            <p style="color: rgba(255,255,255,0.9); font-size: 1rem; line-height: 1.6;">Get tailored career roadmaps based on your skills and aspirations</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: rgba(255,255,255,0.1); border-radius: 20px; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2);">
            <div style="font-size: 3.5rem; margin-bottom: 1.5rem;">📊</div>
            <h3 style="color: white; margin-bottom: 1rem; font-size: 1.4rem; font-weight: 600;">Skill Assessment</h3>
            <p style="color: rgba(255,255,255,0.9); font-size: 1rem; line-height: 1.6;">Take comprehensive quizzes to identify your strengths and improvement areas</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: rgba(255,255,255,0.1); border-radius: 20px; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2);">
            <div style="font-size: 3.5rem; margin-bottom: 1.5rem;">📈</div>
            <h3 style="color: white; margin-bottom: 1rem; font-size: 1.4rem; font-weight: 600;">Progress Tracking</h3>
            <p style="color: rgba(255,255,255,0.9); font-size: 1rem; line-height: 1.6;">Monitor your learning journey with detailed analytics and insights</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Add spacing
    st.markdown("<br><br>", unsafe_allow_html=True)

    # Why Choose AspirePath section - simplified
    st.markdown("""
    <div style="background: rgba(255,255,255,0.95); padding: 2rem; border-radius: 15px; margin: 2rem 0; color: #333;">
        <h2 style="text-align: center; margin-bottom: 2rem; color: #333;">🌟 Why Choose AspirePath?</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem;">
            <div style="padding: 1.5rem; background: linear-gradient(135deg, #667eea, #764ba2); color: white; border-radius: 10px; text-align: center;">
                <h4 style="margin-bottom: 1rem;">🎯 AI-Powered Recommendations</h4>
                <p style="margin: 0; font-size: 0.9rem;">Smart algorithms analyze your profile to suggest the best career paths</p>
            </div>
            <div style="padding: 1.5rem; background: linear-gradient(135deg, #f093fb, #f5576c); color: white; border-radius: 10px; text-align: center;">
                <h4 style="margin-bottom: 1rem;">📚 Curated Learning Resources</h4>
                <p style="margin: 0; font-size: 0.9rem;">Access handpicked tutorials, courses, and project ideas</p>
            </div>
            <div style="padding: 1.5rem; background: linear-gradient(135deg, #4facfe, #00f2fe); color: white; border-radius: 10px; text-align: center;">
                <h4 style="margin-bottom: 1rem;">🤝 Peer Comparison</h4>
                <p style="margin: 0; font-size: 0.9rem;">Benchmark your skills against industry standards and peers</p>
            </div>
            <div style="padding: 1.5rem; background: linear-gradient(135deg, #43e97b, #38f9d7); color: white; border-radius: 10px; text-align: center;">
                <h4 style="margin-bottom: 1rem;">📊 Real-time Analytics</h4>
                <p style="margin: 0; font-size: 0.9rem;">Track your progress with detailed insights and visualizations</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # How to get started - simplified
    st.markdown("""
    <div style="background: rgba(255,255,255,0.95); padding: 2rem; border-radius: 15px; margin: 2rem 0; color: #333;">
        <h2 style="text-align: center; margin-bottom: 2rem; color: #333;">📖 How to Get Started</h2>
        <div style="display: flex; justify-content: space-around; flex-wrap: wrap; gap: 2rem;">
            <div style="flex: 1; min-width: 200px; text-align: center;">
                <div style="width: 60px; height: 60px; background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem; color: white; font-size: 1.5rem; font-weight: bold;">1</div>
                <h4 style="color: #333; margin-bottom: 0.5rem;">Create Account</h4>
                <p style="color: #666; font-size: 0.9rem; margin: 0;">Sign up to start your personalized career journey</p>
            </div>
            <div style="flex: 1; min-width: 200px; text-align: center;">
                <div style="width: 60px; height: 60px; background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem; color: white; font-size: 1.5rem; font-weight: bold;">2</div>
                <h4 style="color: #333; margin-bottom: 0.5rem;">Assess Skills</h4>
                <p style="color: #666; font-size: 0.9rem; margin: 0;">Upload your resume or take our skill assessment quiz</p>
            </div>
            <div style="flex: 1; min-width: 200px; text-align: center;">
                <div style="width: 60px; height: 60px; background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem; color: white; font-size: 1.5rem; font-weight: bold;">3</div>
                <h4 style="color: #333; margin-bottom: 0.5rem;">Get Roadmap</h4>
                <p style="color: #666; font-size: 0.9rem; margin: 0;">Receive a personalized learning path to your goals</p>
            </div>
            <div style="flex: 1; min-width: 200px; text-align: center;">
                <div style="width: 60px; height: 60px; background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem; color: white; font-size: 1.5rem; font-weight: bold;">4</div>
                <h4 style="color: #333; margin-bottom: 0.5rem;">Track Progress</h4>
                <p style="color: #666; font-size: 0.9rem; margin: 0;">Monitor your growth and celebrate achievements</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Call to action
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea, #764ba2); padding: 3rem; border-radius: 20px; text-align: center; margin: 3rem 0;">
        <h2 style="color: white; margin-bottom: 1rem;">Ready to Transform Your Career?</h2>
        <p style="color: rgba(255,255,255,0.9); font-size: 1.1rem; margin-bottom: 2rem;">Start your personalized career development journey with AspirePath</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get Started button
    if not st.session_state.authenticated:
        # Create a centered button using columns
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # Custom styled button
            st.markdown("""
            <style>
            .get-started-btn {
                background: linear-gradient(45deg, #ff6b6b, #ee5a52);
                color: white;
                padding: 1rem 2rem;
                border: none;
                border-radius: 25px;
                font-size: 1.1rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 8px 25px rgba(255, 107, 107, 0.3);
                text-align: center;
                display: block;
                width: 100%;
                margin: 1rem 0;
            }
            .get-started-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 12px 35px rgba(255, 107, 107, 0.4);
            }
            </style>
            """, unsafe_allow_html=True)
            
            if st.button("🚀 Get Started Today", use_container_width=True, type="primary", key="get_started_home"):
                # Set redirect flag and rerun to go to login page
                st.session_state.redirect_to_login = True
                st.rerun()
                
                # Add visual arrow pointing to sidebar
                st.markdown("""
                <div style="background: linear-gradient(135deg, #4facfe, #00f2fe); padding: 1.5rem; border-radius: 15px; margin: 1rem 0; position: relative;">
                    <div style="text-align: center;">
                        <h3 style="color: white; margin-bottom: 1rem;">� Next Step: Create Your Account</h3>
                        <p style="color: white; margin-bottom: 1rem; font-size: 1.1rem;">Click on <strong>"Log In / Sign Up"</strong> in the sidebar to:</p>
                        <div style="text-align: left; max-width: 300px; margin: 0 auto;">
                            <p style="color: white; margin: 0.5rem 0;">✨ Create your free account</p>
                            <p style="color: white; margin: 0.5rem 0;">🎯 Get personalized recommendations</p>
                            <p style="color: white; margin: 0.5rem 0;">📊 Access all career tools</p>
                            <p style="color: white; margin: 0.5rem 0;">🚀 Start your journey today</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.balloons()
                
                # Add blinking arrow animation pointing to sidebar
                st.markdown("""
                <style>
                @keyframes blink {
                    0%, 50% { opacity: 1; }
                    51%, 100% { opacity: 0.3; }
                }
                .arrow-pointer {
                    font-size: 2rem;
                    animation: blink 1.5s infinite;
                    color: #ff6b6b;
                    text-align: center;
                    margin: 1rem 0;
                }
                </style>
                <div class="arrow-pointer">👈 Look to the left sidebar!</div>
                """, unsafe_allow_html=True)
    else:
        # For authenticated users, show different message
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div style="background: rgba(72, 187, 120, 0.2); padding: 1.5rem; border-radius: 15px; text-align: center; margin-top: -2rem; border: 2px solid rgba(72, 187, 120, 0.3);">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🎉</div>
                <h3 style="color: #48bb78; margin-bottom: 0.5rem;">Welcome back!</h3>
                <p style="color: #2d3748; margin: 0; font-weight: 500;">You're all set! Explore the tools in the sidebar to advance your career.</p>
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
    if not st.session_state.authenticated:
        st.error("🔒 Please log in to access this feature.")
        st.info("👉 Use the 'Log In / Sign Up' page to create an account or sign in.")
        st.stop()
        
    st.header("📄 Upload Resume & Take Skill Quiz")
    st.markdown("Upload your resume to extract skills automatically, or enter them manually to take a customized quiz.")

    # Initialize user_skills
    user_skills = []
    
    # Create two columns for better layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📄 Resume Upload")
        uploaded_file = st.file_uploader(
            "Upload your resume (PDF or DOCX)", 
            type=["pdf", "docx"],
            help="Upload a PDF or Word document to automatically extract your skills"
        )

        if uploaded_file:
            try:
                with st.spinner("Analyzing your resume..."):
                    resume_text = parse_resume(uploaded_file)
                    user_skills = assess_skills(resume_text)
                    
                if user_skills:
                    st.success(f"✅ Successfully extracted {len(user_skills)} skills from your resume!")
                    
                    # Display extracted skills in an organized way
                    with st.expander("📋 View Extracted Skills"):
                        skills_display = ", ".join(user_skills)
                        st.markdown(f"**Detected Skills:** {skills_display}")
                else:
                    st.warning("⚠️ No skills could be extracted from your resume. Please try manual entry.")
                    
            except Exception as e:
                st.error(f"❌ Error processing resume: {str(e)}")
                st.info("Please try uploading a different file or use manual skill entry.")

    with col2:
        st.subheader("✏️ Manual Entry")
        manual_input = st.text_area(
            "Enter your skills (one per line or comma-separated):",
            placeholder="Python\nSQL\nData Analysis\nMachine Learning",
            help="List your technical skills to get relevant quiz questions"
        )
        
        if manual_input:
            # Handle both comma-separated and line-separated input
            if ',' in manual_input:
                manual_skills = [skill.strip() for skill in manual_input.split(",") if skill.strip()]
            else:
                manual_skills = [skill.strip() for skill in manual_input.split("\n") if skill.strip()]
            
            if manual_skills:
                user_skills = manual_skills  # Override resume skills if manual entry is provided
                st.success(f"✅ Using {len(user_skills)} manually entered skills!")
                
                with st.expander("📋 View Entered Skills"):
                    skills_display = ", ".join(user_skills)
                    st.markdown(f"**Your Skills:** {skills_display}")

    # Skill Quiz Section
    if user_skills:
        st.markdown("---")
        st.subheader("🧠 Skill Assessment Quiz")
        st.info(f"📊 Ready to test your knowledge in: **{', '.join(user_skills[:5])}**" + 
                ("..." if len(user_skills) > 5 else ""))

        # Try to fetch questions
        try:
            with st.spinner("Preparing your personalized quiz..."):
                questions = fetch_questions_from_api(user_skills)

            if not questions:
                st.warning("⚠️ Unable to generate quiz questions for your skills. Please try with different skills.")
                st.info("💡 **Tip:** Try using common technical skills like 'Python', 'JavaScript', 'SQL', etc.")
            else:
                st.success(f"📝 Generated {len(questions)} questions based on your skills!")
                
                # Add a reset quiz button if there are existing answers
                existing_answers = any(f"quiz_q_{q['id']}" in st.session_state for q in questions)
                if existing_answers:
                    if st.button("🔄 Reset Quiz", help="Clear all answers and start over"):
                        for question in questions:
                            key = f"quiz_q_{question['id']}"
                            if key in st.session_state:
                                del st.session_state[key]
                        st.rerun()
                
                # Quiz form
                with st.form("skill_quiz_form"):
                    st.info("💡 **Important:** Please answer all questions before submitting the quiz.")
                    
                    # Add progress tracking
                    if any(f"quiz_q_{q['id']}" in st.session_state for q in questions):
                        answered_count = sum(1 for q in questions if f"quiz_q_{q['id']}" in st.session_state and st.session_state[f"quiz_q_{q['id']}"] is not None)
                        progress = answered_count / len(questions)
                        st.progress(progress)
                        st.caption(f"Progress: {answered_count}/{len(questions)} questions answered")
                    
                    for idx, question in enumerate(questions, 1):
                        st.markdown(f"### Question {idx}")
                        st.markdown(f"**{question['question']}**")
                        
                        # Create radio button with unique key
                        st.radio(
                            "Select your answer:",
                            options=question['options'],
                            key=f"quiz_q_{question['id']}",
                            index=None  # No default selection
                        )
                        st.markdown("---")

                    quiz_submitted = st.form_submit_button("🎯 Submit Quiz", use_container_width=True)

                # Process quiz results
                if quiz_submitted:
                    # Collect answers from session state after form submission
                    user_answers = {}
                    for question in questions:
                        key = f"quiz_q_{question['id']}"
                        if key in st.session_state:
                            user_answers[question['id']] = st.session_state[key]
                        else:
                            user_answers[question['id']] = None
                    
                    # Debug information (can be removed later)
                    # st.write("Debug - User answers:", {k: v for k, v in user_answers.items() if v is not None})
                    
                    # Check if all questions are answered
                    unanswered = [i+1 for i, q in enumerate(questions) if user_answers.get(q['id']) is None]
                    
                    if unanswered:
                        st.error(f"❌ Please answer all questions before submitting!")
                        
                        # Show specific questions that need answers
                        missing_questions = []
                        for i, q in enumerate(questions):
                            if user_answers.get(q['id']) is None:
                                missing_questions.append(f"Question {i+1}: {q['question'][:50]}...")
                        
                        st.warning("� **Missing answers for:**")
                        for missing in missing_questions:
                            st.write(f"• {missing}")
                            
                        # Show which questions are answered vs unanswered
                        answered_count = len([q for q in questions if user_answers.get(q['id']) is not None])
                        st.info(f"📊 **Progress:** {answered_count}/{len(questions)} questions answered")
                        st.info("🔄 Please scroll up, answer the missing questions, and submit again.")
                    else:
                        # Calculate score
                        score = sum(1 for q in questions if user_answers.get(q['id']) == q['answer'])
                        total = len(questions)
                        percentage = (score / total) * 100
                        wrong_qs = [q for q in questions if user_answers.get(q['id']) != q['answer']]

                        # Get current user info
                        current_user = st.session_state.get('user_email', 'unknown@example.com')
                        current_name = st.session_state.get('user_name', 'Unknown User')

                        # Store quiz results in database
                        try:
                            quiz_data = {
                                "score": score,
                                "total": total,
                                "percentage": percentage,
                                "skills_tested": user_skills,
                                "wrong_answers": len(wrong_qs),
                                "quiz_type": "skill_assessment"
                            }
                            
                            store_quiz_results(current_user, quiz_data)
                            
                            # Also store as progress achievement
                            achievement_data = {
                                "category": "Assessment",
                                "description": f"Completed skill quiz with {percentage:.1f}% score",
                                "skills": user_skills,
                                "time_spent": 0.5,  # Estimated time
                                "quiz_score": percentage
                            }
                            store_progress_achievement(current_user, current_name, achievement_data)
                            
                        except Exception as e:
                            st.warning(f"Results calculated but couldn't save to database: {str(e)}")

                        # Display results with nice formatting
                        st.balloons()
                        
                        # Results summary
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Score", f"{score}/{total}")
                        with col2:
                            st.metric("Percentage", f"{percentage:.1f}%")
                        with col3:
                            if percentage >= 80:
                                st.metric("Grade", "🎉 Excellent!")
                            elif percentage >= 60:
                                st.metric("Grade", "👍 Good!")
                            else:
                                st.metric("Grade", "📚 Keep Learning!")

                        # Detailed feedback
                        if wrong_qs:
                            st.subheader("� Review & Learn")
                            st.info("Here are the questions you missed. Review them to improve your understanding!")
                            
                            for idx, q in enumerate(wrong_qs, 1):
                                with st.expander(f"Question {idx}: {q['question'][:50]}..."):
                                    st.markdown(f"**Question:** {q['question']}")
                                    st.markdown(f"❌ **Your Answer:** {user_answers.get(q['id'])}")
                                    st.markdown(f"✅ **Correct Answer:** {q['answer']}")
                                    
                                    # Add learning suggestion
                                    skill = q.get('skill', 'this topic')
                                    st.markdown(f"💡 **Tip:** Review {skill} concepts to improve your understanding.")
                        else:
                            st.success("🎊 Perfect score! You've mastered these skills!")
                            
        except Exception as e:
            st.error(f"❌ Error generating quiz: {str(e)}")
            st.info("Please try again or contact support if the issue persists.")
            
    else:
        # No skills available - show guidance
        st.markdown("---")
        st.subheader("🚀 Get Started")
        st.info("📋 **Upload your resume** or **enter your skills manually** above to begin your skill assessment!")
        
        # Show sample skills for guidance
        with st.expander("💡 Not sure what skills to enter? See examples"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**Programming:**")
                st.markdown("• Python\n• JavaScript\n• Java\n• C++")
                
            with col2:
                st.markdown("**Data & Analytics:**")
                st.markdown("• SQL\n• Excel\n• Tableau\n• Power BI")
                
            with col3:
                st.markdown("**Other Technical:**")
                st.markdown("• HTML/CSS\n• Git\n• Docker\n• AWS")

elif page_clean == "Career Roadmap":
    if not st.session_state.authenticated:
        st.error("🔒 Please log in to access this feature.")
        st.info("👉 Use the 'Log In / Sign Up' page to create an account or sign in.")
        st.stop()
        
    st.header("🎯 Choose Your Career Goal")
    st.markdown("Enter your current skills to get a personalized career roadmap and learning path.")

    # Input for user skills
    user_input_skills = st.text_input(
        "Enter your skills (comma-separated):",
        placeholder="e.g., Python, SQL, Excel, JavaScript",
        help="List your current technical skills separated by commas"
    )

    if user_input_skills and user_input_skills.strip():
        try:
            # Process user skills
            user_skills = [skill.strip() for skill in user_input_skills.split(",") if skill.strip()]
            
            if not user_skills:
                st.warning("Please enter at least one valid skill.")
                st.stop()
            
            # Predict career goal
            predicted_career = predict_career(user_skills)
            
            # Get all career matches for transparency
            career_matches = get_career_matches(user_skills)
            
            # Display primary recommendation
            st.success(f"🔮 **Top Recommended Career Path:** {predicted_career}")
            
            # Show alternative career matches
            if career_matches:
                st.subheader("🎯 Career Path Analysis")
                
                # Filter out careers with very low scores
                relevant_matches = {career: score for career, score in career_matches.items() if score > 5}
                
                if len(relevant_matches) > 1:
                    st.info("📊 **Alternative Career Paths Based on Your Skills:**")
                    
                    # Create columns for better layout
                    for i, (career, score) in enumerate(list(relevant_matches.items())[:5]):  # Show top 5
                        match_percentage = min(100, score)  # Cap at 100%
                        
                        # Color coding based on match percentage
                        if match_percentage >= 50:
                            color = "🟢"  # Green for high match
                        elif match_percentage >= 25:
                            color = "🟡"  # Yellow for medium match
                        else:
                            color = "🔵"  # Blue for lower match
                        
                        if career == predicted_career:
                            st.markdown(f"**{color} {career}** - {match_percentage:.1f}% match ⭐ **(Recommended)**")
                        else:
                            st.markdown(f"{color} {career} - {match_percentage:.1f}% match")
                
                st.markdown("---")
            
            # Generate roadmap
            roadmap, all_required = generate_roadmap(user_skills, predicted_career)
            
            if roadmap:
                st.subheader("📚 Your Learning Roadmap")
                st.info(f"Based on your current skills, here are the areas to focus on for {predicted_career}:")
                
                # Display roadmap steps
                for idx, step in enumerate(roadmap, start=1):
                    st.markdown(f"**{idx}.** {step}")
                
                # Show progress
                skills_learned = len(all_required) - len(roadmap)
                total_skills = len(all_required)
                progress = skills_learned / total_skills if total_skills > 0 else 0
                
                st.subheader("� Your Progress")
                st.progress(progress)
                st.write(f"You have {skills_learned} out of {total_skills} required skills ({progress:.1%} complete)")
                
            else:
                st.success("🎉 Congratulations! You already have all the required skills for this career path!")
                st.balloons()
            
            # Generate YouTube resources for missing skills
            if roadmap:
                st.subheader("🎥 Recommended Learning Resources")
                
                for step in roadmap[:3]:  # Show resources for first 3 skills
                    skill_name = step.replace("Learn ", "").strip()
                    st.markdown(f"**📖 {skill_name} Resources:**")
                    
                    try:
                        resources = fetch_youtube_resources(skill_name, max_results=3)
                        for resource in resources:
                            st.markdown(f"- [{resource['title']}]({resource['url']})")
                            st.caption(resource['description'])
                    except Exception as e:
                        st.warning(f"Could not load resources for {skill_name}")
                
                # Additional course recommendations
                st.subheader("📘 Recommended Courses")
                courses = [
                    {"title": "Python for Everybody", "platform": "Coursera", "url": "https://www.coursera.org/specializations/python"},
                    {"title": "SQL Fundamentals", "platform": "Codecademy", "url": "https://www.codecademy.com/learn/learn-sql"},
                    {"title": "Data Analysis with Python", "platform": "freeCodeCamp", "url": "https://www.freecodecamp.org/learn/data-analysis-with-python/"},
                    {"title": "Web Development Bootcamp", "platform": "Udemy", "url": "https://www.udemy.com/course/the-web-developer-bootcamp/"},
                    {"title": "Machine Learning Course", "platform": "Coursera", "url": "https://www.coursera.org/learn/machine-learning"}
                ]
                
                for course in courses:
                    st.markdown(f"- **{course['title']}** ({course['platform']}) - [Learn More]({course['url']})")
            
        except Exception as e:
            st.error(f"An error occurred while generating your roadmap: {str(e)}")
            st.info("Please try again with different skills or contact support if the issue persists.")
    
    elif user_input_skills is not None and user_input_skills.strip() == "":
        st.warning("Please enter your skills to generate a personalized career roadmap.")
    
    # Add helpful tips
    if not user_input_skills:
        st.markdown("---")
        st.subheader("💡 How it works:")
        st.markdown("""
        1. **Enter your skills** - List your current technical abilities
        2. **Get career prediction** - Our AI suggests the best career path
        3. **Follow the roadmap** - Learn missing skills step by step
        4. **Track progress** - Monitor your learning journey
        """)
        
        st.subheader("🎯 Supported Career Paths:")
        career_paths = ["Data Analyst", "Web Developer", "ML Engineer", "Cybersecurity Analyst", "AI Engineer", "Software Developer", "Game Developer"]
        cols = st.columns(2)
        for i, career in enumerate(career_paths):
            with cols[i % 2]:
                st.markdown(f"• {career}")

elif page_clean == "Peer Comparison":
    if not st.session_state.authenticated:
        st.error("🔒 Please log in to access this feature.")
        st.info("👉 Use the 'Log In / Sign Up' page to create an account or sign in.")
        st.stop()
        
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
    if not st.session_state.authenticated:
        st.error("🔒 Please log in to access this feature.")
        st.info("👉 Use the 'Log In / Sign Up' page to create an account or sign in.")
        st.stop()
        
    st.header("📈 Weekly Progress Tracker")
    st.markdown(f"Welcome back, **{st.session_state.user_name}**! Track your learning journey here.")

    # Create two columns for better layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Input for weekly achievements
        st.subheader("🏆 Log Your Weekly Achievements")
        
        # Category selection
        achievement_category = st.selectbox(
            "Select Achievement Category:",
            ["Course Completed", "Project Built", "Skill Learned", "Certification Earned", "Book Read", "Other"]
        )
        
        # Achievement description
        achievement_description = st.text_area(
            "Describe your achievement:",
            placeholder="e.g., Completed Python for Data Science course on Coursera",
            help="Be specific about what you accomplished this week"
        )
        
        # Skills involved
        skills_involved = st.text_input(
            "Skills used/learned (comma-separated):",
            placeholder="e.g., Python, Pandas, Data Visualization",
            help="List the technical skills related to this achievement"
        )
        
        # Time spent
        time_spent = st.number_input(
            "Hours spent this week:",
            min_value=0.0,
            max_value=168.0,
            value=0.0,
            step=0.5,
            help="How many hours did you dedicate to this achievement?"
        )
        
        # Difficulty level
        difficulty = st.select_slider(
            "Difficulty Level:",
            options=["Beginner", "Intermediate", "Advanced", "Expert"],
            value="Intermediate"
        )

        if st.button("📝 Submit Achievement", type="primary"):
            if achievement_description.strip():
                try:
                    # Process skills
                    skills_list = [skill.strip() for skill in skills_involved.split(",") if skill.strip()] if skills_involved else []
                    
                    # Create achievement data
                    from datetime import datetime
                    achievement_data = {
                        "user_id": st.session_state.user_email,
                        "user_name": st.session_state.user_name,
                        "date": datetime.now(),
                        "week": datetime.now().strftime("%Y-W%U"),
                        "category": achievement_category,
                        "description": achievement_description.strip(),
                        "skills": skills_list,
                        "time_spent": time_spent,
                        "difficulty": difficulty,
                        "created_at": datetime.now()
                    }
                    
                    # Store using session state
                    success = store_progress_achievement(
                        st.session_state.user_email, 
                        st.session_state.user_name, 
                        achievement_data
                    )
                    
                    if success:
                        st.success("🎉 Achievement logged successfully!")
                        st.balloons()
                        # Clear form
                        st.rerun()
                    else:
                        st.error("❌ Error saving achievement. Please try again.")
                    
                except Exception as e:
                    st.error(f"❌ Error saving achievement: {str(e)}")
            else:
                st.warning("⚠️ Please describe your achievement before submitting.")
    
    with col2:
        # Quick stats
        st.subheader("📊 Your Stats")
        try:
            # Get user progress from session state
            progress_stats = get_user_progress_stats(st.session_state.user_email)
            user_achievements = progress_stats["achievements"]
            
            if user_achievements:
                total_achievements = len(user_achievements)
                total_hours = sum([ach.get("time_spent", 0) for ach in user_achievements])
                unique_skills = set()
                for ach in user_achievements:
                    unique_skills.update(ach.get("skills", []))
                
                st.metric("Total Achievements", total_achievements)
                st.metric("Hours Logged", f"{total_hours:.1f}")
                st.metric("Skills Practiced", len(unique_skills))
                
                # Category breakdown
                categories = {}
                for ach in user_achievements:
                    cat = ach.get("category", "Other")
                    categories[cat] = categories.get(cat, 0) + 1
                
                st.markdown("**Categories:**")
                for cat, count in categories.items():
                    st.write(f"• {cat}: {count}")
            else:
                st.info("No achievements logged yet. Start tracking your progress!")
                
        except Exception as e:
            st.error(f"Error loading stats: {str(e)}")

    # Recent achievements
    st.subheader("📝 Recent Achievements")
    try:
        # Get recent achievements from session state
        progress_stats = get_user_progress_stats(st.session_state.user_email)
        all_achievements = progress_stats["achievements"]
        
        # Sort by date and get recent 5
        recent_achievements = sorted(all_achievements, key=lambda x: x.get("date", ""), reverse=True)[:5]
        
        if recent_achievements:
            for i, achievement in enumerate(recent_achievements):
                with st.expander(f"🏆 {achievement.get('category', 'Achievement')} - {achievement.get('date', 'Unknown').strftime('%Y-%m-%d') if hasattr(achievement.get('date'), 'strftime') else str(achievement.get('date', 'Unknown'))}"):
                    st.write(f"**Description:** {achievement.get('description', 'No description')}")
                    if achievement.get('skills'):
                        st.write(f"**Skills:** {', '.join(achievement.get('skills', []))}")
                    st.write(f"**Time Spent:** {achievement.get('time_spent', 0)} hours")
                    st.write(f"**Difficulty:** {achievement.get('difficulty', 'Unknown')}")
        else:
            st.info("No achievements found. Log your first achievement above!")
            
    except Exception as e:
        st.error(f"Error loading achievements: {str(e)}")

    # Suggestions based on achievements
    st.subheader("💡 Personalized Suggestions")
    try:
        if recent_achievements:
            # Analyze recent achievements for suggestions
            recent_skills = set()
            recent_categories = set()
            
            for ach in recent_achievements[:3]:  # Last 3 achievements
                recent_skills.update(ach.get('skills', []))
                recent_categories.add(ach.get('category', ''))
            
            suggestions = []
            
            if 'Python' in recent_skills:
                suggestions.append("🐍 Try building a web application with Flask or Django")
                suggestions.append("📊 Explore data science with Pandas and Matplotlib")
            
            if 'JavaScript' in recent_skills:
                suggestions.append("⚛️ Learn React or Vue.js for frontend development")
                suggestions.append("🟢 Explore Node.js for backend development")
            
            if 'Course Completed' in recent_categories:
                suggestions.append("🛠️ Apply your learning by building a practical project")
                suggestions.append("🏆 Consider pursuing a relevant certification")
            
            if 'Project Built' in recent_categories:
                suggestions.append("📱 Deploy your project to showcase your skills")
                suggestions.append("🔄 Iterate and improve your existing projects")
            
            # Default suggestions
            if not suggestions:
                suggestions = [
                    "📚 Set a goal to learn one new skill this week",
                    "🎯 Choose a project that challenges your current abilities",
                    "👥 Connect with other learners in your field",
                    "📝 Document your learning journey in a blog or portfolio"
                ]
            
            for suggestion in suggestions[:4]:  # Show max 4 suggestions
                st.markdown(f"• {suggestion}")
        else:
            st.markdown("""
            **Get started with these suggestions:**
            • 📚 Set a weekly learning goal
            • 🎯 Choose a skill you want to develop
            • 📝 Document your progress regularly
            • 🏆 Celebrate small wins along the way
            """)
            
    except Exception as e:
        st.error(f"Error generating suggestions: {str(e)}")

# Progress Dashboard Section
if page_clean == "Progress Dashboard":
    if not st.session_state.authenticated:
        st.error("🔒 Please log in to access this feature.")
        st.info("👉 Use the 'Log In / Sign Up' page to create an account or sign in.")
        st.stop()
        
    st.header("📊 Progress Dashboard")
    st.markdown(f"Comprehensive progress overview for **{st.session_state.user_name}**")

    # Get user's progress data from session state
    progress_stats = get_user_progress_stats(st.session_state.user_email)
    user_achievements = progress_stats["achievements"]
    
    try:        
        if not user_achievements:
            st.info("📝 No progress data found. Start logging your achievements in the Progress Tracker!")
            st.markdown("### 🚀 Get Started")
            st.markdown("Visit the **Progress Tracker** page to log your first achievement and unlock your personalized dashboard!")
        else:
            # Import for charts
            import pandas as pd
            import altair as alt
            from datetime import datetime, timedelta
            
            # Overall Statistics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Achievements", len(user_achievements))
            
            with col2:
                total_hours = sum([ach.get("time_spent", 0) for ach in user_achievements])
                st.metric("Hours Invested", f"{total_hours:.1f}")
            
            with col3:
                unique_skills = set()
                for ach in user_achievements:
                    unique_skills.update(ach.get("skills", []))
                st.metric("Skills Practiced", len(unique_skills))
            
            with col4:
                # Calculate streak (consecutive weeks with achievements)
                weeks_with_achievements = set()
                for ach in user_achievements:
                    if 'week' in ach:
                        weeks_with_achievements.add(ach['week'])
                st.metric("Active Weeks", len(weeks_with_achievements))
            
            # Time-based Analysis
            st.subheader("📈 Progress Over Time")
            
            # Prepare data for charts
            df_data = []
            for ach in user_achievements:
                date = ach.get('date')
                if hasattr(date, 'strftime'):
                    week = date.strftime('%Y-W%U')
                    df_data.append({
                        'Week': week,
                        'Date': date,
                        'Category': ach.get('category', 'Other'),
                        'Hours': ach.get('time_spent', 0),
                        'Skills_Count': len(ach.get('skills', [])),
                        'Difficulty': ach.get('difficulty', 'Intermediate')
                    })
            
            if df_data:
                df = pd.DataFrame(df_data)
                
                # Weekly hours chart
                weekly_hours = df.groupby('Week')['Hours'].sum().reset_index()
                if len(weekly_hours) > 1:
                    hours_chart = alt.Chart(weekly_hours).mark_line(point=True, color='#667eea').encode(
                        x=alt.X('Week:O', title='Week'),
                        y=alt.Y('Hours:Q', title='Hours Spent'),
                        tooltip=['Week', 'Hours']
                    ).properties(width=700, height=300, title="Weekly Learning Hours")
                    st.altair_chart(hours_chart, use_container_width=True)
                
                # Category breakdown
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📊 Achievement Categories")
                    category_counts = df['Category'].value_counts().reset_index()
                    category_counts.columns = ['Category', 'Count']
                    
                    category_chart = alt.Chart(category_counts).mark_arc(innerRadius=50).encode(
                        theta=alt.Theta(field="Count", type="quantitative"),
                        color=alt.Color(field="Category", type="nominal", scale=alt.Scale(scheme='category10')),
                        tooltip=['Category', 'Count']
                    ).properties(width=300, height=300)
                    st.altair_chart(category_chart)
                
                with col2:
                    st.subheader("🎯 Difficulty Distribution")
                    difficulty_counts = df['Difficulty'].value_counts().reset_index()
                    difficulty_counts.columns = ['Difficulty', 'Count']
                    
                    difficulty_chart = alt.Chart(difficulty_counts).mark_bar().encode(
                        x=alt.X('Difficulty:O', sort=['Beginner', 'Intermediate', 'Advanced', 'Expert']),
                        y='Count:Q',
                        color=alt.Color('Difficulty:O', scale=alt.Scale(scheme='viridis')),
                        tooltip=['Difficulty', 'Count']
                    ).properties(width=300, height=300)
                    st.altair_chart(difficulty_chart)
            
            # Skills Analysis
            st.subheader("🧠 Skills Development")
            if unique_skills:
                # Skills frequency
                skill_counts = {}
                for ach in user_achievements:
                    for skill in ach.get('skills', []):
                        skill_counts[skill] = skill_counts.get(skill, 0) + 1
                
                # Top skills
                top_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:10]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Most Practiced Skills:**")
                    for skill, count in top_skills:
                        st.write(f"• {skill}: {count} times")
                
                with col2:
                    if len(top_skills) > 0:
                        skills_df = pd.DataFrame(top_skills, columns=['Skill', 'Count'])
                        skills_chart = alt.Chart(skills_df).mark_bar(color='#764ba2').encode(
                            x=alt.X('Count:Q'),
                            y=alt.Y('Skill:N', sort='-x'),
                            tooltip=['Skill', 'Count']
                        ).properties(width=400, height=300, title="Top Skills")
                        st.altair_chart(skills_chart)
            
            # Recent Activity
            st.subheader("🕒 Recent Activity")
            recent_achievements = sorted(user_achievements, key=lambda x: x.get('date', datetime.min), reverse=True)[:5]
            
            for ach in recent_achievements:
                date_str = ach.get('date', 'Unknown date')
                if hasattr(date_str, 'strftime'):
                    date_str = date_str.strftime('%B %d, %Y')
                
                with st.expander(f"🏆 {ach.get('category', 'Achievement')} - {date_str}"):
                    st.write(f"**Description:** {ach.get('description', 'No description')}")
                    if ach.get('skills'):
                        st.write(f"**Skills:** {', '.join(ach.get('skills', []))}")
                    st.write(f"**Time Spent:** {ach.get('time_spent', 0)} hours")
                    st.write(f"**Difficulty:** {ach.get('difficulty', 'Unknown')}")
            
            # Goals and Recommendations
            st.subheader("🎯 Insights & Recommendations")
            
            # Calculate learning velocity
            if len(user_achievements) > 1:
                days_active = (max([ach.get('date', datetime.min) for ach in user_achievements]) - 
                             min([ach.get('date', datetime.min) for ach in user_achievements])).days
                if days_active > 0:
                    achievements_per_week = len(user_achievements) / (days_active / 7)
                    st.success(f"📈 You're averaging {achievements_per_week:.1f} achievements per week!")
            
            # Personalized recommendations
            recent_categories = [ach.get('category', '') for ach in recent_achievements[:3]]
            recent_skills = set()
            for ach in recent_achievements[:3]:
                recent_skills.update(ach.get('skills', []))
            
            recommendations = []
            if 'Course Completed' in recent_categories:
                recommendations.append("🛠️ Consider building a project to apply your new knowledge")
            if 'Project Built' in recent_categories:
                recommendations.append("📱 Share your project on GitHub or LinkedIn")
            if len(recent_skills) < 3:
                recommendations.append("🌟 Try learning a complementary skill to broaden your expertise")
            
            if recommendations:
                st.markdown("**Personalized Recommendations:**")
                for rec in recommendations:
                    st.write(f"• {rec}")
            
    except Exception as e:
        st.error(f"Error loading dashboard data: {str(e)}")
        st.info("Please check your Progress Tracker for logged achievements.")
