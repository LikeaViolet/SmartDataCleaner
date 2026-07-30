from __future__ import annotations

import json

import pandas as pd
import streamlit as st

from src.export_utils import (
    dataframe_to_csv_bytes,
    dataframe_to_excel_bytes,
)
from src.models import CleaningReport
from src.reporting import (
    format_text_report,
    report_to_dict,
)


def _inject_download_styles() -> None:
    st.markdown(
        """
        <style>
        div[data-testid="stDownloadButton"] {
            display: flex;
            justify-content: center;
        }

        div[data-testid="stDownloadButton"] > button {
            width: 100%;
            min-height: 2.85rem;
            border-radius: 13px;
            font-weight: 600;
            letter-spacing: 0.005em;
            transition:
                transform 150ms ease,
                box-shadow 150ms ease;
        }

        div[data-testid="stDownloadButton"]
        > button[kind="primary"] {
            width: min(21rem, 100%);
            min-height: 3.15rem;
            margin-inline: auto;
            border: 0;
            border-radius: 16px;
            box-shadow:
                0 8px 22px rgba(240, 79, 100, 0.18);
        }

        div[data-testid="stDownloadButton"]
        > button[kind="primary"]:hover {
            transform: translateY(-1px);
            box-shadow:
                0 11px 27px rgba(240, 79, 100, 0.24);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_downloads(
    cleaned: pd.DataFrame,
    source: pd.DataFrame,
    report: CleaningReport,
    output_format: str,
) -> None:
    _inject_download_styles()

    st.subheader("Downloads")

    text_bytes = format_text_report(
        report
    ).encode("utf-8")

    json_bytes = json.dumps(
        report_to_dict(report),
        indent=2,
        default=str,
    ).encode("utf-8")

    if output_format == "Excel":
        removed_duplicates = pd.DataFrame(
            report.removed_duplicate_rows
        )

        cleaned_bytes = dataframe_to_excel_bytes(
            cleaned,
            removed_duplicates=removed_duplicates,
        )
        cleaned_name = "cleaned_dataset.xlsx"
        cleaned_mime = (
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        )
    else:
        cleaned_bytes = dataframe_to_csv_bytes(
            cleaned
        )
        cleaned_name = "cleaned_dataset.csv"
        cleaned_mime = "text/csv"

    st.download_button(
        "Download cleaned dataset",
        data=cleaned_bytes,
        file_name=cleaned_name,
        mime=cleaned_mime,
        type="primary",
        use_container_width=False,
    )

    report_columns = st.columns(3)

    report_columns[0].download_button(
        "Text report",
        data=text_bytes,
        file_name="cleaning_report.txt",
        mime="text/plain",
        use_container_width=True,
    )

    report_columns[1].download_button(
        "JSON report",
        data=json_bytes,
        file_name="cleaning_report.json",
        mime="application/json",
        use_container_width=True,
    )

    report_columns[2].download_button(
        "Original data",
        data=dataframe_to_csv_bytes(source),
        file_name="original_dataset.csv",
        mime="text/csv",
        use_container_width=True,
    )