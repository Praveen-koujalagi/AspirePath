# 📁 JSON Database Alternative for Streamlit Cloud Deployment

import json
import os
import hashlib
from datetime import datetime
import streamlit as st

class JSONDatabase:
    """
    Simple JSON-based database alternative for Streamlit Cloud deployment
    This replaces MongoDB functionality with local JSON file storage
    """
    
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        # Create data directory if it doesn't exist
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Initialize empty files if they don't exist
        self._init_collections()
    
    def _init_collections(self):
        """Initialize JSON files for different collections"""
        collections = ["users", "quiz_results", "roadmaps", "progress"]
        for collection in collections:
            file_path = os.path.join(self.data_dir, f"{collection}.json")
            if not os.path.exists(file_path):
                self._save_json(file_path, [])
    
    def _load_json(self, file_path):
        """Load data from JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _save_json(self, file_path, data):
        """Save data to JSON file"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
    
    # User Management
    def create_user(self, name, email, password):
        """Create a new user"""
        users_file = os.path.join(self.data_dir, "users.json")
        users = self._load_json(users_file)
        
        # Check if user already exists
        if any(user["email"] == email for user in users):
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
        
        users.append(user_data)
        self._save_json(users_file, users)
        return True, "User created successfully"
    
    def authenticate_user(self, email, password):
        """Authenticate user login"""
        users_file = os.path.join(self.data_dir, "users.json")
        users = self._load_json(users_file)
        
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        for user in users:
            if user["email"] == email and user["password"] == hashed_password:
                return user
        return None
    
    def find_user_by_email(self, email):
        """Find user by email"""
        users_file = os.path.join(self.data_dir, "users.json")
        users = self._load_json(users_file)
        
        for user in users:
            if user["email"] == email:
                return user
        return None
    
    # Quiz Results
    def save_quiz_results(self, user_id, quiz_data):
        """Save quiz results"""
        quiz_file = os.path.join(self.data_dir, "quiz_results.json")
        results = self._load_json(quiz_file)
        
        quiz_record = {
            "user_id": user_id,
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().strftime("%Y-%m-%d"),
            **quiz_data
        }
        
        results.append(quiz_record)
        self._save_json(quiz_file, results)
        return True
    
    def get_user_quiz_results(self, user_id):
        """Get quiz results for a user"""
        quiz_file = os.path.join(self.data_dir, "quiz_results.json")
        results = self._load_json(quiz_file)
        
        return [result for result in results if result["user_id"] == user_id]
    
    # Roadmaps
    def save_roadmap(self, user_id, career_goal, roadmap):
        """Save career roadmap"""
        roadmap_file = os.path.join(self.data_dir, "roadmaps.json")
        roadmaps = self._load_json(roadmap_file)
        
        roadmap_record = {
            "user_id": user_id,
            "career_goal": career_goal,
            "roadmap": roadmap,
            "created_at": datetime.now().isoformat()
        }
        
        roadmaps.append(roadmap_record)
        self._save_json(roadmap_file, roadmaps)
        return True
    
    def get_user_roadmaps(self, user_id):
        """Get roadmaps for a user"""
        roadmap_file = os.path.join(self.data_dir, "roadmaps.json")
        roadmaps = self._load_json(roadmap_file)
        
        return [roadmap for roadmap in roadmaps if roadmap["user_id"] == user_id]
    
    # Progress Tracking
    def save_progress(self, user_id, user_name, achievement_data):
        """Save progress achievement"""
        progress_file = os.path.join(self.data_dir, "progress.json")
        progress_data = self._load_json(progress_file)
        
        achievement_record = {
            "user_id": user_id,
            "user_name": user_name,
            "date": datetime.now().isoformat(),
            "week": datetime.now().strftime("%Y-W%U"),
            "created_at": datetime.now().isoformat(),
            **achievement_data
        }
        
        progress_data.append(achievement_record)
        self._save_json(progress_file, progress_data)
        return True
    
    def get_user_progress(self, user_id):
        """Get progress data for a user"""
        progress_file = os.path.join(self.data_dir, "progress.json")
        progress_data = self._load_json(progress_file)
        
        user_progress = [p for p in progress_data if p["user_id"] == user_id]
        
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

# Initialize the JSON database
@st.cache_resource
def get_json_database():
    """Get cached JSON database instance"""
    return JSONDatabase()

# Usage Example:
# db = get_json_database()
# db.create_user("John Doe", "john@email.com", "password123")
# user = db.authenticate_user("john@email.com", "password123")
