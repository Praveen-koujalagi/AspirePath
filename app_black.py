import streamlit as st
from streamlit_option_menu import option_menu

# Page config
st.set_page_config(
    page_title="AspirePath",
    page_icon="🚀",
    layout="wide"
)

# Force black background and white text
st.markdown("""
<style>
    .main {
        background-color: black !important;
        color: white !important;
    }
    
    .block-container {
        background-color: black !important;
        color: white !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: gold !important;
    }
    
    p, div, span {
        color: white !important;
    }
    
    .stButton > button {
        background-color: #333 !important;
        color: white !important;
        border: 2px solid gold !important;
    }
    
    .stTextInput > div > div > input {
        background-color: #333 !important;
        color: white !important;
        border: 1px solid #666 !important;
    }
    
    .stTextInput label {
        color: gold !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Simple header
st.markdown("# 🚀 AspirePath")
st.markdown("## Your Career Development Platform")

# Simple sidebar
with st.sidebar:
    st.markdown("### Navigation")
    
    if st.session_state.authenticated:
        selected = option_menu(
            menu_title=None,
            options=["Home", "Skills", "Profile", "Logout"],
            icons=["house", "gear", "person", "box-arrow-right"],
            default_index=0,
        )
    else:
        selected = option_menu(
            menu_title=None,
            options=["Home", "Login"],
            icons=["house", "person"],
            default_index=0,
        )

# Main content
if selected == "Home":
    st.header("Welcome to AspirePath! 🌟")
    st.write("Transform your career journey with personalized guidance.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🎯 Personalized Guidance**
        
        Get tailored career roadmaps based on your skills and goals.
        """)
    
    with col2:
        st.markdown("""
        **📊 Skill Assessment**
        
        Take comprehensive quizzes to identify strengths and areas for improvement.
        """)
    
    with col3:
        st.markdown("""
        **📈 Progress Tracking**
        
        Monitor your learning journey with detailed analytics.
        """)

elif selected == "Login" and not st.session_state.authenticated:
    st.header("🔐 Login to AspirePath")
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        st.subheader("Welcome Back!")
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        
        if st.button("Login", key="login_btn"):
            if email and password:
                # Simple demo login
                if email == "demo@aspirepath.com" and password == "demo123":
                    st.session_state.authenticated = True
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid credentials. Try: demo@aspirepath.com / demo123")
            else:
                st.error("Please enter both email and password")
    
    with tab2:
        st.subheader("Create Account")
        name = st.text_input("Full Name")
        signup_email = st.text_input("Email", key="signup_email")
        signup_password = st.text_input("Password", type="password", key="signup_password")
        
        if st.button("Sign Up", key="signup_btn"):
            if name and signup_email and signup_password:
                st.session_state.authenticated = True
                st.success("Account created successfully!")
                st.rerun()
            else:
                st.error("Please fill in all fields")

elif selected == "Skills" and st.session_state.authenticated:
    st.header("📊 Skill Assessment")
    
    st.write("Enter your skills to get personalized recommendations:")
    skills_text = st.text_area("Your Skills (comma-separated)", 
                               placeholder="Python, JavaScript, Data Analysis, etc.")
    
    if st.button("Analyze Skills"):
        if skills_text:
            skills = [skill.strip() for skill in skills_text.split(",")]
            st.success(f"Found {len(skills)} skills!")
            
            st.subheader("Your Skills:")
            for skill in skills:
                st.write(f"✅ {skill}")
        else:
            st.error("Please enter some skills")

elif selected == "Profile" and st.session_state.authenticated:
    st.header("👤 User Profile")
    st.write("Manage your profile and preferences")
    
    name = st.text_input("Full Name", value="Demo User")
    email = st.text_input("Email", value="demo@aspirepath.com")
    bio = st.text_area("Bio", value="Aspiring developer")
    
    if st.button("Update Profile"):
        st.success("Profile updated successfully!")

elif selected == "Logout":
    st.header("👋 Logout")
    if st.button("Confirm Logout"):
        st.session_state.authenticated = False
        st.success("Logged out successfully!")
        st.rerun()

# Show login prompt for protected pages
if not st.session_state.authenticated and selected in ["Skills", "Profile"]:
    st.warning("🔒 Please login to access this feature")
    st.info("Use the Login tab in the sidebar. Demo credentials: demo@aspirepath.com / demo123")

# Footer
st.markdown("---")
st.markdown("**AspirePath** - Your journey to career success starts here! 🚀")
