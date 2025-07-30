#!/usr/bin/env python3
"""
Final verification test for career prediction
Tests specific skill combinations to ensure different career paths are predicted
"""

from core import predict_career, get_career_matches

def test_specific_career_paths():
    """Test specific skill combinations that should predict different careers"""
    
    test_cases = [
        {"skills": ["Python", "Pandas", "SQL", "Excel", "Statistics"], "name": "Data Analysis Skills"},
        {"skills": ["JavaScript", "React", "HTML", "CSS", "Node.js"], "name": "Web Development Skills"},
        {"skills": ["Machine Learning", "TensorFlow", "Python", "Deep Learning"], "name": "ML Engineering Skills"},
        {"skills": ["Network Security", "Penetration Testing", "Cybersecurity"], "name": "Cybersecurity Skills"},
        {"skills": ["Unity", "C#", "Game Design", "3D Modeling"], "name": "Game Development Skills"},
        {"skills": ["Artificial Intelligence", "Neural Networks", "NLP"], "name": "AI Engineering Skills"},
        {"skills": ["Java", "Spring Boot", "Microservices", "API"], "name": "Software Development Skills"}
    ]
    
    print("🎯 Career Path Verification Test")
    print("=" * 40)
    
    results = {}
    
    for test_case in test_cases:
        skills = test_case["skills"]
        name = test_case["name"]
        
        predicted = predict_career(skills)
        matches = get_career_matches(skills)
        
        results[name] = {
            "predicted": predicted,
            "top_3": list(matches.items())[:3]
        }
        
        print(f"\n📋 {name}:")
        print(f"   Skills: {', '.join(skills)}")
        print(f"   🔮 Predicted: {predicted}")
        print(f"   📊 Top matches:")
        for career, score in list(matches.items())[:3]:
            marker = "⭐" if career == predicted else "  "
            print(f"      {marker} {career}: {score:.1f}%")
    
    # Check diversity of predictions
    predicted_careers = [results[test]["predicted"] for test in results]
    unique_careers = set(predicted_careers)
    
    print("\n" + "=" * 40)
    print("🏆 DIVERSITY ANALYSIS")
    print("=" * 40)
    print(f"Total test cases: {len(test_cases)}")
    print(f"Unique predictions: {len(unique_careers)}")
    print(f"Diversity score: {len(unique_careers)/len(test_cases)*100:.1f}%")
    
    print(f"\nPredicted careers: {', '.join(unique_careers)}")
    
    if len(unique_careers) >= 5:
        print("🎉 EXCELLENT diversity! Different skills predict different careers!")
    elif len(unique_careers) >= 3:
        print("✅ GOOD diversity! Most skills predict appropriate careers!")
    else:
        print("⚠️  LOW diversity. Algorithm may need adjustment.")
    
    return len(unique_careers), len(test_cases)

if __name__ == "__main__":
    unique_count, total_count = test_specific_career_paths()
    
    print(f"\n🎯 Final Result: {unique_count}/{total_count} different career paths predicted")
    
    if unique_count >= 5:
        print("✨ Career roadmap is working perfectly with diverse predictions!")
    else:
        print("🔧 Career prediction could use more diversity in suggestions.")
