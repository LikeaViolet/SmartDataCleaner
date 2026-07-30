from __future__ import annotations

import pandas as pd
import streamlit as st

from src.models import CleaningReport


def render_column_profile(
    report: CleaningReport,
) -> None:
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

    profile_dataframe = pd.DataFrame(rows)

    st.dataframe(
        profile_dataframe,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Column": st.column_config.TextColumn(
                "Column",
                width="medium",
            ),
            "Detected type": st.column_config.TextColumn(
                "Semantic type",
                width="small",
            ),
            "Storage type": st.column_config.TextColumn(
                "Source dtype",
                width="small",
            ),
            "Non-missing": st.column_config.NumberColumn(
                "Present",
                format="%d",
            ),
            "Missing": st.column_config.NumberColumn(
                "Missing",
                format="%d",
            ),
            "Missing %": st.column_config.NumberColumn(
                "Missing %",
                format="%.1f%%",
            ),
            "Unique values": st.column_config.NumberColumn(
                "Unique",
                format="%d",
            ),
            "Unique %": st.column_config.NumberColumn(
                "Unique %",
                format="%.1f%%",
            ),
        },
    )