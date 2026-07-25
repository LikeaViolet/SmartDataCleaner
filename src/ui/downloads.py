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


def render_downloads(
    cleaned: pd.DataFrame,
    source: pd.DataFrame,
    report: CleaningReport,
    output_format: str,
) -> None:
    st.subheader("Downloads")

    text_bytes = format_text_report(
        report
    ).encode("utf-8")

    json_bytes = json.dumps(
        report_to_dict(report),
        indent=2,
        default=str,
    ).encode("utf-8")

    download_columns = st.columns(4)

    if output_format == "Excel":
        cleaned_bytes = dataframe_to_excel_bytes(cleaned)
        cleaned_name = "cleaned_dataset.xlsx"
        cleaned_mime = (
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        )
    else:
        cleaned_bytes = dataframe_to_csv_bytes(cleaned)
        cleaned_name = "cleaned_dataset.csv"
        cleaned_mime = "text/csv"

    download_columns[0].download_button(
        "Download cleaned data",
        data=cleaned_bytes,
        file_name=cleaned_name,
        mime=cleaned_mime,
        use_container_width=True,
    )

    download_columns[1].download_button(
        "Download text report",
        data=text_bytes,
        file_name="cleaning_report.txt",
        mime="text/plain",
        use_container_width=True,
    )

    download_columns[2].download_button(
        "Download JSON report",
        data=json_bytes,
        file_name="cleaning_report.json",
        mime="application/json",
        use_container_width=True,
    )

    download_columns[3].download_button(
        "Download original CSV",
        data=dataframe_to_csv_bytes(source),
        file_name="original_dataset.csv",
        mime="text/csv",
        use_container_width=True,
    )