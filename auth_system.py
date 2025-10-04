"""
Enhanced Authentication System for AspirePath
Provides a simple, user-friendly login and signup experience
"""

import streamlit as st
import hashlib
from datetime import datetime
import re
from helpers_session import init_session_state_db

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    return True, "Password is strong"

def validate_name(name):
    """Validate name format"""
    return len(name.strip()) >= 2 and name.strip().replace(' ', '').isalpha()

class AuthenticationSystem:
    """Simple and effective authentication system"""
    
    def __init__(self):
        self.init_auth_state()
    
    def init_auth_state(self):
        """Initialize authentication session state"""
        init_session_state_db()
        
        # Initialize auth-specific states
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'user_name' not in st.session_state:
            st.session_state.user_name = ""
        if 'user_email' not in st.session_state:
            st.session_state.user_email = ""
        if 'show_signup' not in st.session_state:
            st.session_state.show_signup = False
        if 'remember_email' not in st.session_state:
            st.session_state.remember_email = ""
    
    def create_user(self, name, email, password):
        """Create a new user account"""
        try:
            # Check if user already exists
            for user in st.session_state.users:
                if isinstance(user, dict) and user.get("email") == email:
                    return False, "An account with this email already exists"
            
            # Create new user
            user_data = {
                "name": name,
                "email": email,
                "password": hash_password(password),
                "created_at": datetime.now().isoformat(),
                "last_login": None
            }
            
            st.session_state.users.append(user_data)
            return True, "Account created successfully!"
        
        except Exception as e:
            return False, f"Error creating account: {str(e)}"
    
    def authenticate_user(self, email, password):
        """Authenticate user login"""
        try:
            hashed_password = hash_password(password)
            
            for user in st.session_state.users:
                if (isinstance(user, dict) and 
                    user.get("email") == email and 
                    user.get("password") == hashed_password):
                    
                    # Update last login
                    user["last_login"] = datetime.now().isoformat()
                    return user
            
            return None
        
        except Exception as e:
            st.error(f"Authentication error: {str(e)}")
            return None
    
    def login_user(self, user_data):
        """Set user as logged in"""
        st.session_state.authenticated = True
        st.session_state.user_name = user_data["name"]
        st.session_state.user_email = user_data["email"]
    
    def logout_user(self):
        """Log out the current user"""
        st.session_state.authenticated = False
        st.session_state.user_name = ""
        st.session_state.user_email = ""
        st.session_state.show_signup = False
    
    def show_demo_credentials(self):
        """Display demo credentials for testing"""
        st.info("""
        🧪 **Try Demo Credentials:**
        - **Email:** demo@aspirepath.com
        - **Password:** demo123
        
        Or create your own account below! 👇
        """)
        
        # Quick login button for demo
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("⚡ Quick Demo Login", use_container_width=True, help="Login instantly with demo credentials"):
                # Auto-login with demo credentials
                user = self.authenticate_user("demo@aspirepath.com", "demo123")
                if user:
                    self.login_user(user)
                    st.success("🎉 Demo login successful!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Demo login failed. Please try manual login.")
    
    def render_login_form(self):
        """Render the login form"""
        st.markdown("### 🔑 Welcome Back!")
        st.markdown("Sign in to continue your career journey")
        
        # Demo credentials
        self.show_demo_credentials()
        
        with st.form("login_form", clear_on_submit=False):
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col2:
                # Pre-fill email if remembered
                default_email = st.session_state.get('remember_email', '')
                email = st.text_input(
                    "📧 Email Address", 
                    value=default_email,
                    placeholder="your.email@example.com"
                )
                
                password = st.text_input(
                    "🔒 Password", 
                    type="password",
                    placeholder="Enter your password"
                )
                
                # Remember me checkbox
                remember_me = st.checkbox("Remember my email")
                
                # Submit button
                login_submitted = st.form_submit_button(
                    "🚀 Sign In", 
                    use_container_width=True
                )
            
            if login_submitted:
                if not email or not password:
                    st.error("❌ Please enter both email and password")
                    return
                
                if not validate_email(email):
                    st.error("❌ Please enter a valid email address")
                    return
                
                # Remember email if requested
                if remember_me:
                    st.session_state.remember_email = email
                else:
                    st.session_state.remember_email = ""
                
                # Authenticate user
                user = self.authenticate_user(email, password)
                if user:
                    self.login_user(user)
                    st.success(f"🎉 Welcome back, {user['name']}!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Invalid email or password. Please try again.")
                    
                    # Show helpful message
                    st.markdown("""
                    <div style="text-align: center; margin-top: 1rem;">
                        <p style="color: #888; font-size: 0.9rem;">
                            💡 <strong>Tip:</strong> Try the demo credentials above or create a new account
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Switch to signup
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🌟 New to AspirePath? Create Account", use_container_width=True):
                st.session_state.show_signup = True
                st.rerun()
    
    def render_signup_form(self):
        """Render the signup form"""
        st.markdown("### 🌟 Join AspirePath!")
        st.markdown("Create your account and unlock your career potential")
        
        with st.form("signup_form", clear_on_submit=True):
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col2:
                name = st.text_input(
                    "👤 Full Name", 
                    placeholder="Enter your full name"
                )
                
                email = st.text_input(
                    "📧 Email Address", 
                    placeholder="your.email@example.com"
                )
                
                password = st.text_input(
                    "🔒 Password", 
                    type="password",
                    placeholder="Create a strong password"
                )
                
                confirm_password = st.text_input(
                    "🔒 Confirm Password", 
                    type="password",
                    placeholder="Confirm your password"
                )
                
                # Show password requirements
                with st.expander("🔍 Password Requirements"):
                    st.markdown("""
                    **Your password must have:**
                    - ✅ At least 8 characters
                    - ✅ One uppercase letter (A-Z)
                    - ✅ One lowercase letter (a-z)
                    - ✅ One number (0-9)
                    - ✅ One special character (!@#$%^&*(),.?":{}|<>)
                    """)
                
                # Terms checkbox
                agree_terms = st.checkbox("I agree to AspirePath's Terms of Service and Privacy Policy")
                
                # Submit button
                signup_submitted = st.form_submit_button(
                    "🎯 Create My Account", 
                    use_container_width=True
                )
            
            if signup_submitted:
                # Validate all fields
                errors = []
                
                if not name or not validate_name(name):
                    errors.append("Please enter a valid full name (at least 2 characters)")
                
                if not email or not validate_email(email):
                    errors.append("Please enter a valid email address")
                
                if not password:
                    errors.append("Please enter a password")
                else:
                    is_valid, msg = validate_password(password)
                    if not is_valid:
                        errors.append(msg)
                
                if password != confirm_password:
                    errors.append("Passwords do not match")
                
                if not agree_terms:
                    errors.append("Please agree to the Terms of Service")
                
                # Show errors
                if errors:
                    for error in errors:
                        st.error(f"❌ {error}")
                    return
                
                # Create user account
                success, message = self.create_user(name.strip(), email.lower().strip(), password)
                
                if success:
                    # Auto-login the new user
                    user = self.authenticate_user(email.lower().strip(), password)
                    if user:
                        self.login_user(user)
                        st.success("🎉 Account created successfully! Welcome to AspirePath!")
                        st.markdown("""
                        <div style="text-align: center; padding: 1rem; background: rgba(76, 175, 80, 0.1); border-radius: 10px; margin: 1rem 0;">
                            <p style="color: #4CAF50; margin: 0;">
                                🚀 <strong>You're all set!</strong> Explore your personalized career journey now.
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                        st.balloons()
                        st.rerun()
                else:
                    st.error(f"❌ {message}")
                    if "already exists" in message.lower():
                        st.info("💡 **Tip:** Try logging in instead, or use a different email address.")
        
        # Switch to login
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔑 Already have an account? Sign In", use_container_width=True):
                st.session_state.show_signup = False
                st.rerun()
    
    def render_auth_page(self):
        """Render the complete authentication page"""
        # Enhanced header with modern design
        st.markdown("""
        <div style="text-align: center; padding: 3rem 0 2rem 0; background: linear-gradient(135deg, rgba(76, 175, 80, 0.1), rgba(255, 193, 7, 0.1)); border-radius: 20px; margin-bottom: 2rem; border: 1px solid rgba(255,255,255,0.1);">
            <div style="font-size: 4rem; margin-bottom: 1rem; background: linear-gradient(45deg, #4CAF50, #FFD700); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">🚀</div>
            <h1 style="color: #4CAF50; font-size: 3.5rem; margin-bottom: 0.5rem; font-weight: 800; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">AspirePath</h1>
            <p style="font-size: 1.4rem; color: #888; margin-bottom: 1rem; font-weight: 300;">
                Your AI-Powered Career Journey Starts Here
            </p>
            <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap; margin-top: 1.5rem;">
                <div style="background: rgba(76, 175, 80, 0.2); padding: 0.5rem 1rem; border-radius: 20px; color: #4CAF50; font-size: 0.9rem; font-weight: 600;">✨ ML-Powered</div>
                <div style="background: rgba(255, 193, 7, 0.2); padding: 0.5rem 1rem; border-radius: 20px; color: #FFD700; font-size: 0.9rem; font-weight: 600;">🎯 Personalized</div>
                <div style="background: rgba(33, 150, 243, 0.2); padding: 0.5rem 1rem; border-radius: 20px; color: #2196F3; font-size: 0.9rem; font-weight: 600;">🚀 Results-Driven</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Main container with improved styling
        with st.container():
            # Show appropriate form
            if st.session_state.get('show_signup', False):
                self.render_signup_form()
            else:
                self.render_login_form()
        
        # Enhanced footer
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: rgba(255,255,255,0.05); border-radius: 15px; margin-top: 2rem;">
            <div style="display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap; margin-bottom: 1rem;">
                <div style="color: #4CAF50;">🤖 <strong>Advanced ML</strong></div>
                <div style="color: #2196F3;">🔒 <strong>Secure & Private</strong></div>
                <div style="color: #FFD700;">⚡ <strong>Instant Access</strong></div>
            </div>
            <p style="color: #666; font-size: 0.9rem; margin: 0;">
                Join thousands of professionals transforming their careers with AI
            </p>
        </div>
        """, unsafe_allow_html=True)

# Initialize the authentication system
def get_auth_system():
    """Get or create authentication system instance"""
    if 'auth_system' not in st.session_state:
        st.session_state.auth_system = AuthenticationSystem()
    return st.session_state.auth_system