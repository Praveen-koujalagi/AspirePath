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

st.set_page_config(
    page_title="AspirePath - Your Career Journey Starts Here",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Simplified CSS to avoid white screen issues
st.markdown(
    """
    <style>
    /* Basic styling to ensure visibility */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        color: white;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 15px;
        font-weight: 600;
        width: 100%;
    }
    
    .stTextInput > div > div > input {
        background: white !important;
        color: black !important;
        border-radius: 10px !important;
    }
    
    /* Ensure text is visible */
    h1, h2, h3, p, div {
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True
)

# Test content to ensure visibility
st.title("🚀 AspirePath")
st.write("Career Development Platform")

# Simple sidebar
with st.sidebar:
    st.markdown("### Navigation")
    
    if st.session_state.authenticated:
        page = option_menu(
            menu_title=None,
            options=["Home", "Skills", "Roadmap", "Logout"],
            icons=["house", "gear", "map", "box-arrow-right"],
            default_index=0,
        )
    else:
        page = option_menu(
            menu_title=None,
            options=["Home", "Login"],
            icons=["house", "person"],
            default_index=0,
        )

# Main content based on page selection
if page == "Home":
    st.header("Welcome to AspirePath! 🌟")
    st.write("Transform your career journey with personalized guidance.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("🎯 **Personalized Guidance**\n\nGet tailored career roadmaps")
    
    with col2:
        st.info("📊 **Skill Assessment**\n\nTake comprehensive quizzes")
    
    with col3:
        st.info("📈 **Progress Tracking**\n\nMonitor your learning journey")

elif page == "Login" and not st.session_state.authenticated:
    st.header("Login to AspirePath")
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        st.subheader("Welcome Back!")
        
        login_email = st.text_input("Email", key="login_email")
        login_password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login"):
            if login_email and login_password:
                result, user_data = authenticate_user(login_email, login_password)
                if result:
                    st.session_state.authenticated = True
                    st.session_state.user_name = user_data.get('name', 'User')
                    st.session_state.user_email = login_email
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")
            else:
                st.error("Please fill in all fields")
    
    with tab2:
        st.subheader("Create Your Account")
        
        signup_name = st.text_input("Full Name", key="signup_name")
        signup_email = st.text_input("Email", key="signup_email")
        signup_password = st.text_input("Password", type="password", key="signup_password")
        
        if st.button("Sign Up"):
            if signup_name and signup_email and signup_password:
                # Validate inputs
                if not validate_name(signup_name):
                    st.error("Invalid name")
                elif not validate_email(signup_email):
                    st.error("Invalid email")
                elif not validate_password(signup_password):
                    st.error("Password must be at least 6 characters")
                else:
                    success, message = create_user(signup_name, signup_email, signup_password)
                    if success:
                        st.session_state.authenticated = True
                        st.session_state.user_name = signup_name
                        st.session_state.user_email = signup_email
                        st.success("Account created successfully!")
                        st.rerun()
                    else:
                        st.error(f"Error: {message}")
            else:
                st.error("Please fill in all fields")

elif page == "Skills" and st.session_state.authenticated:
    st.header("📊 Skill Assessment")
    st.write("Upload your resume or enter skills to get personalized recommendations.")
    
    # Simple skills input
    skills_input = st.text_area("Enter your skills (comma-separated)", height=100)
    
    if st.button("Assess Skills"):
        if skills_input:
            skills = assess_skills(skills_input)
            st.success(f"Found {len(skills)} skills!")
            
            for skill in skills[:10]:  # Show first 10 skills
                st.write(f"✅ {skill}")

elif page == "Roadmap" and st.session_state.authenticated:
    st.header("🗺️ Career Roadmap")
    
    goal = st.selectbox("Select your career goal:", [
        "Data Analyst", "Web Developer", "ML Engineer", 
        "Cybersecurity Analyst", "AI Engineer", "Software Developer"
    ])
    
    if st.button("Generate Roadmap"):
        roadmap = generate_roadmap([goal])  # Simple roadmap generation
        st.success("Roadmap generated!")
        st.write(roadmap)

elif page == "Logout" and st.session_state.authenticated:
    st.header("Logout")
    if st.button("Confirm Logout"):
        st.session_state.authenticated = False
        st.session_state.user_name = ""
        st.session_state.user_email = ""
        st.success("Logged out successfully!")
        st.rerun()

# Show authentication prompt for protected pages
if not st.session_state.authenticated and page in ["Skills", "Roadmap"]:
    st.warning("Please login to access this feature.")
    st.info("Use the 'Login' option in the sidebar to get started.")
