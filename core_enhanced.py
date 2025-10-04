# 🔧 Enhanced Core Module with ML Integration
from config import SKILL_TEMPLATES
from ml_career_predictor import DynamicCareerPredictor
import numpy as np
from typing import List, Dict, Tuple

# Initialize the ML predictor
ml_predictor = DynamicCareerPredictor()

# Original functionality (preserved for backward compatibility)
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

# Original predefined career skills (kept as fallback)
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
    """Enhanced skill assessment with ML support"""
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
    """Return available career goals (both predefined and ML-discovered)"""
    goals = list(SKILL_TEMPLATES.keys())
    
    # Add ML-discovered careers if available
    try:
        if ml_predictor.is_trained:
            ml_careers = ml_predictor.career_names
            goals.extend([career for career in ml_careers if career not in goals])
    except:
        pass
    
    return goals

def generate_roadmap(user_skills, goal):
    """Enhanced roadmap generation"""
    required = SKILL_TEMPLATES.get(goal, [])
    missing = list(set(required) - set(user_skills))
    roadmap = [f"Learn {skill}" for skill in missing]
    
    # Add ML-enhanced suggestions if available
    try:
        if ml_predictor.is_trained:
            skill_importance = ml_predictor.get_skill_importance(goal)
            if skill_importance:
                important_skills = list(skill_importance.keys())[:5]
                ml_suggestions = [f"Focus on {skill} (High Impact)" for skill in important_skills 
                                if skill not in [s.lower() for s in user_skills]]
                roadmap.extend(ml_suggestions[:3])  # Add top 3 ML suggestions
    except:
        pass
    
    return roadmap, required

def predict_career_ml(user_skills: List[str], use_ml: bool = True) -> Dict:
    """
    Enhanced career prediction using ML algorithms
    
    Args:
        user_skills: List of user skills
        use_ml: Whether to use ML prediction (True) or fallback to rule-based (False)
    
    Returns:
        Dict with prediction results including multiple career options
    """
    if use_ml:
        try:
            # Try ML prediction first
            if not ml_predictor.is_trained:
                ml_predictor.train_models()
            
            ml_predictions = ml_predictor.predict_dynamic_careers(user_skills, top_k=5)
            
            return {
                'method': 'ml',
                'primary_career': ml_predictions[0]['career'] if ml_predictions else 'Generalist',
                'confidence': ml_predictions[0]['confidence'] if ml_predictions else 0,
                'alternative_careers': ml_predictions[1:] if len(ml_predictions) > 1 else [],
                'all_predictions': ml_predictions,
                'diversity_score': len(set(pred['career'] for pred in ml_predictions)) / len(ml_predictions) if ml_predictions else 0
            }
        except Exception as e:
            print(f"ML prediction failed: {e}, falling back to rule-based")
            use_ml = False
    
    if not use_ml:
        # Fallback to original rule-based prediction
        primary_career = predict_career(user_skills)
        alternative_careers = get_career_matches(user_skills)
        
        return {
            'method': 'rule_based',
            'primary_career': primary_career,
            'confidence': 85.7,  # Original system's reported accuracy
            'alternative_careers': list(alternative_careers.keys())[1:4],  # Top 3 alternatives
            'all_predictions': [{'career': career, 'confidence': score} 
                              for career, score in alternative_careers.items()],
            'diversity_score': len(alternative_careers) / 7  # 7 is total predefined careers
        }

def discover_emerging_careers(user_skills: List[str]) -> List[Dict]:
    """
    Discover emerging career paths based on user skills and market trends
    """
    try:
        if not ml_predictor.is_trained:
            ml_predictor.train_models()
        
        new_paths = ml_predictor.discover_new_career_paths()
        
        # Filter paths relevant to user skills
        relevant_paths = []
        user_skills_lower = [skill.lower() for skill in user_skills]
        
        for path in new_paths:
            path_skills_lower = [skill.lower() for skill in path['key_skills']]
            overlap = len(set(user_skills_lower) & set(path_skills_lower))
            
            if overlap >= 2:  # At least 2 skill matches
                path['user_overlap'] = overlap
                path['relevance_score'] = overlap / len(path['key_skills'])
                relevant_paths.append(path)
        
        # Sort by relevance
        relevant_paths.sort(key=lambda x: x['relevance_score'], reverse=True)
        return relevant_paths[:3]  # Top 3 most relevant
        
    except Exception as e:
        print(f"Emerging career discovery failed: {e}")
        return []

def get_skill_gaps(user_skills: List[str], target_career: str) -> Dict:
    """
    Analyze skill gaps for a target career using ML insights
    """
    gaps = {
        'missing_skills': [],
        'recommended_skills': [],
        'skill_importance': {},
        'learning_priority': []
    }
    
    try:
        # Get ML-based skill importance
        if ml_predictor.is_trained:
            skill_importance = ml_predictor.get_skill_importance(target_career)
            gaps['skill_importance'] = skill_importance
            
            # Find missing high-importance skills
            user_skills_lower = [skill.lower() for skill in user_skills]
            for skill, importance in skill_importance.items():
                if not any(skill in user_skill.lower() or user_skill.lower() in skill 
                          for user_skill in user_skills_lower):
                    gaps['missing_skills'].append({
                        'skill': skill,
                        'importance': importance,
                        'priority': 'High' if importance > 0.1 else 'Medium'
                    })
            
            # Sort by importance
            gaps['missing_skills'].sort(key=lambda x: x['importance'], reverse=True)
            gaps['learning_priority'] = gaps['missing_skills'][:5]  # Top 5 priorities
    
    except Exception as e:
        print(f"Skill gap analysis failed: {e}")
        # Fallback to rule-based analysis
        required_skills = SKILL_TEMPLATES.get(target_career, [])
        missing = list(set(required_skills) - set(user_skills))
        gaps['missing_skills'] = [{'skill': skill, 'importance': 0.5, 'priority': 'Medium'} 
                                 for skill in missing]
    
    return gaps

# Original functions (preserved for backward compatibility)
def predict_career(user_skills):
    """Original career prediction function (preserved)"""
    if not user_skills:
        return "Generalist"
    
    normalized_user_skills = [skill.strip().lower() for skill in user_skills]
    career_scores = {}
    
    for career, skills_str in CAREER_SKILLS.items():
        career_skills = [skill.strip().lower() for skill in skills_str.split(",")]
        
        exact_matches = 0
        partial_matches = 0
        
        for user_skill in normalized_user_skills:
            if user_skill in career_skills:
                exact_matches += 2
            else:
                for career_skill in career_skills:
                    if user_skill in career_skill or career_skill in user_skill:
                        partial_matches += 1
                        break
        
        total_score = exact_matches + (partial_matches * 0.5)
        normalized_score = total_score / len(career_skills) * 100
        career_scores[career] = normalized_score
    
    if not career_scores or max(career_scores.values()) == 0:
        return predict_career_by_keywords(normalized_user_skills)
    
    best_career = max(career_scores, key=career_scores.get)
    best_score = career_scores[best_career]
    
    if best_score < 10:
        return "Generalist"
    
    return best_career

def get_career_matches(user_skills):
    """Original career matching function (preserved)"""
    if not user_skills:
        return {}
    
    normalized_user_skills = [skill.strip().lower() for skill in user_skills]
    career_scores = {}
    
    for career, skills_str in CAREER_SKILLS.items():
        career_skills = [skill.strip().lower() for skill in skills_str.split(",")]
        
        exact_matches = 0
        partial_matches = 0
        
        for user_skill in normalized_user_skills:
            if user_skill in career_skills:
                exact_matches += 2
            else:
                for career_skill in career_skills:
                    if user_skill in career_skill or career_skill in user_skill:
                        partial_matches += 1
                        break
        
        total_score = exact_matches + (partial_matches * 0.5)
        normalized_score = total_score / len(career_skills) * 100
        career_scores[career] = normalized_score
    
    sorted_careers = sorted(career_scores.items(), key=lambda x: x[1], reverse=True)
    return dict(sorted_careers)

def predict_career_by_keywords(normalized_user_skills):
    """Original keyword-based prediction (preserved)"""
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
    
    return "Software Developer"