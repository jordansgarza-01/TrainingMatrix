"""UI rendering utilities for the Streamlit training prototype."""

from __future__ import annotations

import os
from typing import Dict, List, Optional, Tuple

import pandas as pd
import streamlit as st

from data import (
    get_business_lines,
    get_supervisors_for_business_line,
    get_teammate_record,
    get_teammates_for_supervisor,
)

STEPS = {
    "select_context": "Business Line → Supervisor",
    "select_teammate": "Business Line → Supervisor → Teammate",
    "training_profile": "Business Line → Supervisor → Teammate → Training Profile",
}


def initialize_session_state() -> None:
    defaults = {
        "authenticated": False,
        "current_screen": "login",
        "selected_business_line": None,
        "selected_supervisor": None,
        "selected_teammate": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def render_header(step_key: str) -> None:
    st.markdown(
        f"""
        <div class="om-header">
            <p class="om-title">Owens &amp; Minor</p>
            <p class="om-subtitle">Teammate Training &amp; Development</p>
            <p class="om-breadcrumb">{STEPS.get(step_key, "")}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_logout() -> None:
    with st.sidebar:
        if st.session_state.get("authenticated"):
            st.markdown("### Session")
            if st.button("Logout", use_container_width=True):
                for key in [
                    "authenticated",
                    "current_screen",
                    "selected_business_line",
                    "selected_supervisor",
                    "selected_teammate",
                ]:
                    st.session_state[key] = None
                st.session_state["authenticated"] = False
                st.session_state["current_screen"] = "login"
                st.rerun()


def render_login_screen() -> None:
    st.markdown("## Owens & Minor")
    st.markdown("### Teammate Training & Development")

    configured_password = st.secrets.get("prototype_password") or os.getenv(
        "OM_TRAINING_APP_PASSWORD"
    )
    if not configured_password:
        st.error(
            "Application password is not configured. Set `prototype_password` in Streamlit "
            "secrets or set `OM_TRAINING_APP_PASSWORD` in your environment."
        )
        return

    password = st.text_input("Password", type="password")
    if st.button("Login", type="primary"):
        if password == configured_password:
            st.session_state["authenticated"] = True
            st.session_state["current_screen"] = "select_context"
            st.rerun()
        else:
            st.error("Invalid password. Please try again.")


def render_context_selection() -> None:
    render_header("select_context")

    business_lines = get_business_lines()
    current_business_line = st.selectbox(
        "Business Line",
        options=[""] + business_lines,
        index=(
            [""] + business_lines
        ).index(st.session_state["selected_business_line"])
        if st.session_state.get("selected_business_line") in business_lines
        else 0,
    )
    st.session_state["selected_business_line"] = current_business_line or None

    valid_supervisors = (
        get_supervisors_for_business_line(current_business_line)
        if current_business_line
        else []
    )

    if st.session_state.get("selected_supervisor") not in valid_supervisors:
        st.session_state["selected_supervisor"] = None
        st.session_state["selected_teammate"] = None

    supervisor = st.selectbox(
        "Supervisor",
        options=[""] + valid_supervisors,
        index=(
            [""] + valid_supervisors
        ).index(st.session_state["selected_supervisor"])
        if st.session_state.get("selected_supervisor") in valid_supervisors
        else 0,
    )
    st.session_state["selected_supervisor"] = supervisor or None

    continue_disabled = not (
        st.session_state.get("selected_business_line")
        and st.session_state.get("selected_supervisor")
    )

    if st.button("Continue", type="primary", disabled=continue_disabled):
        st.session_state["current_screen"] = "select_teammate"
        st.rerun()


def render_teammate_selection(records: List[Dict[str, object]]) -> None:
    render_header("select_teammate")

    business_line = st.session_state.get("selected_business_line")
    supervisor = st.session_state.get("selected_supervisor")

    if not business_line or not supervisor:
        st.warning("Please select both Business Line and Supervisor first.")
        if st.button("Back to Business Line & Supervisor"):
            st.session_state["current_screen"] = "select_context"
            st.rerun()
        return

    allowed_supervisors = get_supervisors_for_business_line(business_line)
    if supervisor not in allowed_supervisors:
        st.error("Selected Supervisor is not valid for the chosen Business Line.")
        st.session_state["selected_supervisor"] = None
        st.session_state["selected_teammate"] = None
        if st.button("Return to Selection"):
            st.session_state["current_screen"] = "select_context"
            st.rerun()
        return

    st.markdown("## Select Teammate")
    teammates = get_teammates_for_supervisor(records, supervisor, business_line)

    if not teammates:
        st.error("No teammate records found for this Supervisor.")
        return

    selected_teammate = st.selectbox(
        "Teammate",
        options=[""] + teammates,
        index=([""] + teammates).index(st.session_state["selected_teammate"])
        if st.session_state.get("selected_teammate") in teammates
        else 0,
    )

    st.session_state["selected_teammate"] = selected_teammate or None

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Back", use_container_width=True):
            st.session_state["current_screen"] = "select_context"
            st.rerun()
    with col2:
        if st.button(
            "View Training Profile",
            type="primary",
            disabled=not st.session_state.get("selected_teammate"),
            use_container_width=True,
        ):
            st.session_state["current_screen"] = "training_profile"
            st.rerun()


def _status_style(value: str) -> str:
    if value in {"No", "Incomplete"}:
        return "color: #6B1F2B; font-weight: 700; background-color: #F7ECEF"
    if value in {"Yes", "Complete"}:
        return "color: #36454F; font-weight: 700; background-color: #F7F7F7"
    return "color: #000000"


def _render_status_table(df: pd.DataFrame, status_column: str) -> None:
    styled = df.style.map(_status_style, subset=[status_column])
    st.table(styled)


def _calculate_metrics(record: Dict[str, object]) -> Dict[str, Tuple[int, int, int]]:
    job = record.get("job_function_training", {})
    mhe = record.get("mhe_certifications", {})
    etq = record.get("etq_training", {})

    job_complete = sum(1 for value in job.values() if value == "Yes")
    mhe_complete = sum(1 for value in mhe.values() if value == "Yes")
    etq_complete = sum(1 for value in etq.values() if value == "Complete")

    total_complete = job_complete + mhe_complete + etq_complete
    total_items = len(job) + len(mhe) + len(etq)
    pct = int(round((total_complete / total_items) * 100)) if total_items else 0

    return {
        "job": (job_complete, len(job), total_complete),
        "mhe": (mhe_complete, len(mhe), total_complete),
        "etq": (etq_complete, len(etq), total_complete),
        "overall": (total_complete, total_items, pct),
    }


def _training_gaps(record: Dict[str, object]) -> Dict[str, List[str]]:
    job = record.get("job_function_training", {})
    mhe = record.get("mhe_certifications", {})
    etq = record.get("etq_training", {})

    return {
        "job": [name for name, status in job.items() if status == "No"],
        "mhe": [name for name, status in mhe.items() if status == "No"],
        "etq": [name for name, status in etq.items() if status == "Incomplete"],
    }


def render_training_profile(records: List[Dict[str, object]]) -> None:
    render_header("training_profile")

    business_line = st.session_state.get("selected_business_line")
    supervisor = st.session_state.get("selected_supervisor")
    teammate = st.session_state.get("selected_teammate")

    if not all([business_line, supervisor, teammate]):
        st.warning("Please complete Business Line, Supervisor, and Teammate selections.")
        if st.button("Go to Selections"):
            st.session_state["current_screen"] = "select_context"
            st.rerun()
        return

    if supervisor not in get_supervisors_for_business_line(business_line):
        st.error("Invalid Business Line and Supervisor combination detected.")
        st.session_state["selected_supervisor"] = None
        st.session_state["selected_teammate"] = None
        if st.button("Fix Selection"):
            st.session_state["current_screen"] = "select_context"
            st.rerun()
        return

    record = get_teammate_record(records, business_line, supervisor, teammate)
    if not record:
        st.error("Teammate training record was not found.")
        return

    st.markdown("## Teammate Training Profile")
    st.markdown(
        f"**Business Line:** {business_line}  \\n**Supervisor:** {supervisor}  \\n**Teammate:** {teammate}"
    )

    metrics = _calculate_metrics(record)
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Job Functions Trained", f"{metrics['job'][0]} / {metrics['job'][1]}")
    c2.metric("MHE Certifications", f"{metrics['mhe'][0]} / {metrics['mhe'][1]}")
    c3.metric("ETQ Courses Complete", f"{metrics['etq'][0]} / {metrics['etq'][1]}")
    c4.metric("Total Training Items", f"{metrics['overall'][0]} / {metrics['overall'][1]}")
    c5.metric("Overall Completion %", f"{metrics['overall'][2]}%")

    job_df = pd.DataFrame(
        list(record.get("job_function_training", {}).items()),
        columns=["Job Function", "Training Status"],
    )
    mhe_df = pd.DataFrame(
        list(record.get("mhe_certifications", {}).items()),
        columns=["MHE / PIT Type", "Certified"],
    )
    etq_df = pd.DataFrame(
        list(record.get("etq_training", {}).items()),
        columns=["ETQ Training Group", "Status"],
    )

    if job_df.empty or mhe_df.empty or etq_df.empty:
        st.error("One or more training sections are empty for this teammate.")
        return

    st.markdown('<p class="om-section-title">Job Function Training</p>', unsafe_allow_html=True)
    _render_status_table(job_df, "Training Status")

    st.markdown('<p class="om-section-title">MHE Certification</p>', unsafe_allow_html=True)
    _render_status_table(mhe_df, "Certified")

    st.markdown('<p class="om-section-title">ETQ Training</p>', unsafe_allow_html=True)
    _render_status_table(etq_df, "Status")

    gaps = _training_gaps(record)
    st.markdown('<p class="om-section-title">Training Gaps</p>', unsafe_allow_html=True)

    if not any(gaps.values()):
        st.success("No training gaps identified. Teammate is fully complete across all sections.")
    else:
        if gaps["job"]:
            st.markdown(f"**Job Functions (No):** {', '.join(gaps['job'])}")
        if gaps["mhe"]:
            st.markdown(f"**MHE / PIT Types (No):** {', '.join(gaps['mhe'])}")
        if gaps["etq"]:
            st.markdown(f"**ETQ Groups (Incomplete):** {', '.join(gaps['etq'])}")

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Back to Teammate Selection", use_container_width=True):
            st.session_state["current_screen"] = "select_teammate"
            st.rerun()
    with col2:
        if st.button("Change Business Line / Supervisor", use_container_width=True):
            st.session_state["selected_teammate"] = None
            st.session_state["current_screen"] = "select_context"
            st.rerun()
