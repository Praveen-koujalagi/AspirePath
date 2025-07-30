#!/usr/bin/env python3
"""
Comprehensive test for career prediction algorithm
Tests various skill combinations to ensure diverse career predictions
"""

from core import predict_career, get_career_matches

def test_career_predictions():
    """Test career predictions with various skill combinations"""
    
    test_cases = [
        # Data Science/Analytics focused
        {
            "skills": ["Python", "SQL", "Excel", "Pandas", "Statistics"],
            "expected_categories": ["Data Analyst", "ML Engineer", "AI Engineer"]
        },
        
        # Web Development focused
        {
            "skills": ["JavaScript", "HTML", "CSS", "React", "Node.js"],
            "expected_categories": ["Web Developer", "Software Developer"]
        },
        
        # Machine Learning focused
        {
            "skills": ["Python", "TensorFlow", "Machine Learning", "Deep Learning", "NumPy"],
            "expected_categories": ["ML Engineer", "AI Engineer", "Data Analyst"]
        },
        
        # Cybersecurity focused
        {
            "skills": ["Network Security", "Penetration Testing", "Firewall", "Encryption", "Risk Assessment"],
            "expected_categories": ["Cybersecurity Analyst"]
        },
        
        # Game Development focused
        {
            "skills": ["Unity", "C#", "Game Design", "3D Modeling", "Animation"],
            "expected_categories": ["Game Developer", "Software Developer"]
        },
        
        # AI Engineering focused
        {
            "skills": ["Artificial Intelligence", "Neural Networks", "Computer Vision", "NLP", "Python"],
            "expected_categories": ["AI Engineer", "ML Engineer"]
        },
        
        # Mixed technical skills
        {
            "skills": ["Java", "Spring Boot", "Database Design", "API Development"],
            "expected_categories": ["Software Developer", "Web Developer"]
        },
        
        # Data Analysis specific
        {
            "skills": ["R", "Statistical Analysis", "Data Visualization", "Tableau", "Power BI"],
            "expected_categories": ["Data Analyst"]
        },
        
        # Frontend focused
        {
            "skills": ["React", "Vue.js", "CSS", "HTML", "JavaScript", "UI/UX"],
            "expected_categories": ["Web Developer"]
        },
        
        # Backend/Infrastructure
        {
            "skills": ["AWS", "Docker", "Kubernetes", "Microservices", "DevOps"],
            "expected_categories": ["Software Developer", "Web Developer"]
        }
    ]
    
    print("🧪 Comprehensive Career Prediction Test")
    print("=" * 50)
    
    total_tests = len(test_cases)
    passed_tests = 0
    
    for i, test_case in enumerate(test_cases, 1):
        skills = test_case["skills"]
        expected_categories = test_case["expected_categories"]
        
        print(f"\n📋 Test {i}: {', '.join(skills[:3])}...")
        
        # Get prediction
        predicted_career = predict_career(skills)
        
        # Get all matches for analysis
        career_matches = get_career_matches(skills)
        
        # Check if prediction is in expected categories
        test_passed = predicted_career in expected_categories
        
        if test_passed:
            print(f"✅ PASS: Predicted '{predicted_career}' (Expected: {expected_categories})")
            passed_tests += 1
        else:
            print(f"❌ FAIL: Predicted '{predicted_career}' (Expected: {expected_categories})")
        
        # Show top 3 matches for transparency
        print("   Top 3 matches:")
        for j, (career, score) in enumerate(list(career_matches.items())[:3]):
            marker = "⭐" if career == predicted_career else "  "
            print(f"   {marker} {career}: {score:.1f}%")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed_tests}/{total_tests} tests passed")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! Career prediction is working excellently!")
    elif passed_tests >= total_tests * 0.8:
        print("✅ Most tests passed! Career prediction is working well!")
    else:
        print("⚠️  Some tests failed. Career prediction needs improvement.")
    
    return passed_tests, total_tests

def test_edge_cases():
    """Test edge cases and boundary conditions"""
    
    print("\n🔬 Edge Case Testing")
    print("-" * 30)
    
    edge_cases = [
        {
            "name": "Empty skills",
            "skills": [],
            "expected": "Generalist"
        },
        {
            "name": "Single skill",
            "skills": ["Python"],
            "expected_categories": ["Software Developer", "Data Analyst", "ML Engineer", "AI Engineer", "Web Developer"]
        },
        {
            "name": "Unrecognized skills",
            "skills": ["Underwater Basket Weaving", "Time Travel", "Telepathy"],
            "expected": "Generalist"
        },
        {
            "name": "Mixed case and spacing",
            "skills": [" PYTHON ", "  machine learning  ", "SQL"],
            "expected_categories": ["Data Analyst", "ML Engineer", "AI Engineer"]
        }
    ]
    
    edge_passed = 0
    
    for test_case in edge_cases:
        name = test_case["name"]
        skills = test_case["skills"]
        
        print(f"\n🧪 {name}: {skills}")
        
        predicted = predict_career(skills)
        print(f"   Result: {predicted}")
        
        if "expected" in test_case:
            if predicted == test_case["expected"]:
                print("   ✅ PASS")
                edge_passed += 1
            else:
                print(f"   ❌ FAIL (Expected: {test_case['expected']})")
        elif "expected_categories" in test_case:
            if predicted in test_case["expected_categories"]:
                print("   ✅ PASS")
                edge_passed += 1
            else:
                print(f"   ❌ FAIL (Expected one of: {test_case['expected_categories']})")
    
    print(f"\n📊 Edge Case Results: {edge_passed}/{len(edge_cases)} passed")
    return edge_passed, len(edge_cases)

if __name__ == "__main__":
    # Run comprehensive tests
    main_passed, main_total = test_career_predictions()
    edge_passed, edge_total = test_edge_cases()
    
    # Overall results
    total_passed = main_passed + edge_passed
    total_tests = main_total + edge_total
    
    print("\n" + "=" * 60)
    print("🏆 FINAL RESULTS")
    print("=" * 60)
    print(f"Main Tests: {main_passed}/{main_total} passed ({(main_passed/main_total)*100:.1f}%)")
    print(f"Edge Cases: {edge_passed}/{edge_total} passed ({(edge_passed/edge_total)*100:.1f}%)")
    print(f"Overall: {total_passed}/{total_tests} passed ({(total_passed/total_tests)*100:.1f}%)")
    
    if total_passed == total_tests:
        print("\n🎉 EXCELLENT! All tests passed successfully!")
        print("✨ Career prediction algorithm is working perfectly!")
    elif total_passed >= total_tests * 0.9:
        print("\n🎊 GREAT! Most tests passed!")
        print("👍 Career prediction algorithm is working very well!")
    else:
        print("\n⚠️  NEEDS IMPROVEMENT")
        print("🔧 Career prediction algorithm needs some adjustments.")
