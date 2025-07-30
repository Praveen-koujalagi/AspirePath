import json
import random
import requests
import streamlit as st

def load_questions(skills, path="real_mcq_bank.json"):
    """
    Load questions from local JSON file based on skills.
    
    Args:
        skills (list): List of skills to filter questions
        path (str): Path to the JSON file containing questions
        
    Returns:
        list: Filtered questions matching the skills
    """
    try:
        with open(path, "r", encoding='utf-8') as f:
            all_qs = json.load(f)
        
        # Create case-insensitive skill matching
        skills_lower = [skill.lower().strip() for skill in skills]
        
        # Find questions that match any of the user's skills
        matching_questions = []
        for q in all_qs:
            question_skill = q.get("skill", "").lower().strip()
            if any(skill in question_skill or question_skill in skill for skill in skills_lower):
                matching_questions.append(q)
        
        return matching_questions
        
    except FileNotFoundError:
        print(f"Question bank file not found: {path}")
        return []
    except json.JSONDecodeError:
        print(f"Invalid JSON format in: {path}")
        return []
    except Exception as e:
        print(f"Error loading questions: {e}")
        return []

def fetch_questions_from_api(skills, api_url="https://example.com/api/questions", api_key="your_api_key"):
    """
    Fetches questions from a real-time API based on the provided skills.
    Falls back to local questions if API is unavailable.

    Args:
        skills (list): List of skills to generate questions for.
        api_url (str): The API endpoint for fetching questions.
        api_key (str): The API key for authentication.

    Returns:
        list: A list of questions in the format [{"id": ..., "question": ..., "options": [...], "answer": ...}].
    """
    # Skip API call since it's a placeholder and go directly to local questions
    # In a real implementation, you would uncomment the API code below
    
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {"skills": skills}

    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        questions = response.json().get("questions", [])

        if questions:
            random.shuffle(questions)
            return questions[:10]  # Limit to 10 questions max
            
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
    """
    
    # Use local questions (primary method for now)
    try:
        local_questions = load_questions(skills)
        if local_questions:
            # Limit to reasonable number of questions
            random.shuffle(local_questions)
            return local_questions[:min(10, len(local_questions))]
        else:
            # If no questions found for specific skills, try general questions
            print(f"No questions found for skills: {skills}")
            # Try to find questions for common skills
            common_skills = ["Python", "JavaScript", "SQL", "HTML", "CSS", "Java"]
            fallback_skills = [skill for skill in common_skills if any(s.lower() in skill.lower() for s in skills)]
            
            if fallback_skills:
                fallback_questions = load_questions(fallback_skills)
                if fallback_questions:
                    random.shuffle(fallback_questions)
                    return fallback_questions[:5]
            
            return []
    except Exception as e:
        print(f"Error loading questions: {e}")
        return []

def run_quiz(skills, num_qs=5):
    questions = load_questions(skills)
    random.shuffle(questions)
    selected = questions[:num_qs]

    st.session_state["quiz_answers"] = st.session_state.get("quiz_answers", {})

    form_key = f"quiz_form_{random.randint(1, 10000)}"  # Generate a unique key for the form
    with st.form(form_key):
        for q in selected:
            user_ans = st.radio(
                q["question"],
                q["options"],
                key=f"quiz_{q['id']}"
            )
            st.session_state["quiz_answers"][q["id"]] = user_ans

        submitted = st.form_submit_button("✅ Submit Quiz")

    score = 0
    wrong = []
    if submitted:
        for q in selected:
            user_ans = st.session_state["quiz_answers"].get(q["id"], "")
            if user_ans == q["answer"]:
                score += 1
            else:
                q["user_answer"] = user_ans
                wrong.append(q)

        return score, len(selected), wrong

    return None, len(selected), []
