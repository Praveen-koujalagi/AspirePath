# 🧪 Session State Demo - Understanding How It Works

import streamlit as st

st.title("🧠 Streamlit Session State Demo")

st.markdown("""
## What is Session State?
Session State is like having a **temporary memory** for your app that remembers things while the user is interacting with it.

### 🔍 **Try This Demo:**
""")

# Initialize session state
if 'demo_users' not in st.session_state:
    st.session_state.demo_users = []
if 'demo_counter' not in st.session_state:
    st.session_state.demo_counter = 0

# Demo 1: Simple Counter
st.subheader("Demo 1: Simple Counter")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("➕ Add 1"):
        st.session_state.demo_counter += 1

with col2:
    if st.button("➖ Subtract 1"):
        st.session_state.demo_counter -= 1

with col3:
    if st.button("🔄 Reset"):
        st.session_state.demo_counter = 0

st.write(f"**Current Count:** {st.session_state.demo_counter}")

st.markdown("---")

# Demo 2: User Registration
st.subheader("Demo 2: User Registration (Like Your App)")

with st.form("user_demo"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    submitted = st.form_submit_button("Add User")
    
    if submitted and name and email:
        # Add user to session state
        user_data = {"name": name, "email": email}
        st.session_state.demo_users.append(user_data)
        st.success(f"✅ Added {name} to session state!")

# Show current users
if st.session_state.demo_users:
    st.subheader("Users in Session State:")
    for i, user in enumerate(st.session_state.demo_users, 1):
        st.write(f"{i}. **{user['name']}** - {user['email']}")
else:
    st.info("No users registered yet. Add some users above!")

# Clear users
if st.button("🗑️ Clear All Users"):
    st.session_state.demo_users = []
    st.success("Cleared all users!")

st.markdown("---")

# Explanation
st.subheader("🎯 How This Works in Your AspirePath App:")

st.markdown("""
### Instead of MongoDB:
```python
# OLD (MongoDB):
users_collection.insert_one({"name": "John", "email": "john@email.com"})
user = users_collection.find_one({"email": "john@email.com"})

# NEW (Session State):
st.session_state.users.append({"name": "John", "email": "john@email.com"})
user = next((u for u in st.session_state.users if u["email"] == "john@email.com"), None)
```

### ✅ **Advantages:**
- ✨ **Zero Setup** - Works immediately
- 🚀 **Fast Deployment** - No database configuration needed
- 💰 **Free** - No external service costs
- 🔧 **Simple** - Easy to understand and implement

### ⚠️ **Limitations:**
- 🔄 **Data Lost on Refresh** - Users lose data if they refresh the page
- 👤 **Single Session** - Each user only sees their own data
- ⏰ **Temporary** - Data doesn't survive browser closure
- 📊 **Not for Production** - Good for demos and prototypes only

### 🎯 **Perfect For:**
- 🎭 **Demo Applications** - Showing off your app's functionality
- 🏗️ **Prototypes** - Testing ideas quickly
- 📚 **Learning** - Understanding how your app works
- 🎪 **Presentations** - Live demonstrations
""")

st.markdown("---")

# Show raw session state
with st.expander("🔍 View Raw Session State Data"):
    st.write("**Current Session State:**")
    st.json({
        "demo_counter": st.session_state.demo_counter,
        "demo_users": st.session_state.demo_users,
        "total_keys": len(st.session_state.keys()),
        "all_keys": list(st.session_state.keys())
    })

st.info("💡 **Try refreshing this page** - you'll see all the data disappears! That's the main limitation of session state.")
