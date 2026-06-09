import streamlit as st

st.set_page_config(
    page_title="Agentic AI",
    page_icon="🤖",
    layout="wide"
)
USERS = {
    "admin": {"password": "admin123", "role": "admin", "email": "admin@example.com"},
    "ronit": {"password": "123", "role": "admin", "email": "ronit@example.com"},
    "user2": {"password": "user456", "role": "user", "email": "user2@example.com"},
}
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    with st.form("user_form"):
        username = st.text_input("Enter your name")
        password = st.text_input("Enter your password", type="password")
        email = st.text_input("Enter your email")
        
        if st.form_submit_button("Login"):
            user = USERS.get(username)

            if user and user["password"] == password:
                st.session_state.logged_in = True
                st.session_state.role = user["role"]
                st.session_state.email = user["email"]
                st.write(f"Welcome, {username}! You are logged in as {user['role']}.")
                st.write(f"Your email is: {user['email']}")
            else:
                st.error("Invalid credentials")

        