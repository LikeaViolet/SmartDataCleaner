from __future__ import annotations

import streamlit as st

from src.models import CleaningReport


def render_metrics(report: CleaningReport) -> None:
    quality = report.quality_score
    profile = report.dataset_profile

    st.subheader("Dataset overview")

    overview_columns = st.columns(5)

    overview_columns[0].metric(
        "Quality score",
        f"{quality.overall:.1f}%",
    )

    overview_columns[1].metric(
        "Grade",
        quality.grade,
    )

    overview_columns[2].metric(
        "Rows exported",
        report.output_rows,
        delta=report.output_rows - report.input_rows,
    )

    overview_columns[3].metric(
        "Duplicates removed",
        report.duplicate_rows_removed,
    )

    overview_columns[4].metric(
        "Original missing cells",
        profile.missing_cells,
    )

    st.subheader("Quality dimensions")

    quality_columns = st.columns(4)

    quality_columns[0].metric(
        "Completeness",
        f"{quality.completeness:.1f}%",
    )

    quality_columns[1].metric(
        "Validity",
        f"{quality.validity:.1f}%",
    )

    quality_columns[2].metric(
        "Uniqueness",
        f"{quality.uniqueness:.1f}%",
    )

    quality_columns[3].metric(
        "Consistency",
        f"{quality.consistency:.1f}%",
    )