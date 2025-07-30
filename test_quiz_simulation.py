#!/usr/bin/env python3
"""
Simulate the quiz answer collection from Streamlit session state
"""

def simulate_streamlit_quiz():
    """Simulate how Streamlit handles quiz answers"""
    
    print("🧪 Simulating Streamlit Quiz Answer Collection")
    print("=" * 60)
    
    # Simulate questions
    questions = [
        {"id": "python_1", "question": "What is Python?", "answer": "Programming Language"},
        {"id": "sql_1", "question": "What does SQL stand for?", "answer": "Structured Query Language"}
    ]
    
    # Simulate different session state scenarios
    scenarios = [
        {
            "name": "All questions answered correctly",
            "session_state": {
                "quiz_q_python_1": "Programming Language",
                "quiz_q_sql_1": "Structured Query Language"
            }
        },
        {
            "name": "All questions answered, some wrong",
            "session_state": {
                "quiz_q_python_1": "Programming Language", 
                "quiz_q_sql_1": "Wrong Answer"
            }
        },
        {
            "name": "Some questions unanswered (None values)",
            "session_state": {
                "quiz_q_python_1": "Programming Language",
                "quiz_q_sql_1": None
            }
        },
        {
            "name": "Some questions missing from session state",
            "session_state": {
                "quiz_q_python_1": "Programming Language"
                # quiz_q_sql_1 is missing entirely
            }
        }
    ]
    
    for scenario in scenarios:
        print(f"\n📋 Scenario: {scenario['name']}")
        print(f"   Session state: {scenario['session_state']}")
        
        # Simulate the answer collection logic from app.py
        user_answers = {}
        for question in questions:
            key = f"quiz_q_{question['id']}"
            if key in scenario['session_state']:
                user_answers[question['id']] = scenario['session_state'][key]
            else:
                user_answers[question['id']] = None
        
        print(f"   Collected answers: {user_answers}")
        
        # Check for unanswered questions
        unanswered = [i+1 for i, q in enumerate(questions) if user_answers.get(q['id']) is None]
        
        if unanswered:
            print(f"   ❌ Validation: Failed - Missing questions {unanswered}")
        else:
            # Calculate score
            score = sum(1 for q in questions if user_answers.get(q['id']) == q['answer'])
            total = len(questions)
            percentage = (score / total) * 100
            print(f"   ✅ Validation: Passed - Score {score}/{total} ({percentage:.1f}%)")
    
    print("\n" + "=" * 60)
    print("✅ Quiz simulation completed successfully!")
    print("🎯 The answer collection logic should now work correctly!")

if __name__ == "__main__":
    simulate_streamlit_quiz()
