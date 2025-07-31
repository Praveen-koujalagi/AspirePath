import streamlit as st

# Page config
st.set_page_config(
    page_title="AspirePath - Theme Test",
    page_icon="🚀",
    layout="wide"
)

# Test the black theme
st.markdown("""
<style>
    .main {
        background-color: #000000 !important;
        color: white !important;
    }
    
    section[data-testid="stSidebar"] {
        background-color: #000000 !important;
    }
    
    * {
        color: white !important;
    }
    
    h1, h2, h3 {
        color: #FFD700 !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("🚀 AspirePath - Theme Diagnostic")
st.header("Black Theme Test")

st.write("If you can see this white text on black background, the theme is working!")

with st.sidebar:
    st.header("Sidebar Test")
    st.write("This sidebar should also be black with white text.")
    
col1, col2 = st.columns(2)

with col1:
    st.subheader("Text Visibility Test")
    st.write("✅ This text should be WHITE")
    st.success("Success message test")
    
with col2:
    st.subheader("Input Test")
    test_input = st.text_input("Test input field")
    if st.button("Test Button"):
        st.write("Button works!")

st.info("If all text above is visible, the black theme is working correctly!")