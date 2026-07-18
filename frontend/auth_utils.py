import secrets

import streamlit as st

from database import authenticate_user, create_user, find_username_by_email, reset_password


class DatabaseAuthenticator:
    """Small Streamlit-compatible auth UI backed entirely by MySQL."""

    def login(self, location="main"):
        if location == "unrendered" or st.session_state.get("authentication_status"):
            return
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
        if submitted:
            user = authenticate_user(username, password)
            if not user:
                st.session_state["authentication_status"] = False
                return
            st.session_state.update(
                authentication_status=True, user_id=user["id"], username=user["username"],
                name=user["name"], email=user["email"], role=user["role"],
            )

    def register_user(self, pre_authorized=None):
        with st.form("register_form"):
            name = st.text_input("Full name")
            email = st.text_input("Email")
            username = st.text_input("Choose a username")
            password = st.text_input("Choose a password", type="password")
            confirm = st.text_input("Confirm password", type="password")
            submitted = st.form_submit_button("Register")
        if not submitted:
            return None, None, None
        if password != confirm:
            raise ValueError("Passwords do not match")
        create_user(username, email, name, password)
        return email, username, name

    def forgot_password(self):
        with st.form("password_reset_form"):
            username = st.text_input("Username", key="reset_username")
            email = st.text_input("Email", key="reset_email")
            submitted = st.form_submit_button("Generate new password")
        if not submitted:
            return None, None, None
        new_password = secrets.token_urlsafe(10)
        if not reset_password(username, email, new_password):
            return False, email, None
        return username, email, new_password

    def forgot_username(self):
        with st.form("username_recovery_form"):
            email = st.text_input("Email", key="recovery_email")
            submitted = st.form_submit_button("Recover username")
        if not submitted:
            return None, None
        return find_username_by_email(email) or False, email

    def logout(self, label="Logout", location="sidebar"):
        if st.button(label):
            for key in ("authentication_status", "user_id", "username", "name", "email", "role"):
                st.session_state.pop(key, None)
            st.rerun()


def save_config(config):
    """Compatibility no-op: account changes are committed directly to MySQL."""


def get_authenticator():
    if "authenticator" not in st.session_state:
        st.session_state["authenticator"] = DatabaseAuthenticator()
    return st.session_state["authenticator"], {"pre-authorized": {"emails": []}}


def restore_session():
    return get_authenticator()


def require_login():
    authenticator, config = restore_session()
    if not st.session_state.get("authentication_status"):
        st.warning("Please log in from the Home page to view this module.")
        st.page_link("main.py", label="Go to Home / Login", icon="🏠")
        st.stop()
    return authenticator, config
