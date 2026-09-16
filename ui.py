"""
UI rendering functions for the Owens & Minor Teammate Training &
Development prototype.

Each screen in the application flow (login, business line/supervisor
selection, teammate selection, training profile) has a dedicated render
function here. UI logic is kept separate from the prototype data in
data.py so the data source can be replaced later without reworking the
screens themselves.
"""

import pandas as pd
import streamlit as st

import data
import styles

PLACEHOLDER_SUPERVISOR = "-- Select Supervisor --"
PLACEHOLDER_TEAMMATE = "-- Select Teammate --"


# ---------------------------------------------------------------------------
# Screen 1 — Login
# ---------------------------------------------------------------------------
def render_login_screen(app_password):
    """Render the password-gated login screen."""
    styles.render_header()
    st.subheader("Please log in to continue")

    with st.form("login_form"):
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Log In")

    if submitted:
        if password == app_password:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password. Please verify your credentials and try again.")


def render_session_sidebar():
    """Render the persistent sidebar showing current selections and logout."""
    with st.sidebar:
        st.markdown("### Current Selections")
        st.write(f"**Business Line:** {st.session_state.get('business_line') or 'Not selected'}")
        st.write(f"**Supervisor:** {st.session_state.get('supervisor') or 'Not selected'}")
        st.write(f"**Teammate:** {st.session_state.get('teammate') or 'Not selected'}")
        st.markdown("---")
        if st.button("Log Out", key="logout_button"):
            _reset_session(logout=True)
            st.rerun()


def _reset_session(logout=False):
    """Clear selection state; optionally also clear authentication."""
    st.session_state.business_line = None
    st.session_state.supervisor = None
    st.session_state.teammate = None
    if logout:
        st.session_state.authenticated = False


# ---------------------------------------------------------------------------
# Screen 2 — Business Line and Supervisor Selection
# ---------------------------------------------------------------------------
def render_business_line_supervisor_screen():
    """Render the Business Line / Supervisor selection screen."""
    styles.render_header(breadcrumb_stage="Business Line")
    st.subheader("Select Business Line and Supervisor")

    business_line = st.selectbox("Business Line", data.BUSINESS_LINES, key="business_line_widget")

    valid_supervisors = data.get_supervisors_for_business_line(business_line)

    # Keying the supervisor widget on the business line means it is
    # automatically rebuilt (and reset) whenever the business line changes,
    # instead of retaining a supervisor from an unrelated business line.
    supervisor_widget_key = f"supervisor_widget_{business_line}"
    supervisor_options = [PLACEHOLDER_SUPERVISOR] + valid_supervisors
    supervisor = st.selectbox("Supervisor", supervisor_options, key=supervisor_widget_key)

    has_valid_selection = business_line in data.BUSINESS_LINES and supervisor in valid_supervisors

    if st.button("Continue", disabled=not has_valid_selection):
        st.session_state.business_line = business_line
        st.session_state.supervisor = supervisor
        st.session_state.teammate = None
        st.rerun()


# ---------------------------------------------------------------------------
# Screen 3 — Teammate Selection
# ---------------------------------------------------------------------------
def render_teammate_selection_screen():
    """Render the Teammate selection screen for the chosen Supervisor."""
    business_line = st.session_state.business_line
    supervisor = st.session_state.supervisor

    styles.render_header(breadcrumb_stage="Teammate")
    st.markdown(
        f'<div class="om-context-line"><strong>Business Line:</strong> {business_line} '
        f'&nbsp;|&nbsp; <strong>Supervisor:</strong> {supervisor}</div>',
        unsafe_allow_html=True,
    )
    st.subheader("Select Teammate")

    teammates = data.get_teammates_for_supervisor(supervisor)
    if not teammates:
        st.error(
            "No teammates were found for this Supervisor. "
            "Please return to the previous screen and select a valid Supervisor."
        )
        if st.button("Back to Business Line / Supervisor Selection"):
            _reset_session()
            st.rerun()
        return

    def _on_teammate_change():
        selected = st.session_state.get("teammate_widget")
        if selected and selected != PLACEHOLDER_TEAMMATE:
            st.session_state.teammate = selected

    st.selectbox(
        "Teammate",
        [PLACEHOLDER_TEAMMATE] + teammates,
        key="teammate_widget",
        on_change=_on_teammate_change,
    )

    if st.button("Back to Business Line / Supervisor Selection"):
        _reset_session()
        st.rerun()


# ---------------------------------------------------------------------------
# Screen 4 — Teammate Training Matrix
# ---------------------------------------------------------------------------
def render_training_profile_screen():
    """Render the full training profile dashboard for the selected teammate."""
    business_line = st.session_state.business_line
    supervisor = st.session_state.supervisor
    teammate = st.session_state.teammate

    record = data.get_teammate_record(teammate)

    styles.render_header(breadcrumb_stage="Training Profile")

    if record is None:
        st.error(
            f"No training record could be found for '{teammate}'. "
            "Please select a different Teammate."
        )
        if st.button("Back to Teammate Selection"):
            st.session_state.teammate = None
            st.rerun()
        return

    st.markdown(
        f'<div class="om-context-line"><strong>Business Line:</strong> {business_line} '
        f'&nbsp;|&nbsp; <strong>Supervisor:</strong> {supervisor} '
        f'&nbsp;|&nbsp; <strong>Teammate:</strong> {teammate}</div>',
        unsafe_allow_html=True,
    )
    st.title("Teammate Training Profile")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Change Teammate"):
            st.session_state.teammate = None
            st.rerun()
    with col2:
        if st.button("Change Business Line / Supervisor"):
            _reset_session()
            st.rerun()

    _render_summary_metrics(record)
    _render_status_table(
        "Job Function Training", record["job_function_training"], "Job Function", "Training Status", "Yes"
    )
    _render_status_table(
        "MHE Certification", record["mhe_certifications"], "MHE / PIT Type", "Certified", "Yes"
    )
    _render_status_table(
        "ETQ Training", record["etq_training"], "ETQ Training Group", "Status", "Complete"
    )
    _render_training_gaps(record)


def _compute_summary_metrics(record):
    """Calculate summary metrics from a teammate's actual training record."""
    job_data = record["job_function_training"]
    mhe_data = record["mhe_certifications"]
    etq_data = record["etq_training"]

    job_trained = sum(1 for v in job_data.values() if v == "Yes")
    mhe_certified = sum(1 for v in mhe_data.values() if v == "Yes")
    etq_complete = sum(1 for v in etq_data.values() if v == "Complete")

    total_items = len(job_data) + len(mhe_data) + len(etq_data)
    total_complete = job_trained + mhe_certified + etq_complete
    overall_pct = round((total_complete / total_items) * 100) if total_items else 0

    return {
        "job_trained": job_trained, "job_total": len(job_data),
        "mhe_certified": mhe_certified, "mhe_total": len(mhe_data),
        "etq_complete": etq_complete, "etq_total": len(etq_data),
        "total_complete": total_complete, "total_items": total_items,
        "overall_pct": overall_pct,
    }


def _render_summary_metrics(record):
    """Render the top-of-page summary metric cards."""
    metrics = _compute_summary_metrics(record)

    cols = st.columns(5)
    cols[0].metric("Job Functions Trained", f"{metrics['job_trained']} / {metrics['job_total']}")
    cols[1].metric("MHE Certifications", f"{metrics['mhe_certified']} / {metrics['mhe_total']}")
    cols[2].metric("ETQ Complete", f"{metrics['etq_complete']} / {metrics['etq_total']}")
    cols[3].metric("Total Training Items", f"{metrics['total_complete']} / {metrics['total_items']}")
    cols[4].metric("Overall Completion", f"{metrics['overall_pct']}%")


def _render_status_table(title, status_dict, category_column, status_column, positive_value):
    """Render a reusable, conditionally formatted training status table."""
    st.markdown(f'<div class="om-section-title">{title}</div>', unsafe_allow_html=True)

    if not status_dict:
        st.info(f"No {title.lower()} records are available for this teammate.")
        return

    table_df = pd.DataFrame(
        [{category_column: item, status_column: status} for item, status in status_dict.items()]
    )

    def _highlight_negative(value):
        if value != positive_value:
            return f"color: {styles.COLOR_BURGUNDY}; font-weight: 700;"
        return f"color: {styles.COLOR_DARK_SLATE}; font-weight: 600;"

    styled_df = table_df.style.applymap(_highlight_negative, subset=[status_column])
    st.dataframe(styled_df, use_container_width=True, hide_index=True)


def _render_training_gaps(record):
    """Render the dynamically generated Training Gaps summary."""
    st.markdown('<div class="om-section-title">Training Gaps</div>', unsafe_allow_html=True)

    job_gaps = [item for item, status in record["job_function_training"].items() if status == "No"]
    mhe_gaps = [item for item, status in record["mhe_certifications"].items() if status == "No"]
    etq_gaps = [item for item, status in record["etq_training"].items() if status == "Incomplete"]

    if not (job_gaps or mhe_gaps or etq_gaps):
        st.markdown(
            '<div class="om-gap-box"><strong>No training gaps identified.</strong> '
            "This teammate is fully trained, certified, and current on all ETQ requirements.</div>",
            unsafe_allow_html=True,
        )
        return

    gap_lines = []
    if job_gaps:
        gap_lines.append(f"<strong>Job Functions not trained:</strong> {', '.join(job_gaps)}")
    if mhe_gaps:
        gap_lines.append(f"<strong>MHE / PIT types not certified:</strong> {', '.join(mhe_gaps)}")
    if etq_gaps:
        gap_lines.append(f"<strong>ETQ Training Groups incomplete:</strong> {', '.join(etq_gaps)}")

    gaps_html = "<br><br>".join(gap_lines)
    st.markdown(f'<div class="om-gap-box">{gaps_html}</div>', unsafe_allow_html=True)
