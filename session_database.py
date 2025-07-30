# 🧠 Session State Database Alternative for Streamlit Cloud

import streamlit as st
import hashlib
from datetime import datetime

class SessionStateDatabase:
    """
    Complete database replacement using Streamlit Session State
    Perfect for demos and quick deployments without external dependencies
    
    ⚠️ Note: Data is lost when user refreshes the page or closes browser
    """
    
    def __init__(self):
        self._init_session_state()
    
    def _init_session_state(self):
        """Initialize all session state collections if they don't exist"""
        if 'users' not in st.session_state:
            st.session_state.users = []
        if 'quiz_results' not in st.session_state:
            st.session_state.quiz_results = []
        if 'roadmaps' not in st.session_state:
            st.session_state.roadmaps = []
        if 'progress' not in st.session_state:
            st.session_state.progress = []
        if 'resumes' not in st.session_state:
            st.session_state.resumes = []
    
    # User Management
    def create_user(self, name, email, password):
        """Create a new user in session state"""
        self._init_session_state()
        
        # Check if user already exists
        if any(user["email"] == email for user in st.session_state.users):
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
    
    def authenticate_user(self, email, password):
        """Authenticate user login"""
        self._init_session_state()
        
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        for user in st.session_state.users:
            if user["email"] == email and user["password"] == hashed_password:
                return user
        return None
    
    def find_user_by_email(self, email):
        """Find user by email"""
        self._init_session_state()
        
        for user in st.session_state.users:
            if user["email"] == email:
                return user
        return None
    
    # Quiz Results
    def save_quiz_results(self, user_id, quiz_data):
        """Save quiz results to session state"""
        self._init_session_state()
        
        quiz_record = {
            "user_id": user_id,
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().strftime("%Y-%m-%d"),
            **quiz_data
        }
        
        st.session_state.quiz_results.append(quiz_record)
        return True
    
    def get_user_quiz_results(self, user_id):
        """Get quiz results for a user"""
        self._init_session_state()
        
        return [result for result in st.session_state.quiz_results if result["user_id"] == user_id]
    
    # Roadmaps
    def save_roadmap(self, user_id, career_goal, roadmap):
        """Save career roadmap to session state"""
        self._init_session_state()
        
        roadmap_record = {
            "user_id": user_id,
            "career_goal": career_goal,
            "roadmap": roadmap,
            "created_at": datetime.now().isoformat()
        }
        
        st.session_state.roadmaps.append(roadmap_record)
        return True
    
    def get_user_roadmaps(self, user_id):
        """Get roadmaps for a user"""
        self._init_session_state()
        
        return [roadmap for roadmap in st.session_state.roadmaps if roadmap["user_id"] == user_id]
    
    # Progress Tracking
    def save_progress(self, user_id, user_name, achievement_data):
        """Save progress achievement to session state"""
        self._init_session_state()
        
        achievement_record = {
            "user_id": user_id,
            "user_name": user_name,
            "date": datetime.now().isoformat(),
            "week": datetime.now().strftime("%Y-W%U"),
            "created_at": datetime.now().isoformat(),
            **achievement_data
        }
        
        st.session_state.progress.append(achievement_record)
        return True
    
    def get_user_progress(self, user_id):
        """Get progress data for a user"""
        self._init_session_state()
        
        user_progress = [p for p in st.session_state.progress if p["user_id"] == user_id]
        
        if not user_progress:
            return {
                "total_achievements": 0,
                "total_hours": 0,
                "unique_skills": 0,
                "active_weeks": 0,
                "achievements": []
            }
        
        # Calculate statistics
        total_hours = sum([p.get("time_spent", 0) for p in user_progress])
        
        unique_skills = set()
        for p in user_progress:
            unique_skills.update(p.get("skills", []))
        
        weeks_with_achievements = set()
        for p in user_progress:
            if 'week' in p:
                weeks_with_achievements.add(p['week'])
        
        return {
            "total_achievements": len(user_progress),
            "total_hours": total_hours,
            "unique_skills": len(unique_skills),
            "active_weeks": len(weeks_with_achievements),
            "achievements": user_progress,
            "skill_list": list(unique_skills)
        }
    
    # Resume Storage
    def save_resume(self, file_name, content):
        """Save resume content to session state"""
        self._init_session_state()
        
        resume_record = {
            "file_name": file_name,
            "content": content,
            "uploaded_at": datetime.now().isoformat()
        }
        
        st.session_state.resumes.append(resume_record)
        return True
    
    def get_all_resumes(self):
        """Get all uploaded resumes"""
        self._init_session_state()
        return st.session_state.resumes
    
    # Utility Functions
    def clear_all_data(self):
        """Clear all data from session state (useful for testing)"""
        st.session_state.users = []
        st.session_state.quiz_results = []
        st.session_state.roadmaps = []
        st.session_state.progress = []
        st.session_state.resumes = []
    
    def get_database_stats(self):
        """Get statistics about the session state database"""
        self._init_session_state()
        
        return {
            "total_users": len(st.session_state.users),
            "total_quiz_results": len(st.session_state.quiz_results),
            "total_roadmaps": len(st.session_state.roadmaps),
            "total_progress_entries": len(st.session_state.progress),
            "total_resumes": len(st.session_state.resumes)
        }
    
    def export_session_data(self):
        """Export all session data (useful for debugging)"""
        self._init_session_state()
        
        return {
            "users": st.session_state.users,
            "quiz_results": st.session_state.quiz_results,
            "roadmaps": st.session_state.roadmaps,
            "progress": st.session_state.progress,
            "resumes": st.session_state.resumes
        }

# Initialize the session state database
@st.cache_resource
def get_session_database():
    """Get cached session state database instance"""
    return SessionStateDatabase()

# Example Usage:
"""
# In your main app.py, replace MongoDB calls with:

from session_database import get_session_database

# Initialize database
db = get_session_database()

# User operations
success, message = db.create_user("John Doe", "john@email.com", "password123")
user = db.authenticate_user("john@email.com", "password123")

# Quiz operations
db.save_quiz_results("john@email.com", {"score": 85, "total": 100})
results = db.get_user_quiz_results("john@email.com")

# Progress tracking
db.save_progress("john@email.com", "John Doe", {
    "category": "Learning",
    "description": "Completed Python course",
    "skills": ["Python", "Programming"],
    "time_spent": 5
})

# Get statistics
stats = db.get_database_stats()
st.write(f"Total users: {stats['total_users']}")
"""
