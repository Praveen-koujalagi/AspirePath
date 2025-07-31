from config import SKILL_TEMPLATES
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize MongoDB client and collection (optional for deployment)
try:
    from pymongo import MongoClient
    client = MongoClient("mongodb://localhost:27017/")
    db = client["skills_database"]
    skills_collection = db["skills"]
    MONGODB_AVAILABLE = True
except Exception as e:
    print(f"MongoDB not available: {e}")
    MONGODB_AVAILABLE = False
    skills_collection = None

# Predefined career goals and their associated skills (comprehensive and inclusive)
CAREER_SKILLS = {
    "Data Analyst": "Excel, SQL, Python, Tableau, Statistics, Power BI, Data Analysis, Analytics, R, SPSS, Data Visualization, Pandas, NumPy",
    "Web Developer": "HTML, CSS, JavaScript, React, Node.js, MongoDB, Angular, Vue, Frontend, Backend, Web Development, Bootstrap, jQuery",
    "ML Engineer": "Python, NumPy, Pandas, Scikit-learn, Deep Learning, Machine Learning, TensorFlow, PyTorch, Data Science, Statistics",
    "Cybersecurity Analyst": "Network Security, Cryptography, Firewalls, Linux, Ethical Hacking, Penetration Testing, Security Analysis, Cybersecurity",
    "AI Engineer": "Python, TensorFlow, PyTorch, Machine Learning, Neural Networks, Artificial Intelligence, Deep Learning, NLP, Computer Vision",
    "Software Developer": "C++, Java, Python, Data Structures, Algorithms, Programming, Software Development, C#, .NET, Object-Oriented Programming",
    "Game Developer": "C++, Unity, Unreal Engine, Game Physics, 3D Modeling, Game Development, C#, Graphics Programming, Animation"
}

def assess_skills(text):
    found = []
    for skills in SKILL_TEMPLATES.values():
        found += [skill for skill in skills if skill.lower() in text.lower()]
    # Store the extracted skills in the database (if available)
    if MONGODB_AVAILABLE and skills_collection:
        try:
            skills_collection.insert_one({"text": text, "skills": found})
        except Exception as e:
            print(f"Failed to store skills in database: {e}")
    return list(set(found))

def select_goal():
    return list(SKILL_TEMPLATES.keys())

def generate_roadmap(user_skills, goal):
    required = SKILL_TEMPLATES.get(goal, [])
    missing = list(set(required) - set(user_skills))
    roadmap = [f"Learn {skill}" for skill in missing]
    return roadmap, required

def predict_career(user_skills):
    """
    Predicts the most suitable career goal based on user skills using improved matching.

    Args:
        user_skills (list): List of skills provided by the user.

    Returns:
        str: Predicted career goal.
    """
    if not user_skills:
        return "Generalist"
    
    # Normalize user skills for better matching
    normalized_user_skills = [skill.strip().lower() for skill in user_skills]
    
    career_scores = {}
    
    # Calculate scores for each career path
    for career, skills_str in CAREER_SKILLS.items():
        career_skills = [skill.strip().lower() for skill in skills_str.split(",")]
        
        # Count exact matches
        exact_matches = 0
        partial_matches = 0
        
        for user_skill in normalized_user_skills:
            # Check for exact matches
            if user_skill in career_skills:
                exact_matches += 2  # Weight exact matches higher
            else:
                # Check for partial matches (contains)
                for career_skill in career_skills:
                    if user_skill in career_skill or career_skill in user_skill:
                        partial_matches += 1
                        break
        
        # Calculate total score (exact matches weighted more heavily)
        total_score = exact_matches + (partial_matches * 0.5)
        
        # Normalize by career requirements (careers with fewer requirements get slight boost)
        normalized_score = total_score / len(career_skills) * 100
        
        career_scores[career] = normalized_score
    
    # Find the best matching career
    if not career_scores or max(career_scores.values()) == 0:
        # Fallback: try keyword-based matching
        return predict_career_by_keywords(normalized_user_skills)
    
    best_career = max(career_scores, key=career_scores.get)
    best_score = career_scores[best_career]
    
    # If the best score is very low, return Generalist
    if best_score < 10:  # Threshold for minimum relevance
        return "Generalist"
    
    return best_career

def get_career_matches(user_skills):
    """
    Gets all career matches with scores for transparency.
    
    Args:
        user_skills (list): List of skills provided by the user.
        
    Returns:
        dict: Career matches with scores
    """
    if not user_skills:
        return {}
    
    # Normalize user skills for better matching
    normalized_user_skills = [skill.strip().lower() for skill in user_skills]
    
    career_scores = {}
    
    # Calculate scores for each career path
    for career, skills_str in CAREER_SKILLS.items():
        career_skills = [skill.strip().lower() for skill in skills_str.split(",")]
        
        # Count exact matches
        exact_matches = 0
        partial_matches = 0
        
        for user_skill in normalized_user_skills:
            # Check for exact matches
            if user_skill in career_skills:
                exact_matches += 2  # Weight exact matches higher
            else:
                # Check for partial matches (contains)
                for career_skill in career_skills:
                    if user_skill in career_skill or career_skill in user_skill:
                        partial_matches += 1
                        break
        
        # Calculate total score (exact matches weighted more heavily)
        total_score = exact_matches + (partial_matches * 0.5)
        
        # Normalize by career requirements (careers with fewer requirements get slight boost)
        normalized_score = total_score / len(career_skills) * 100
        
        career_scores[career] = normalized_score
    
    # Sort by score (highest first)
    sorted_careers = sorted(career_scores.items(), key=lambda x: x[1], reverse=True)
    
    return dict(sorted_careers)

def predict_career_by_keywords(normalized_user_skills):
    """
    Fallback function to predict career based on keyword patterns.
    
    Args:
        normalized_user_skills (list): Normalized user skills
        
    Returns:
        str: Predicted career goal
    """
    # Define keyword patterns for each career
    career_keywords = {
        "Data Analyst": ["excel", "sql", "tableau", "power bi", "statistics", "data", "analytics", "powerbi"],
        "Web Developer": ["html", "css", "javascript", "react", "angular", "vue", "web", "frontend", "backend", "node"],
        "ML Engineer": ["machine learning", "ml", "numpy", "pandas", "scikit", "sklearn", "data science"],
        "AI Engineer": ["ai", "artificial intelligence", "tensorflow", "pytorch", "neural", "deep learning"],
        "Cybersecurity Analyst": ["security", "cyber", "network", "firewall", "encryption", "hacking", "penetration"],
        "Software Developer": ["java", "c++", "programming", "algorithms", "data structures", "software", "development"],
        "Game Developer": ["unity", "unreal", "game", "gaming", "3d", "physics", "graphics"]
    }
    
    career_scores = {}
    
    for career, keywords in career_keywords.items():
        score = 0
        for user_skill in normalized_user_skills:
            for keyword in keywords:
                if keyword in user_skill or user_skill in keyword:
                    score += 1
                    break
        career_scores[career] = score
    
    if max(career_scores.values()) > 0:
        return max(career_scores, key=career_scores.get)
    
    return "Software Developer"  # Default fallback
