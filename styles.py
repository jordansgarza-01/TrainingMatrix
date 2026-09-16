"""Styling for Owens & Minor Teammate Training & Development."""

from __future__ import annotations

import streamlit as st


def apply_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --om-white: #FFFFFF;
            --om-black: #000000;
            --om-light-grey: #E6E6E6;
            --om-dark-slate: #36454F;
            --om-burgundy: #6B1F2B;
            --om-medium-grey: #B8B8B8;
        }

        .stApp {
            background-color: var(--om-white);
            color: var(--om-black);
            font-family: "Segoe UI", "Arial", sans-serif;
        }

        .om-header {
            border-bottom: 2px solid var(--om-light-grey);
            padding-bottom: 0.6rem;
            margin-bottom: 1rem;
        }

        .om-title {
            color: var(--om-dark-slate);
            font-size: 1.9rem;
            font-weight: 700;
            margin: 0;
        }

        .om-subtitle {
            color: var(--om-black);
            font-size: 1rem;
            margin: 0.1rem 0 0.4rem 0;
            font-weight: 500;
        }

        .om-breadcrumb {
            color: var(--om-burgundy);
            font-size: 0.9rem;
            font-weight: 600;
            letter-spacing: 0.01em;
        }

        .om-section-title {
            color: var(--om-burgundy);
            font-size: 1.05rem;
            font-weight: 700;
            margin-top: 1.1rem;
        }

        .om-muted {
            color: var(--om-dark-slate);
            font-size: 0.92rem;
        }

        .stButton > button {
            border: 1px solid var(--om-dark-slate);
            background: var(--om-dark-slate);
            color: var(--om-white);
            font-weight: 600;
            border-radius: 0.25rem;
        }

        .stButton > button:hover {
            border-color: var(--om-burgundy);
            background: var(--om-burgundy);
            color: var(--om-white);
        }

        .stTextInput input, .stSelectbox div[data-baseweb="select"] > div {
            border-color: var(--om-medium-grey);
        }

        [data-testid="stMetricValue"] {
            color: var(--om-dark-slate);
            font-weight: 700;
        }

        [data-testid="stMetricLabel"] {
            color: var(--om-black);
            font-weight: 600;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
