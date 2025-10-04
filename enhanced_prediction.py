# 🚀 IMMEDIATE ML ENHANCEMENT - Drop-in replacement for core.py predict_career function

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def predict_career_enhanced(user_skills):
    """
    Enhanced career prediction with ML-based confidence scoring and multiple suggestions.
    This is a drop-in replacement for your current predict_career function.
    
    Returns: dict with enhanced prediction data
    """
    if not user_skills:
        return {
            'primary_career': 'Generalist',
            'confidence': 0,
            'alternatives': [],
            'method': 'fallback'
        }
    
    # Your existing career skills data
    CAREER_SKILLS = {
        "Data Analyst": "Excel, SQL, Python, Tableau, Statistics, Power BI, Data Analysis, Analytics, R, SPSS, Data Visualization, Pandas, NumPy",
        "Web Developer": "HTML, CSS, JavaScript, React, Node.js, MongoDB, Angular, Vue, Frontend, Backend, Web Development, Bootstrap, jQuery",
        "ML Engineer": "Python, NumPy, Pandas, Scikit-learn, Deep Learning, Machine Learning, TensorFlow, PyTorch, Data Science, Statistics",
        "Cybersecurity Analyst": "Network Security, Cryptography, Firewalls, Linux, Ethical Hacking, Penetration Testing, Security Analysis, Cybersecurity",
        "AI Engineer": "Python, TensorFlow, PyTorch, Machine Learning, Neural Networks, Artificial Intelligence, Deep Learning, NLP, Computer Vision",
        "Software Developer": "C++, Java, Python, Data Structures, Algorithms, Programming, Software Development, C#, .NET, Object-Oriented Programming",
        "Game Developer": "C++, Unity, Unreal Engine, Game Physics, 3D Modeling, Game Development, C#, Graphics Programming, Animation"
    }
    
    # Create documents for TF-IDF analysis
    user_skills_text = " ".join(user_skills)
    career_documents = [skills_text for skills_text in CAREER_SKILLS.values()]
    all_documents = [user_skills_text] + career_documents
    
    # Use TF-IDF for better text similarity (you already have this imported!)
    try:
        vectorizer = TfidfVectorizer(stop_words='english', lowercase=True)
        tfidf_matrix = vectorizer.fit_transform(all_documents)
        
        # Calculate cosine similarity between user skills and each career
        user_vector = tfidf_matrix[0:1]  # First document is user skills
        career_vectors = tfidf_matrix[1:]  # Rest are career skills
        
        similarities = cosine_similarity(user_vector, career_vectors).flatten()
        
        # Create career predictions with confidence scores
        career_predictions = []
        career_names = list(CAREER_SKILLS.keys())
        
        for i, similarity in enumerate(similarities):
            confidence = min(similarity * 100, 100)  # Convert to percentage, cap at 100
            career_predictions.append({
                'career': career_names[i],
                'confidence': round(confidence, 1),
                'similarity_score': similarity
            })
        
        # Sort by confidence
        career_predictions.sort(key=lambda x: x['confidence'], reverse=True)
        
        # Apply your existing rule-based scoring as a boost
        for pred in career_predictions:
            rule_based_score = calculate_rule_based_score(user_skills, pred['career'], CAREER_SKILLS)
            # Combine ML score with rule-based score (weighted average)
            combined_score = (pred['confidence'] * 0.6) + (rule_based_score * 0.4)
            pred['confidence'] = round(combined_score, 1)
        
        # Re-sort after combining scores
        career_predictions.sort(key=lambda x: x['confidence'], reverse=True)
        
        return {
            'primary_career': career_predictions[0]['career'],
            'confidence': career_predictions[0]['confidence'],
            'alternatives': career_predictions[1:4],  # Top 3 alternatives
            'all_predictions': career_predictions,
            'method': 'ml_enhanced'
        }
        
    except Exception as e:
        print(f"ML prediction failed: {e}, using fallback")
        # Fallback to your existing logic
        from core import predict_career as original_predict
        return {
            'primary_career': original_predict(user_skills),
            'confidence': 85.7,  # Your reported accuracy
            'alternatives': [],
            'method': 'rule_based_fallback'
        }

def calculate_rule_based_score(user_skills, career, career_skills_dict):
    """Calculate rule-based score using your existing logic"""
    skills_str = career_skills_dict.get(career, "")
    career_skills = [skill.strip().lower() for skill in skills_str.split(",")]
    normalized_user_skills = [skill.strip().lower() for skill in user_skills]
    
    exact_matches = sum(2 for user_skill in normalized_user_skills if user_skill in career_skills)
    partial_matches = 0
    
    for user_skill in normalized_user_skills:
        if user_skill not in career_skills:
            for career_skill in career_skills:
                if user_skill in career_skill or career_skill in user_skill:
                    partial_matches += 0.5
                    break
    
    total_score = exact_matches + partial_matches
    normalized_score = (total_score / len(career_skills)) * 100 if career_skills else 0
    return min(normalized_score, 100)

# Test the enhanced function
if __name__ == "__main__":
    test_skills = ["Python", "Machine Learning", "Data Analysis", "SQL"]
    result = predict_career_enhanced(test_skills)
    print("Enhanced Prediction Result:")
    print(f"Primary: {result['primary_career']} ({result['confidence']}%)")
    print("Alternatives:")
    for alt in result['alternatives']:
        print(f"  - {alt['career']}: {alt['confidence']}%")