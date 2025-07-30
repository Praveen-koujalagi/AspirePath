import os
import re
import streamlit as st
from PyPDF2 import PdfReader
from docx import Document
from pymongo import MongoClient

# MongoDB connection setup with caching
@st.cache_resource
def init_mongodb_connection():
    """Initialize MongoDB connection with caching for better performance"""
    client = MongoClient("mongodb://localhost:27017/")
    db = client["aspirepath"]
    return db

# Initialize database connection
db = init_mongodb_connection()

# Collections
resumes_collection = db["resumes"]
skills_collection = db["skills"]
quiz_results_collection = db["quiz_results"]
roadmaps_collection = db["roadmaps"]

def parse_resume(file):
    text = ""
    file_type = file.name.split(".")[-1]

    if file_type == "pdf":
        reader = PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    elif file_type == "docx":
        doc = Document(file)
        for para in doc.paragraphs:
            text += para.text
    elif file_type == "txt":
        text = file.read().decode("utf-8")
    else:
        text = "Unsupported file format"

    # Store the parsed resume in the database
    resumes_collection.insert_one({"file_name": file.name, "content": text})
    return text

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
    Stores the quiz results in the MongoDB `quiz_results` collection.

    Args:
        user_id (str): The ID of the user taking the quiz.
        quiz_results (dict): A dictionary containing quiz details (e.g., score, total questions, wrong answers).

    Returns:
        bool: True if stored successfully, False otherwise
    """
    try:
        from datetime import datetime
        
        # Prepare the complete quiz record
        quiz_record = {
            "user_id": user_id,
            "timestamp": datetime.now(),
            "date": datetime.now().strftime("%Y-%m-%d"),
            **quiz_results  # Merge in the provided quiz data
        }
        
        # Insert into database
        result = quiz_results_collection.insert_one(quiz_record)
        return bool(result.inserted_id)
        
    except Exception as e:
        print(f"Error storing quiz results: {e}")
        return False

def store_roadmap(user_id, career_goal, roadmap):
    """
    Stores the generated roadmap in the MongoDB `roadmaps` collection.

    Args:
        user_id (str): The ID of the user.
        career_goal (str): The career goal specified by the user.
        roadmap (list): A list of steps in the roadmap.

    Returns:
        None
    """
    roadmaps_collection.insert_one({"user_id": user_id, "career_goal": career_goal, "roadmap": roadmap})

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
    Stores a progress achievement in the MongoDB progress collection.
    
    Args:
        user_email (str): User's email address
        user_name (str): User's display name
        achievement_data (dict): Achievement details including category, description, skills, etc.
        
    Returns:
        bool: True if stored successfully, False otherwise
    """
    try:
        progress_collection = db["progress"]
        
        from datetime import datetime
        
        # Prepare the complete achievement record
        achievement_record = {
            "user_id": user_email,
            "user_name": user_name,
            "date": datetime.now(),
            "week": datetime.now().strftime("%Y-W%U"),
            "created_at": datetime.now(),
            **achievement_data  # Merge in the provided achievement data
        }
        
        # Insert into database
        result = progress_collection.insert_one(achievement_record)
        return bool(result.inserted_id)
        
    except Exception as e:
        print(f"Error storing achievement: {e}")
        return False

def get_user_progress_stats(user_email):
    """
    Retrieves progress statistics for a specific user.
    
    Args:
        user_email (str): User's email address
        
    Returns:
        dict: Statistics including total achievements, hours, skills, etc.
    """
    try:
        progress_collection = db["progress"]
        user_achievements = list(progress_collection.find({"user_id": user_email}))
        
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
