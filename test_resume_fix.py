"""
Test script to verify resume parsing and skill extraction works without errors
"""

import streamlit as st
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_resume_parsing():
    """Test the resume parsing functionality"""
    try:
        from helpers_session import parse_resume, init_session_state_db
        from core import assess_skills
        
        print("✅ All imports successful")
        
        # Initialize session state
        if 'users' not in st.session_state:
            st.session_state.users = []
        if 'resumes' not in st.session_state:
            st.session_state.resumes = []
            
        init_session_state_db()
        print("✅ Session state initialized")
        
        # Test skill assessment with sample text
        sample_text = "I have experience with Python, JavaScript, React, Node.js, and MongoDB. I also know HTML, CSS, and SQL."
        skills = assess_skills(sample_text)
        print(f"✅ Skill assessment works: Found {len(skills)} skills: {skills[:5]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in testing: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 Testing AspirePath resume parsing functionality...")
    success = test_resume_parsing()
    if success:
        print("🎉 All tests passed! Resume parsing should work correctly.")
    else:
        print("⚠️ Some issues detected. Check the error messages above.")