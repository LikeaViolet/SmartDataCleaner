from __future__ import annotations

import streamlit as st

from src.models import CleaningReport


def render_ai_panel(report: CleaningReport) -> None:
    st.subheader("AI data quality insights")

    if report.ai_summary:
        st.markdown("#### Summary")
        st.write(report.ai_summary)

        left_column, right_column = st.columns(2)

        with left_column:
            st.markdown("#### Strengths")

            if report.ai_strengths:
                for strength in report.ai_strengths:
                    st.write(f"• {strength}")
            else:
                st.write("No strengths returned.")

        with right_column:
            st.markdown("#### Risks")

            if report.ai_risks:
                for risk in report.ai_risks:
                    st.write(f"• {risk}")
            else:
                st.write("No risks returned.")

        st.markdown("#### Recommendations")

        if not report.ai_recommendations:
            st.write("No recommendations returned.")
            return

        for recommendation in report.ai_recommendations:
            priority = recommendation["priority"].upper()
            title = recommendation["title"]

            with st.expander(f"[{priority}] {title}"):
                st.write(
                    f"**Category:** "
                    f"{recommendation['category']}"
                )
                st.write(
                    f"**Why:** "
                    f"{recommendation['explanation']}"
                )
                st.write(
                    f"**Suggested action:** "
                    f"{recommendation['suggested_action']}"
                )

    elif report.ai_error:
        st.warning(
            "Cleaning succeeded, but AI insights were "
            f"unavailable: {report.ai_error}"
        )

    else:
        st.info(
            "AI insights were not requested for this run."
        )