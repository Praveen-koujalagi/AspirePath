# 🧠 SMART QUIZ ENHANCEMENT - Adaptive question selection based on predicted career

import json
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_smart_questions(user_skills, predicted_career=None, path="real_mcq_bank.json", max_questions=10):
    """
    Enhanced question loading with ML-based relevance scoring.
    
    Args:
        user_skills (list): User's current skills
        predicted_career (str): Predicted career path (optional)
        path (str): Path to question bank
        max_questions (int): Maximum questions to return
    
    Returns:
        list: Optimally selected questions based on user profile
    """
    try:
        with open(path, "r", encoding='utf-8') as f:
            all_questions = json.load(f)
        
        if not all_questions:
            return []
        
        # Career-specific skill priorities
        CAREER_SKILL_PRIORITIES = {
            "Data Analyst": ["sql", "python", "excel", "statistics", "tableau", "powerbi"],
            "Web Developer": ["javascript", "html", "css", "react", "node", "mongodb"],
            "ML Engineer": ["python", "machine learning", "tensorflow", "pytorch", "pandas"],
            "AI Engineer": ["python", "tensorflow", "neural networks", "deep learning", "nlp"],
            "Cybersecurity Analyst": ["security", "network", "firewall", "encryption", "linux"],
            "Software Developer": ["java", "python", "algorithms", "data structures", "programming"],
            "Game Developer": ["unity", "c#", "game development", "3d", "physics"]
        }
        
        user_skills_lower = [skill.lower().strip() for skill in user_skills]
        
        # Score each question based on relevance
        scored_questions = []
        
        for question in all_questions:
            question_skill = question.get("skill", "").lower().strip()
            question_text = question.get("question", "").lower()
            
            relevance_score = 0
            
            # 1. Direct skill match (highest priority)
            if any(skill in question_skill or question_skill in skill for skill in user_skills_lower):
                relevance_score += 10
            
            # 2. Career-specific relevance boost
            if predicted_career and predicted_career in CAREER_SKILL_PRIORITIES:
                priority_skills = CAREER_SKILL_PRIORITIES[predicted_career]
                if any(priority_skill in question_skill for priority_skill in priority_skills):
                    relevance_score += 5
            
            # 3. Keyword matching in question text
            keyword_matches = sum(1 for skill in user_skills_lower 
                                if skill in question_text and len(skill) > 2)
            relevance_score += keyword_matches * 2
            
            # 4. Question difficulty alignment (prefer medium difficulty for assessment)
            difficulty = question.get("difficulty", "medium").lower()
            if difficulty == "medium":
                relevance_score += 1
            elif difficulty == "hard":
                relevance_score += 0.5
            
            scored_questions.append({
                **question,
                'relevance_score': relevance_score
            })
        
        # Sort by relevance score
        scored_questions.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        # Select top questions with diversity
        selected_questions = []
        used_skills = set()
        
        # First pass: High relevance questions
        for q in scored_questions:
            if len(selected_questions) >= max_questions:
                break
            
            q_skill = q.get("skill", "").lower()
            if q['relevance_score'] >= 5 and q_skill not in used_skills:
                selected_questions.append(q)
                used_skills.add(q_skill)
        
        # Second pass: Fill remaining slots with diverse questions
        remaining_slots = max_questions - len(selected_questions)
        for q in scored_questions:
            if remaining_slots <= 0:
                break
            
            if q not in selected_questions:
                selected_questions.append(q)
                remaining_slots -= 1
        
        # Shuffle to avoid predictable order
        random.shuffle(selected_questions)
        
        return selected_questions[:max_questions]
        
    except FileNotFoundError:
        print(f"Question bank file not found: {path}")
        return []
    except json.JSONDecodeError:
        print(f"Invalid JSON format in: {path}")
        return []
    except Exception as e:
        print(f"Error loading smart questions: {e}")
        return []

def adaptive_quiz_flow(user_skills, initial_questions_count=10):
    """
    Adaptive quiz that adjusts based on user performance.
    
    Args:
        user_skills (list): User's skills
        initial_questions_count (int): Starting number of questions
    
    Returns:
        dict: Adaptive quiz configuration
    """
    # Predict career first
    from enhanced_prediction import predict_career_enhanced
    prediction_result = predict_career_enhanced(user_skills)
    predicted_career = prediction_result['primary_career']
    
    # Load smart questions
    questions = load_smart_questions(
        user_skills, 
        predicted_career, 
        max_questions=initial_questions_count
    )
    
    # Create adaptive flow
    quiz_config = {
        'questions': questions,
        'predicted_career': predicted_career,
        'confidence': prediction_result['confidence'],
        'adaptive_rules': {
            'extend_quiz': prediction_result['confidence'] < 70,  # More questions if uncertain
            'focus_areas': get_focus_areas(user_skills, predicted_career),
            'difficulty_adjustment': True
        },
        'personalization': {
            'career_focused': True,
            'skill_gap_assessment': True,
            'learning_recommendations': True
        }
    }
    
    return quiz_config

def get_focus_areas(user_skills, predicted_career):
    """Identify areas that need more assessment based on career prediction"""
    
    CAREER_FOCUS_AREAS = {
        "Data Analyst": ["Statistics", "SQL", "Data Visualization", "Excel"],
        "Web Developer": ["JavaScript", "Frontend Frameworks", "Backend Development", "Databases"],
        "ML Engineer": ["Machine Learning Algorithms", "Python Libraries", "Model Deployment", "Statistics"],
        "AI Engineer": ["Deep Learning", "Neural Networks", "Computer Vision", "NLP"],
        "Cybersecurity Analyst": ["Network Security", "Cryptography", "Incident Response", "Risk Assessment"],
        "Software Developer": ["Programming Languages", "Algorithms", "System Design", "Testing"],
        "Game Developer": ["Game Engines", "Graphics Programming", "Game Physics", "3D Mathematics"]
    }
    
    focus_areas = CAREER_FOCUS_AREAS.get(predicted_career, [])
    user_skills_lower = [skill.lower() for skill in user_skills]
    
    # Identify missing focus areas
    missing_areas = []
    for area in focus_areas:
        if not any(area.lower() in skill or skill in area.lower() for skill in user_skills_lower):
            missing_areas.append(area)
    
    return missing_areas

# Integration function for your existing app
def integrate_smart_quiz_in_app(user_skills):
    """
    Drop-in replacement for your existing quiz logic in app.py
    """
    # Get adaptive quiz configuration
    quiz_config = adaptive_quiz_flow(user_skills)
    
    # Return questions in the format your app expects
    return quiz_config['questions'], quiz_config

# Test the smart quiz system
if __name__ == "__main__":
    test_skills = ["Python", "Data Analysis", "SQL"]
    questions, config = integrate_smart_quiz_in_app(test_skills)
    
    print(f"Smart Quiz Generated:")
    print(f"Predicted Career: {config['predicted_career']}")
    print(f"Confidence: {config['confidence']}%")
    print(f"Questions Selected: {len(questions)}")
    print(f"Focus Areas: {config['adaptive_rules']['focus_areas']}")
    print("\\nSample Questions:")
    for i, q in enumerate(questions[:3]):
        print(f"{i+1}. {q.get('question', 'N/A')} (Skill: {q.get('skill', 'N/A')})")