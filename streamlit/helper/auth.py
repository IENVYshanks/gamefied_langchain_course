import streamlit as st

def require_role(*roles):
    if st.session_state.role not in roles:
        st.error("Access Denied")
        st.stop()