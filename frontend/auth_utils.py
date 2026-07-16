import os

import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Resolve config.yaml next to this file so it works regardless of the
# directory `streamlit run` was launched from.
_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(_DIR, "config.yaml")


def load_config():
    with open(CONFIG_PATH) as file:
        return yaml.load(file, Loader=SafeLoader)


def save_config(config):
    with open(CONFIG_PATH, "w") as file:
        yaml.dump(config, file, default_flow_style=False, allow_unicode=True)


def get_authenticator():
    """
    Build the Authenticate object once per session and reuse the same
    instance on every page so the same cookie manager is shared app-wide.
    """
    if "authenticator" not in st.session_state:
        config = load_config()
        st.session_state["config"] = config
        st.session_state["authenticator"] = stauth.Authenticate(
            config["credentials"],
            config["cookie"]["name"],
            config["cookie"]["key"],
            config["cookie"]["expiry_days"],
        )
    return st.session_state["authenticator"], st.session_state["config"]


def restore_session():
    """
    Silently re-check the re-authentication cookie on every page load
    (no widget rendered). This is what keeps a user logged in as they
    click between Module pages.
    """
    authenticator, config = get_authenticator()
    try:
        authenticator.login(location="unrendered")
    except Exception:
        pass
    return authenticator, config


def require_login():
    """
    Call at the top of every protected page, right after apply_style().
    Halts the page with a friendly message if the user isn't logged in,
    since Streamlit's legacy pages/ sidebar always lists every page
    regardless of auth state.
    """
    authenticator, config = restore_session()
    if not st.session_state.get("authentication_status"):
        st.warning("Please log in from the Home page to view this module.")
        st.page_link("main.py", label="Go to Home / Login", icon="🏠")
        st.stop()
    return authenticator, config
