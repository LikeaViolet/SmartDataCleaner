from __future__ import annotations

from typing import Any

import pandas as pd
import streamlit as st

from src.models import CleaningReport


PRIORITY_ORDER = {
    "high": 0,
    "medium": 1,
    "low": 2,
}


def _recommendation_value(
    recommendation: Any,
    field: str,
    default: str = "",
) -> str:
    """
    Read recommendation values safely whether recommendations
    are dictionaries or Pydantic-style objects.
    """

    if isinstance(recommendation, dict):
        return str(recommendation.get(field, default))

    return str(getattr(recommendation, field, default))


def _sorted_recommendations(
    recommendations: list[Any],
) -> list[Any]:
    return sorted(
        recommendations,
        key=lambda item: PRIORITY_ORDER.get(
            _recommendation_value(
                item,
                "priority",
                "low",
            ).lower(),
            99,
        ),
    )


def render_ai_panel(report: CleaningReport) -> None:
    st.subheader("AI data quality insights")

    if report.ai_error:
        st.warning(
            "Cleaning succeeded, but AI insights were unavailable: "
            f"{report.ai_error}"
        )
        return

    if not report.ai_summary:
        st.info("AI insights were not requested for this run.")
        return

    recommendations = _sorted_recommendations(
        report.ai_recommendations
    )

    high_count = sum(
        _recommendation_value(
            recommendation,
            "priority",
        ).lower()
        == "high"
        for recommendation in recommendations
    )

    summary_columns = st.columns(4)

    summary_columns[0].metric(
        "Positive findings",
        len(report.ai_strengths),
    )

    summary_columns[1].metric(
        "Potential issues",
        len(report.ai_risks),
    )

    summary_columns[2].metric(
        "Recommendations",
        len(recommendations),
    )
    summary_columns[3].metric(
        "High priority",
        high_count,
    )

    (
        summary_tab,
        findings_tab,
        recommendations_tab,
    ) = st.tabs(
        [
            "Summary",
            "Strengths and risks",
            "Recommendations",
        ]
    )

    with summary_tab:
        st.write(report.ai_summary)

    with findings_tab:
        findings = []

        for strength in report.ai_strengths:
            findings.append(
                {
                    "Type": "Strength",
                    "Finding": strength,
                }
            )

        for risk in report.ai_risks:
            findings.append(
                {
                    "Type": "Risk",
                    "Finding": risk,
                }
            )

        if findings:
            st.dataframe(
                pd.DataFrame(findings),
                hide_index=True,
                use_container_width=True,
                column_config={
                    "Type": st.column_config.TextColumn(
                        "Type",
                        width="small",
                    ),
                    "Finding": st.column_config.TextColumn(
                        "Finding",
                        width="large",
                    ),
                },
            )
        else:
            st.write("No strengths or risks were returned.")

    with recommendations_tab:
        if not recommendations:
            st.write("No recommendations were returned.")
            return

        for position, recommendation in enumerate(
            recommendations,
            start=1,
        ):
            priority = _recommendation_value(
                recommendation,
                "priority",
                "low",
            ).upper()

            title = _recommendation_value(
                recommendation,
                "title",
                "Untitled recommendation",
            )

            category = _recommendation_value(
                recommendation,
                "category",
                "general",
            )

            explanation = _recommendation_value(
                recommendation,
                "explanation",
                "No explanation supplied.",
            )

            suggested_action = _recommendation_value(
                recommendation,
                "suggested_action",
                "No action supplied.",
            )

            label = (
                f"{position}. [{priority}] "
                f"{title} · {category.title()}"
            )

            with st.expander(
                label,
                expanded=False,
            ):
                st.markdown(f"**Why it matters**  \n{explanation}")

                st.markdown(
                    f"**Recommended action**  \n"
                    f"{suggested_action}"
                )