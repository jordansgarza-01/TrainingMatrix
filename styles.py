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
COLOR_BURGUNDY = "#800002"  # sampled directly from the O&M favicon artwork
COLOR_MEDIUM_GREY = "#B8B8B8"

# RAG (Red/Amber/Green) status flag colors used across all training tables.
COLOR_RAG_GREEN_BG = "#E1F5E4"
COLOR_RAG_GREEN_TEXT = "#1E7B34"
COLOR_RAG_RED_BG = "#FBE2E2"
COLOR_RAG_RED_TEXT = "#B00020"
COLOR_RAG_YELLOW_BG = "#FFF6D8"
COLOR_RAG_YELLOW_TEXT = "#8A6D00"

RAG_COLORS = {
    "Yes": (COLOR_RAG_GREEN_BG, COLOR_RAG_GREEN_TEXT),
    "Complete": (COLOR_RAG_GREEN_BG, COLOR_RAG_GREEN_TEXT),
    "No": (COLOR_RAG_RED_BG, COLOR_RAG_RED_TEXT),
    "Incomplete": (COLOR_RAG_RED_BG, COLOR_RAG_RED_TEXT),
    "In Process": (COLOR_RAG_YELLOW_BG, COLOR_RAG_YELLOW_TEXT),
}

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

        /* Center the main content column; the sidebar stays left-aligned. */
        .block-container {{
            max-width: 1150px;
            margin-left: auto;
            margin-right: auto;
        }}
        .block-container h1,
        .block-container h2,
        .block-container h3,
        .om-header,
        .om-section-title,
        .om-context-line,
        .om-gap-box {{
            text-align: center;
        }}
        section[data-testid="stSidebar"] * {{
            text-align: left !important;
        }}

        /* Header / brand block — bright, white, thin burgundy rule */
        .om-header {{
            background-color: {COLOR_WHITE};
            padding: 1.25rem 1rem 1rem 1rem;
            margin-bottom: 1.5rem;
            border-bottom: 3px solid {COLOR_BURGUNDY};
        }}
        .om-header h1 {{
            color: {COLOR_BURGUNDY};
            font-size: 1.9rem;
            font-weight: 700;
            margin: 0;
            letter-spacing: 0.5px;
        }}
        .om-header h2 {{
            color: {COLOR_BLACK};
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

        /* Buttons — outlined, fills on hover for a brighter, sleeker look */
        div.stButton > button {{
            background-color: {COLOR_WHITE};
            color: {COLOR_BURGUNDY};
            border: 2px solid {COLOR_BURGUNDY};
            border-radius: 2px;
            padding: 0.5rem 1.5rem;
            font-weight: 600;
        }}
        div.stButton > button:hover {{
            background-color: {COLOR_BURGUNDY};
            color: {COLOR_WHITE};
            border: 2px solid {COLOR_BURGUNDY};
        }}
        div.stButton > button:disabled {{
            background-color: {COLOR_WHITE};
            color: {COLOR_MEDIUM_GREY};
            border: 2px solid {COLOR_MEDIUM_GREY};
        }}

        /* Metric cards */
        div[data-testid="stMetric"] {{
            background-color: {COLOR_WHITE};
            border: 1px solid {COLOR_LIGHT_GREY};
            border-left: 4px solid {COLOR_BURGUNDY};
            padding: 0.75rem 1rem;
        }}

        .om-gap-box {{
            background-color: {COLOR_WHITE};
            border: 1px solid {COLOR_BURGUNDY};
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

        /* Data tables rendered as plain HTML for full border/RAG control */
        table.om-data-table {{
            border-collapse: collapse;
            width: 100%;
            margin: 0.5rem auto 1.25rem auto;
        }}
        table.om-data-table th,
        table.om-data-table td {{
            border: 1px solid {COLOR_MEDIUM_GREY};
            padding: 0.5rem 0.85rem;
            text-align: left;
        }}
        table.om-data-table thead th {{
            background-color: {COLOR_BURGUNDY};
            color: {COLOR_WHITE};
        }}
        table.om-data-table tbody tr:nth-child(even) {{
            background-color: {COLOR_LIGHT_GREY};
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
