from __future__ import annotations

import pandas as pd
import streamlit as st

from src.models import CleaningReport


def render_column_profile(
    report: CleaningReport,
) -> None:
    st.subheader("Column profile")

    rows = [
        {
            "Column": column.name,
            "Detected type": (
                column.detected_type or "general"
            ),
            "Storage type": column.dtype,
            "Non-missing": column.non_missing,
            "Missing": column.missing,
            "Missing %": column.missing_percentage,
            "Unique values": column.unique_values,
            "Unique %": column.unique_percentage,
        }
        for column in report.dataset_profile.column_profiles
    ]

    st.dataframe(
        pd.DataFrame(rows),
        use_container_width=True,
        hide_index=True,
    )