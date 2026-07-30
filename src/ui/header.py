from __future__ import annotations

import streamlit as st


def render_header() -> None:
    left, right = st.columns(
        [4, 1],
        vertical_alignment="center",
    )

    with left:
        st.title("Smart Data Cleaner")

        st.caption(
            "Profile, clean, validate, and analyze CSV and Excel datasets."
        )

    with right:
        st.markdown(
            """
            <div style="
                text-align: right;
                font-size: 0.85rem;
                color: #6B7280;
                padding-top: 0.5rem;
            ">
                Version 1.0.0
            </div>
            """,
            unsafe_allow_html=True,
        )