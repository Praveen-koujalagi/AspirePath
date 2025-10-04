import os
import re
import streamlit as st
from PyPDF2 import PdfReader
from docx import Document
import hashlib
from datetime import datetime

# Session State Database Setup
@st.cache_resource
def init_session_state_db():
    """Initialize session state collections for data storage"""
    try:
        if 'users' not in st.session_state or st.session_state.users is None:
            st.session_state.users = []
            # Add demo users for testing
            demo_password = hashlib.sha256("demo123".encode()).hexdigest()
            demo_users = [
                {
                    "name": "Demo User",
                    "email": "demo@aspirepath.com",
                    "password": demo_password,
                    "created_at": datetime.now().isoformat()
                },
                {
                    "name": "Test User",
                    "email": "test@aspirepath.com", 
                    "password": demo_password,
                    "created_at": datetime.now().isoformat()
                }
            ]
            st.session_state.users.extend(demo_users)
        if 'resumes' not in st.session_state:
            st.session_state.resumes = []
        if 'skills' not in st.session_state:
            st.session_state.skills = []
        if 'quiz_results' not in st.session_state:
            st.session_state.quiz_results = []
        if 'roadmaps' not in st.session_state:
            st.session_state.roadmaps = []
        if 'progress' not in st.session_state:
            st.session_state.progress = []
        return True
    except Exception as e:
        print(f"Error initializing session state: {e}")
        # Force reinitialize with empty lists
        st.session_state.users = []
        st.session_state.resumes = []
        st.session_state.skills = []
        st.session_state.quiz_results = []
        st.session_state.roadmaps = []
        st.session_state.progress = []
        return False

# Initialize session state database
init_session_state_db()

def parse_resume(file):
    """Parse resume and store in session state with enhanced error handling"""
    try:
        text = ""
        file_type = file.name.split(".")[-1].lower()

        if file_type == "pdf":
            reader = PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
        elif file_type == "docx":
            doc = Document(file)
            for para in doc.paragraphs:
                if para.text.strip():
                    text += para.text + "\n"
        elif file_type == "txt":
            text = file.read().decode("utf-8")
        else:
            raise ValueError(f"Unsupported file format: {file_type}")

        if not text.strip():
            raise ValueError("No text content could be extracted from the file")

        # Ensure session state is properly initialized
        init_session_state_db()
        
        # Ensure resumes list exists and is properly initialized
        if 'resumes' not in st.session_state or st.session_state.resumes is None:
            st.session_state.resumes = []

        # Store the parsed resume in session state
        resume_data = {
            "file_name": file.name, 
            "content": text.strip(),
            "uploaded_at": datetime.now().isoformat(),
            "file_size": len(text),
            "file_type": file_type
        }
        
        st.session_state.resumes.append(resume_data)
        return text.strip()
        
    except Exception as e:
        # Enhanced error handling with specific error messages
        error_msg = f"Error processing resume: {str(e)}"
        print(error_msg)  # For debugging
        
        # Initialize session state if needed
        try:
            init_session_state_db()
            if 'resumes' not in st.session_state:
                st.session_state.resumes = []
        except:
            pass
            
        # Return a user-friendly error message
        if "Collection objects do not implement truth value" in str(e):
            raise ValueError("Database connection error. Please try uploading a different file or use manual skill entry.")
        elif "No text content" in str(e):
            raise ValueError("Could not extract text from this file. Please ensure the file contains readable text.")
        else:
            raise ValueError(f"File processing error: {str(e)}")

@st.cache_data
def fetch_youtube_resources(goal, skills=[], max_results=5):
    """
    Generates smart YouTube search links based on user goal and skills.
    Enhanced with better search query generation and caching.
    """
    # Create more targeted search queries
    queries = []
    
    # Primary query with goal
    base_query = f"{goal} tutorial complete course 2024"
    queries.append(base_query)
    
    # Skill-specific queries
    if skills:
        for skill in skills[:2]:  # Use top 2 skills
            skill_query = f"{skill} for {goal} beginners tutorial"
            queries.append(skill_query)
    
    # Generate search URLs
    search_urls = []
    for i, query in enumerate(queries[:max_results]):
        clean_query = query.strip().replace(' ', '+')
        url = f"https://www.youtube.com/results?search_query={clean_query}"
        search_urls.append({
            'title': f"🎥 {query.title()}",
            'url': url,
            'description': f"Learn {goal} with practical examples and hands-on tutorials"
        })
    
    return search_urls

def store_quiz_results(user_id, quiz_results):
    """
    Stores the quiz results in session state.

    Args:
        user_id (str): The ID of the user taking the quiz.
        quiz_results (dict): A dictionary containing quiz details (e.g., score, total questions, wrong answers).

    Returns:
        bool: True if stored successfully, False otherwise
    """
    try:
        init_session_state_db()
        
        # Prepare the complete quiz record
        quiz_record = {
            "user_id": user_id,
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().strftime("%Y-%m-%d"),
            **quiz_results  # Merge in the provided quiz data
        }
        
        # Add to session state
        st.session_state.quiz_results.append(quiz_record)
        return True
        
    except Exception as e:
        print(f"Error storing quiz results: {e}")
        return False

def store_roadmap(user_id, career_goal, roadmap):
    """
    Stores the generated roadmap in session state.

    Args:
        user_id (str): The ID of the user.
        career_goal (str): The career goal specified by the user.
        roadmap (list): A list of steps in the roadmap.

    Returns:
        None
    """
    init_session_state_db()
    
    roadmap_data = {
        "user_id": user_id, 
        "career_goal": career_goal, 
        "roadmap": roadmap,
        "created_at": datetime.now().isoformat()
    }
    st.session_state.roadmaps.append(roadmap_data)

def validate_email(email):
    """
    Validates email format using regex pattern.
    
    Args:
        email (str): Email address to validate
        
    Returns:
        bool: True if email is valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """
    Validates password strength.
    
    Args:
        password (str): Password to validate
        
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    
    return True, ""

def validate_name(name):
    """
    Validates name format.
    
    Args:
        name (str): Name to validate
        
    Returns:
        bool: True if name is valid, False otherwise
    """
    return len(name.strip()) >= 2 and name.replace(' ', '').isalpha()

def store_progress_achievement(user_email, user_name, achievement_data):
    """
    Stores a progress achievement in session state.
    
    Args:
        user_email (str): User's email address
        user_name (str): User's display name
        achievement_data (dict): Achievement details including category, description, skills, etc.
        
    Returns:
        bool: True if stored successfully, False otherwise
    """
    try:
        init_session_state_db()
        
        # Prepare the complete achievement record
        achievement_record = {
            "user_id": user_email,
            "user_name": user_name,
            "date": datetime.now().isoformat(),
            "week": datetime.now().strftime("%Y-W%U"),
            "created_at": datetime.now().isoformat(),
            **achievement_data  # Merge in the provided achievement data
        }
        
        # Add to session state
        st.session_state.progress.append(achievement_record)
        return True
        
    except Exception as e:
        print(f"Error storing achievement: {e}")
        return False

def get_user_progress_stats(user_email):
    """
    Retrieves progress statistics for a specific user from session state.
    
    Args:
        user_email (str): User's email address
        
    Returns:
        dict: Statistics including total achievements, hours, skills, etc.
    """
    try:
        init_session_state_db()
        user_achievements = [p for p in st.session_state.progress if p["user_id"] == user_email]
        
        if not user_achievements:
            return {
                "total_achievements": 0,
                "total_hours": 0,
                "unique_skills": 0,
                "active_weeks": 0,
                "achievements": []
            }
        
        # Calculate statistics
        total_hours = sum([ach.get("time_spent", 0) for ach in user_achievements])
        
        unique_skills = set()
        for ach in user_achievements:
            unique_skills.update(ach.get("skills", []))
        
        weeks_with_achievements = set()
        for ach in user_achievements:
            if 'week' in ach:
                weeks_with_achievements.add(ach['week'])
        
        return {
            "total_achievements": len(user_achievements),
            "total_hours": total_hours,
            "unique_skills": len(unique_skills),
            "active_weeks": len(weeks_with_achievements),
            "achievements": user_achievements,
            "skill_list": list(unique_skills)
        }
        
    except Exception as e:
        print(f"Error retrieving progress stats: {e}")
        return {
            "total_achievements": 0,
            "total_hours": 0,
            "unique_skills": 0,
            "active_weeks": 0,
            "achievements": []
        }

# Session State User Management Functions
def create_user(name, email, password):
    """Create a new user in session state"""
    try:
        init_session_state_db()
        
        # Ensure users list exists and is not None
        if 'users' not in st.session_state or st.session_state.users is None:
            st.session_state.users = []
            init_session_state_db()
        
        # Check if user already exists
        for user in st.session_state.users:
            if isinstance(user, dict) and "email" in user:
                if user["email"] == email:
                    return False, "User already exists"
        
        # Hash password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # Create user record
        user_data = {
            "name": name,
            "email": email,
            "password": hashed_password,
            "created_at": datetime.now().isoformat()
        }
        
        st.session_state.users.append(user_data)
        return True, "User created successfully"
    except Exception as e:
        # Log error and reinitialize session state
        print(f"Error in create_user: {e}")
        st.session_state.users = []
        init_session_state_db()
        return False, "Error creating user"

def authenticate_user(email, password):
    """Authenticate user login from session state"""
    try:
        init_session_state_db()
        
        # Ensure users list exists and is not None
        if 'users' not in st.session_state or st.session_state.users is None:
            st.session_state.users = []
            init_session_state_db()
            return None
        
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        for user in st.session_state.users:
            # Check if user is a dictionary and has required keys
            if isinstance(user, dict) and "email" in user and "password" in user:
                if user["email"] == email and user["password"] == hashed_password:
                    return user
        return None
    except Exception as e:
        # Log error and reinitialize session state
        print(f"Error in authenticate_user: {e}")
        st.session_state.users = []
        init_session_state_db()
        return None

def find_user_by_email(email):
    """Find user by email in session state"""
    try:
        init_session_state_db()
        
        # Ensure users list exists and is not None
        if 'users' not in st.session_state or st.session_state.users is None:
            st.session_state.users = []
            return None
            
        for user in st.session_state.users:
            # Check if user is a dictionary and has email key
            if isinstance(user, dict) and "email" in user:
                if user["email"] == email:
                    return user
        return None
    except Exception as e:
        # Log error and reinitialize session state
        print(f"Error in find_user_by_email: {e}")
        st.session_state.users = []
        init_session_state_db()
        return None

# Session State Database Statistics (for debugging)
def get_session_stats():
    """Get statistics about session state database"""
    init_session_state_db()
    
    return {
        "total_users": len(st.session_state.users),
        "total_resumes": len(st.session_state.resumes),
        "total_quiz_results": len(st.session_state.quiz_results),
        "total_roadmaps": len(st.session_state.roadmaps),
        "total_progress_entries": len(st.session_state.progress)
    }
