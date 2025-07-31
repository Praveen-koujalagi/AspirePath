import streamlit as st

# Simple test to check if basic Streamlit is working
st.set_page_config(
    page_title="AspirePath Test",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 AspirePath - Test Page")
st.write("If you can see this, the basic Streamlit setup is working!")

# Test basic functionality
st.button("Test Button")
st.selectbox("Test Select", ["Option 1", "Option 2"])

st.success("✅ Basic Streamlit components are loading correctly!")

st.markdown("""
### Debug Information:
- This is a test page to verify Streamlit is working
- If you see this, the deployment is successful
- The white screen issue might be in the main app.py
""")
