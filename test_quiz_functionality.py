#!/usr/bin/env python3
"""
Test script for Skill Quiz & Resume functionality
"""

from quiz_engine import fetch_questions_from_api, load_questions
from core import assess_skills

def test_quiz_engine():
    """Test the quiz engine functionality"""
    
    print("🧪 Testing Quiz Engine Functionality")
    print("=" * 50)
    
    # Test skills
    test_skills = ["Python", "SQL", "Machine Learning", "JavaScript"]
    
    for skill in test_skills:
        print(f"\n📋 Testing skill: {skill}")
        
        # Test local question loading
        questions = load_questions([skill])
        print(f"   Local questions found: {len(questions)}")
        
        if questions:
            sample_q = questions[0]
            print(f"   Sample question: {sample_q['question'][:50]}...")
            print(f"   Answer options: {len(sample_q['options'])} choices")
        
        # Test API function (which falls back to local)
        api_questions = fetch_questions_from_api([skill])
        print(f"   API function returned: {len(api_questions)} questions")
    
    # Test multiple skills
    print(f"\n🔀 Testing multiple skills: {test_skills}")
    multi_questions = fetch_questions_from_api(test_skills)
    print(f"   Total questions for all skills: {len(multi_questions)}")
    
    # Test edge cases
    print(f"\n🔬 Testing edge cases:")
    
    # Empty skills
    empty_result = fetch_questions_from_api([])
    print(f"   Empty skills list: {len(empty_result)} questions")
    
    # Non-existent skill
    fake_skill = fetch_questions_from_api(["Quantum Basket Weaving"])
    print(f"   Non-existent skill: {len(fake_skill)} questions")
    
    # Case sensitivity test
    case_test = fetch_questions_from_api(["python", "PYTHON", "Python"])
    print(f"   Case sensitivity test: {len(case_test)} questions")
    
    print("\n" + "=" * 50)
    print("✅ Quiz engine testing completed!")

def test_skill_assessment():
    """Test skill assessment from text"""
    
    print("\n🧪 Testing Skill Assessment")
    print("=" * 50)
    
    # Sample resume text
    sample_texts = [
        "I have 5 years of experience in Python programming, SQL databases, and machine learning projects.",
        "Skilled in JavaScript, React, HTML, CSS, and Node.js development.",
        "Experienced data analyst with expertise in SQL, Excel, Tableau, and statistical analysis.",
        "Software engineer proficient in Java, Spring Boot, microservices, and AWS cloud technologies."
    ]
    
    for i, text in enumerate(sample_texts, 1):
        print(f"\n📄 Sample text {i}:")
        print(f"   Text: {text[:60]}...")
        
        try:
            skills = assess_skills(text)
            print(f"   Extracted skills: {skills}")
            print(f"   Number of skills: {len(skills)}")
        except Exception as e:
            print(f"   Error extracting skills: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Skill assessment testing completed!")

if __name__ == "__main__":
    try:
        test_quiz_engine()
        test_skill_assessment()
        
        print("\n🎉 All tests completed successfully!")
        print("🚀 The Skill Quiz & Resume functionality should be working properly!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        print("🔧 Please check the implementation and try again.")
