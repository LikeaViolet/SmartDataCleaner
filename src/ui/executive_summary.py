from __future__ import annotations

import streamlit as st

from src.models import CleaningReport


def build_executive_summary(
    report: CleaningReport,
) -> list[str]:
    quality = report.quality_score
    profile = report.dataset_profile

    findings = [
        (
            f"Dataset quality is {quality.grade.lower()} "
            f"at {quality.overall:.1f}%."
        ),
        (
            f"{report.duplicate_rows_removed} duplicate "
            f"{'record was' if report.duplicate_rows_removed == 1 else 'records were'} "
            "removed."
        ),
        (
            f"{profile.missing_cells} missing "
            f"{'cell remains' if profile.missing_cells == 1 else 'cells remain'}."
        ),
    ]

    if profile.missing_cells > 0:
        findings.append(
            "Recommended next step: review and resolve missing "
            "values before importing the dataset."
        )
    elif quality.overall >= 90:
        findings.append(
            "Recommended next step: the dataset is ready for "
            "final review or import."
        )
    else:
        findings.append(
            "Recommended next step: review the remaining data "
            "quality findings before import."
        )

    return findings


def render_executive_summary(
    report: CleaningReport,
) -> None:
    findings = build_executive_summary(report)

    st.markdown("#### Executive summary")

    with st.container(border=True):
        st.markdown(
            "\n".join(
                f"- {finding}"
                for finding in findings
            )
        )