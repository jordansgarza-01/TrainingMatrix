"""Owens & Minor — Teammate Training & Development Streamlit prototype."""

from __future__ import annotations

import streamlit as st

from data import load_training_data
from styles import apply_styles
from ui import (
    initialize_session_state,
    render_context_selection,
    render_login_screen,
    render_logout,
    render_teammate_selection,
    render_training_profile,
)

st.set_page_config(
    page_title="Owens & Minor — Teammate Training & Development",
    layout="wide",
)


@st.cache_data
def get_training_records():
    return load_training_data()


def main() -> None:
    apply_styles()
    initialize_session_state()

    records = get_training_records()

    if not st.session_state.get("authenticated"):
        render_login_screen()
        return

    render_logout()

    screen = st.session_state.get("current_screen", "select_context")
    if screen == "select_context":
        render_context_selection()
    elif screen == "select_teammate":
        render_teammate_selection(records)
    elif screen == "training_profile":
        render_training_profile(records)
    else:
        st.session_state["current_screen"] = "select_context"
        render_context_selection()


if __name__ == "__main__":
    main()
