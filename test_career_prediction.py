#!/usr/bin/env python3
"""
Test script for improved Career Prediction functionality
"""

import sys
sys.path.append('.')

from core import predict_career, generate_roadmap

def test_career_prediction():
    """Test the improved career prediction with various skill combinations"""
    
    print("🧪 Testing Improved Career Prediction...")
    print("=" * 60)
    
    # Test cases with different skill combinations
    test_cases = [
        {
            "name": "Data Analyst Skills",
            "skills": ["Excel", "SQL", "Python", "Tableau"],
            "expected": "Data Analyst"
        },
        {
            "name": "Web Developer Skills",
            "skills": ["HTML", "CSS", "JavaScript", "React"],
            "expected": "Web Developer"
        },
        {
            "name": "ML Engineer Skills", 
            "skills": ["Python", "Machine Learning", "Pandas", "NumPy"],
            "expected": "ML Engineer"
        },
        {
            "name": "AI Engineer Skills",
            "skills": ["Python", "TensorFlow", "Neural Networks", "Deep Learning"],
            "expected": "AI Engineer"
        },
        {
            "name": "Cybersecurity Skills",
            "skills": ["Linux", "Network Security", "Firewalls", "Ethical Hacking"],
            "expected": "Cybersecurity Analyst"
        },
        {
            "name": "Game Developer Skills",
            "skills": ["Unity", "C#", "Game Development", "3D Modeling"],
            "expected": "Game Developer"
        },
        {
            "name": "Mixed Technical Skills",
            "skills": ["Java", "Programming", "Algorithms", "Data Structures"],
            "expected": "Software Developer"
        },
        {
            "name": "Alternative Naming",
            "skills": ["Data Analysis", "Power BI", "Statistics"],
            "expected": "Data Analyst"
        },
        {
            "name": "Frontend Focus",
            "skills": ["JavaScript", "React", "Frontend", "CSS"],
            "expected": "Web Developer"
        },
        {
            "name": "Very Generic Skills",
            "skills": ["Microsoft Office", "Communication"],
            "expected": "Generalist or Software Developer"
        }
    ]
    
    success_count = 0
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔍 Test {i}: {test_case['name']}")
        print(f"Input Skills: {test_case['skills']}")
        
        try:
            predicted_career = predict_career(test_case['skills'])
            print(f"Predicted Career: {predicted_career}")
            print(f"Expected: {test_case['expected']}")
            
            # Check if prediction matches expectation (allowing for some flexibility)
            if predicted_career == test_case['expected'] or test_case['expected'] in predicted_career:
                print("✅ PASS")
                success_count += 1
            elif "or" in test_case['expected'] and predicted_career in test_case['expected']:
                print("✅ PASS (Alternative)")
                success_count += 1
            else:
                print("❌ FAIL")
            
            # Also test roadmap generation
            roadmap, required = generate_roadmap(test_case['skills'], predicted_career)
            print(f"Learning Path: {len(roadmap)} skills to learn")
            
        except Exception as e:
            print(f"❌ ERROR: {e}")
    
    print(f"\n" + "=" * 60)
    print(f"📊 Test Results: {success_count}/{len(test_cases)} tests passed")
    print(f"Success Rate: {(success_count/len(test_cases)*100):.1f}%")
    
    if success_count >= len(test_cases) * 0.8:  # 80% success rate
        print("🎉 Career prediction is working well!")
    else:
        print("⚠️ Career prediction needs more tuning.")

if __name__ == "__main__":
    test_career_prediction()
