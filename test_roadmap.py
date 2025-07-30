#!/usr/bin/env python3
"""
Test script for Career Roadmap functionality
"""

import sys
sys.path.append('.')

from core import predict_career, generate_roadmap

def test_career_roadmap():
    """Test the career roadmap functionality"""
    
    print("🧪 Testing Career Roadmap Functions...")
    print("=" * 50)
    
    # Test case 1: Data Analyst skills
    test_skills_1 = ["Python", "SQL", "Excel"]
    print(f"\n📊 Test 1 - Skills: {test_skills_1}")
    
    try:
        predicted_career_1 = predict_career(test_skills_1)
        print(f"Predicted Career: {predicted_career_1}")
        
        roadmap_1, required_1 = generate_roadmap(test_skills_1, predicted_career_1)
        print(f"Required Skills: {required_1}")
        print(f"Learning Roadmap: {roadmap_1}")
        print(f"Skills to Learn: {len(roadmap_1)}")
        
    except Exception as e:
        print(f"❌ Error in Test 1: {e}")
    
    # Test case 2: Web Developer skills
    test_skills_2 = ["HTML", "CSS", "JavaScript"]
    print(f"\n🌐 Test 2 - Skills: {test_skills_2}")
    
    try:
        predicted_career_2 = predict_career(test_skills_2)
        print(f"Predicted Career: {predicted_career_2}")
        
        roadmap_2, required_2 = generate_roadmap(test_skills_2, predicted_career_2)
        print(f"Required Skills: {required_2}")
        print(f"Learning Roadmap: {roadmap_2}")
        print(f"Skills to Learn: {len(roadmap_2)}")
        
    except Exception as e:
        print(f"❌ Error in Test 2: {e}")
    
    # Test case 3: Mixed skills
    test_skills_3 = ["Python", "Machine Learning", "React"]
    print(f"\n🤖 Test 3 - Skills: {test_skills_3}")
    
    try:
        predicted_career_3 = predict_career(test_skills_3)
        print(f"Predicted Career: {predicted_career_3}")
        
        roadmap_3, required_3 = generate_roadmap(test_skills_3, predicted_career_3)
        print(f"Required Skills: {required_3}")
        print(f"Learning Roadmap: {roadmap_3}")
        print(f"Skills to Learn: {len(roadmap_3)}")
        
    except Exception as e:
        print(f"❌ Error in Test 3: {e}")
    
    print("\n✅ Career Roadmap tests completed!")

if __name__ == "__main__":
    test_career_roadmap()
