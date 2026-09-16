"""
Owens & Minor visual design system for the Streamlit application.

Centralizes the corporate color palette and injects the CSS theme so the
look and feel stays consistent across every screen.
"""

import streamlit as st

# ---------------------------------------------------------------------------
# Owens & Minor corporate color palette
# ---------------------------------------------------------------------------
COLOR_WHITE = "#FFFFFF"
COLOR_BLACK = "#000000"
COLOR_LIGHT_GREY = "#E6E6E6"
COLOR_BURGUNDY = "#6B1F2B"
COLOR_MEDIUM_GREY = "#B8B8B8"

WORKFLOW_STAGES = ["Business Line", "Supervisor", "Teammate", "Training Profile"]


def apply_custom_styles():
    """Inject the Owens & Minor corporate CSS theme into the page."""
    st.markdown(
        f"""
        <style>
        html, body, [class*="css"] {{
            font-family: "Segoe UI", Helvetica, Arial, sans-serif;
            color: {COLOR_BLACK};
        }}

        .stApp {{
            background-color: {COLOR_WHITE};
        }}

        /* Header / brand block */
        .om-header {{
            background-color: {COLOR_BURGUNDY};
            padding: 1.5rem 2rem;
            margin-bottom: 1.5rem;
            border-left: 6px solid {COLOR_BLACK};
        }}
        .om-header h1 {{
            color: {COLOR_WHITE};
            font-size: 1.8rem;
            font-weight: 700;
            margin: 0;
            letter-spacing: 0.5px;
        }}
        .om-header h2 {{
            color: {COLOR_LIGHT_GREY};
            font-size: 1.05rem;
            font-weight: 400;
            margin: 0.25rem 0 0 0;
        }}
        .om-breadcrumb {{
            color: {COLOR_MEDIUM_GREY};
            font-size: 0.9rem;
            margin-top: 0.75rem;
        }}
        .om-breadcrumb span.active {{
            color: {COLOR_BURGUNDY};
            font-weight: 700;
        }}

        /* Section headings */
        .om-section-title {{
            color: {COLOR_BURGUNDY};
            font-size: 1.2rem;
            font-weight: 700;
            border-bottom: 2px solid {COLOR_BURGUNDY};
            padding-bottom: 0.3rem;
            margin-top: 1.75rem;
            margin-bottom: 0.75rem;
        }}

        /* Buttons */
        div.stButton > button {{
            background-color: {COLOR_BURGUNDY};
            color: {COLOR_WHITE};
            border: none;
            border-radius: 2px;
            padding: 0.5rem 1.5rem;
            font-weight: 600;
        }}
        div.stButton > button:hover {{
            background-color: {COLOR_LIGHT_GREY};
            color: {COLOR_BURGUNDY};
        }}
        div.stButton > button:disabled {{
            background-color: {COLOR_MEDIUM_GREY};
            color: {COLOR_LIGHT_GREY};
        }}

        /* Metric cards */
        div[data-testid="stMetric"] {{
            background-color: {COLOR_LIGHT_GREY};
            padding: 0.75rem 1rem;
            border-left: 4px solid {COLOR_BURGUNDY};
        }}

        /* Tables */
        thead tr th {{
            background-color: {COLOR_BURGUNDY} !important;
            color: {COLOR_WHITE} !important;
        }}

        .om-gap-box {{
            background-color: {COLOR_LIGHT_GREY};
            border-left: 4px solid {COLOR_BURGUNDY};
            padding: 1rem;
            margin-top: 0.5rem;
        }}

        .om-context-line {{
            font-size: 1.05rem;
            margin-bottom: 0.25rem;
        }}
        .om-context-line strong {{
            color: {COLOR_BURGUNDY};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header(breadcrumb_stage=None):
    """Render the persistent Owens & Minor application header."""
    breadcrumb_html = ""
    if breadcrumb_stage:
        parts = []
        for stage in WORKFLOW_STAGES:
            css_class = "active" if stage == breadcrumb_stage else ""
            parts.append(f'<span class="{css_class}">{stage}</span>')
        breadcrumb_html = f'<div class="om-breadcrumb">{" &rarr; ".join(parts)}</div>'

    st.markdown(
        f"""
        <div class="om-header">
            <h1>Owens &amp; Minor</h1>
            <h2>Teammate Training &amp; Development</h2>
            {breadcrumb_html}
        </div>
        """,
        unsafe_allow_html=True,
    )
