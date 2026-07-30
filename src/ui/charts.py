from __future__ import annotations

import altair as alt
import pandas as pd
import streamlit as st

from src.models import CleaningReport


def build_missing_values_dataframe(
    report: CleaningReport,
) -> pd.DataFrame:
    rows: list[dict[str, object]] = []

    denominator = max(report.input_rows, 1)

    for column, count in (
        report.missing_values_by_column.items()
    ):
        if count <= 0:
            continue

        rows.append(
            {
                "Column": column,
                "Missing values": int(count),
                "Missing %": (
                    float(count) / denominator
                ) * 100,
            }
        )

    if not rows:
        return pd.DataFrame(
            columns=[
                "Column",
                "Missing values",
                "Missing %",
            ]
        )

    return (
        pd.DataFrame(rows)
        .sort_values(
            by=["Missing %", "Column"],
            ascending=[False, True],
        )
        .reset_index(drop=True)
    )

def render_missing_values_summary(
    report: CleaningReport,
) -> None:
    missing_data = build_missing_values_dataframe(
        report
    )

    if missing_data.empty:
        st.success(
            "No missing values were detected."
        )
        return

    for row in missing_data.itertuples(index=False):
        column = row[0]
        missing_percentage = float(row[2])

        st.progress(
            missing_percentage / 100,
            text=(
                f"**{column}** · "
                f"{missing_percentage:.1f}%"
            ),
        )


