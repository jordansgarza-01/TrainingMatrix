"""
Owens & Minor — Teammate Training & Development
Streamlit application entry point.

Run with: streamlit run app.py
"""

import os

import streamlit as st

import styles
import ui

st.set_page_config(
    page_title="Owens & Minor | Teammate Training & Development Platform",
    page_icon="O&M (3).png",
    layout="wide",
)

# Prototype hard-coded password. For a production deployment, replace this
# with st.secrets["app_password"] or an environment variable backed by an
# enterprise authentication system (SSO, Active Directory, etc.).
APP_PASSWORD = os.environ.get("OM_APP_PASSWORD", "Platinum2025")


def _init_session_state():
    """Ensure every session-state key used by the app flow exists."""
    defaults = {
        "authenticated": False,
        "business_line": None,
        "supervisor": None,
        "teammate": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def main():
    styles.apply_custom_styles()
    _init_session_state()

    if not st.session_state.authenticated:
        ui.render_login_screen(APP_PASSWORD)
        return

    ui.render_session_sidebar()

    # Route to the correct screen based on how far the user has progressed
    # through Business Line -> Supervisor -> Teammate -> Training Profile.
    if not st.session_state.business_line or not st.session_state.supervisor:
        ui.render_business_line_supervisor_screen()
    elif not st.session_state.teammate:
        ui.render_teammate_selection_screen()
    else:
        ui.render_training_profile_screen()


if __name__ == "__main__":
    main()
