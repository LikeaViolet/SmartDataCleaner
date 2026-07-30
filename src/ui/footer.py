from __future__ import annotations

import streamlit as st


def render_footer() -> None:
    st.divider()

    st.markdown(
        """
        <div style="
            text-align: center;
            color: #8A8F9C;
            font-size: 0.82rem;
            padding: 8px 0 20px 0;
        ">
            Smart Data Cleaner v1.0.0 ·
            Deterministic validation with optional AI insights
        </div>
        """,
        unsafe_allow_html=True,
    )