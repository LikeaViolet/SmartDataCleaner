from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st

from src.cleaner import clean_dataset
from src.ui.ai_panel import render_ai_panel
from src.ui.downloads import render_downloads
from src.ui.metrics import render_metrics
from src.ui.profile import render_column_profile


def read_uploaded_dataset(
    uploaded_file: Any,
) -> pd.DataFrame:
    suffix = Path(uploaded_file.name).suffix.lower()

    if suffix == ".csv":
        return pd.read_csv(uploaded_file)

    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(uploaded_file)

    raise ValueError(
        "Unsupported file type. Upload a CSV, XLSX, or XLS file."
    )


def parse_title_case_columns(value: str) -> list[str]:
    return [
        column.strip()
        for column in value.split(",")
        if column.strip()
    ]


def render_sidebar() -> tuple[bool, str, str]:
    with st.sidebar:
        st.header("Cleaning options")

        generate_ai = st.toggle(
            "Generate AI insights",
            value=False,
            help=(
                "Uses the configured OpenAI API key to "
                "analyze the deterministic cleaning report."
            ),
        )

        title_case_input = st.text_input(
            "Title-case columns",
            placeholder="Name, City",
            help=(
                "Enter column headers, not data values. "
                "Example: Name, City"
            )
        )

        output_format = st.selectbox(
            "Cleaned file format",
            options=["Excel", "CSV"],
        )

    return (
        generate_ai,
        title_case_input,
        output_format,
    )


def render_app() -> None:
    st.title("Smart Data Cleaner")

    st.write(
        "Upload a CSV or Excel dataset to profile, clean, "
        "validate, and analyze it."
    )

    (
        generate_ai,
        title_case_input,
        output_format,
    ) = render_sidebar()

    uploaded_file = st.file_uploader(
        "Upload a dataset",
        type=["csv", "xlsx", "xls"],
    )

    if uploaded_file is None:
        st.info("Upload a dataset to begin.")
        return

    try:
        source = read_uploaded_dataset(uploaded_file)
    except Exception as exc:
        st.error(
            f"Could not read the uploaded dataset: {exc}"
        )
        return

    st.subheader("Original data preview")

    st.dataframe(
        source.head(100),
        use_container_width=True,
    )

    title_case_columns = parse_title_case_columns(
        title_case_input
    )

    if st.button(
        "Clean dataset",
        type="primary",
        use_container_width=True,
    ):
        with st.spinner(
            "Cleaning and analyzing the dataset..."
        ):
            try:
                cleaned, report = clean_dataset(
                    source,
                    title_case_columns=title_case_columns,
                    generate_ai=generate_ai,
                )
            except Exception as exc:
                st.error(f"Cleaning failed: {exc}")
                return

        st.session_state["cleaned_dataset"] = cleaned
        st.session_state["cleaning_report"] = report
        st.session_state["source_dataset"] = source
        st.session_state["output_format"] = output_format
        st.session_state["uploaded_name"] = uploaded_file.name

    if "cleaned_dataset" not in st.session_state:
        return

    if (
        st.session_state.get("uploaded_name")
        != uploaded_file.name
    ):
        return

    cleaned = st.session_state["cleaned_dataset"]
    report = st.session_state["cleaning_report"]
    stored_source = st.session_state["source_dataset"]
    stored_output_format = st.session_state[
        "output_format"
    ]

    st.success("Cleaning completed successfully.")

    render_metrics(report)

    st.subheader("Cleaned data")

    st.dataframe(
        cleaned,
        use_container_width=True,
    )

    render_column_profile(report)
    render_ai_panel(report)

    render_downloads(
        cleaned=cleaned,
        source=stored_source,
        report=report,
        output_format=stored_output_format,
    )