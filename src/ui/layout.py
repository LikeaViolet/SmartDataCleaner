from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st

from src.cleaner import clean_dataset
from src.ui.ai_panel import render_ai_panel
from src.ui.downloads import render_downloads
from src.ui.profile import render_column_profile
from src.ui.footer import render_footer
from src.ui.header import render_header
from src.ui.metrics import (
    render_metrics,
    render_quality_dimensions,
)
from src.ui.charts import (
    render_missing_values_summary,
)



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

def prepare_display_dataframe(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Create a display-only copy with clearer validation statuses.

    The original cleaned dataframe is not modified, so downloads
    still contain plain values such as Valid, Missing, and Invalid.
    """

    display_dataframe = dataframe.copy()

    status_columns = [
        column
        for column in display_dataframe.columns
        if column.lower().endswith("status")
    ]

    status_labels = {
        "valid": "✓ Valid",
        "missing": "○ Missing",
        "invalid": "✕ Invalid",
        "standardized": "✓ Standardized",
    }

    for column in status_columns:
        display_dataframe[column] = (
            display_dataframe[column]
            .astype("string")
            .map(
                lambda value: (
                    status_labels.get(
                        str(value).strip().lower(),
                        value,
                    )
                    if pd.notna(value)
                    else value
                )
            )
        )

    return display_dataframe


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
    render_header()

    (
        generate_ai,
        title_case_input,
        output_format,
    ) = render_sidebar()

    upload_tab_label = "Upload"
    results_tab_label = "Results"
    download_tab_label = "Download"

    workflow_tabs = [
        upload_tab_label,
        results_tab_label,
        download_tab_label,
    ]

    tab_state_key = "workflow_tab_selection"
    pending_tab_key = "pending_workflow_tab"

    # Apply programmatic navigation before the tab
    # widget is created during this rerun.
    pending_tab = st.session_state.pop(
        pending_tab_key,
        None,
    )

    if pending_tab in workflow_tabs:
        st.session_state[
            tab_state_key
        ] = pending_tab

    current_tab = st.session_state.get(
        tab_state_key,
    )

    if current_tab not in workflow_tabs:
        st.session_state[
            tab_state_key
        ] = upload_tab_label

    upload_tab, results_tab, download_tab = st.tabs(
        workflow_tabs,
        default=upload_tab_label,
        key=tab_state_key,
        on_change=lambda: None,
    )

    uploaded_file = None

    with upload_tab:
        st.write(
            "Upload a CSV or Excel dataset to profile, "
            "clean, validate, and analyze it."
        )

        uploaded_file = st.file_uploader(
            "Upload a dataset",
            type=["csv", "xlsx", "xls"],
        )

        if uploaded_file is None:
            st.info(
                "Upload a dataset to begin."
            )

        else:
            try:
                source = read_uploaded_dataset(
                    uploaded_file
                )
            except Exception as exc:
                st.error(
                    "Could not read the uploaded dataset: "
                    f"{exc}"
                )
                source = None

            if source is not None:
                st.subheader(
                    "Original data preview"
                )

                st.dataframe(
                    source.head(100),
                    width="stretch",
                    hide_index=True,
                )

                title_case_columns = (
                    parse_title_case_columns(
                        title_case_input
                    )
                )

                if st.button(
                    "Clean dataset",
                    type="primary",
                    width="stretch",
                ):
                    with st.spinner(
                        "Cleaning and analyzing the "
                        "dataset..."
                    ):
                        try:
                            cleaned, report = (
                                clean_dataset(
                                    source,
                                    title_case_columns=(
                                        title_case_columns
                                    ),
                                    generate_ai=(
                                        generate_ai
                                    ),
                                )
                            )
                        except Exception as exc:
                            st.error(
                                "Cleaning failed: "
                                f"{exc}"
                            )
                        else:
                            st.session_state[
                                "cleaned_dataset"
                            ] = cleaned

                            st.session_state[
                                "cleaning_report"
                            ] = report

                            st.session_state[
                                "source_dataset"
                            ] = source

                            st.session_state[
                                "output_format"
                            ] = output_format

                            st.session_state[
                                "uploaded_name"
                            ] = uploaded_file.name

                            st.session_state[
                                "cleaning_completed_notice"
                            ] = True

                            st.session_state[
                                pending_tab_key
                            ] = results_tab_label

                            st.rerun()

    results_are_available = (
        "cleaned_dataset" in st.session_state
        and "cleaning_report" in st.session_state
        and "source_dataset" in st.session_state
    )

    if (
        results_are_available
        and uploaded_file is not None
        and st.session_state.get(
            "uploaded_name"
        )
        != uploaded_file.name
    ):
        results_are_available = False

    with results_tab:
        if not results_are_available:
            st.info(
                "Clean a dataset in the Upload tab "
                "to view results."
            )

        else:
            cleaned = st.session_state[
                "cleaned_dataset"
            ]

            report = st.session_state[
                "cleaning_report"
            ]

            if st.session_state.pop(
                "cleaning_completed_notice",
                False,
            ):
                st.success(
                    "Cleaning completed successfully."
                )

            overview_column, quality_column = (
                st.columns(
                    [2.15, 1],
                    gap="large",
                )
            )

            with overview_column:
                render_metrics(report)

            with quality_column:
                st.markdown(
                    "### Data quality"
                )

                with st.container(
                    border=True
                ):
                    (
                        dimensions_tab,
                        missing_tab,
                    ) = st.tabs(
                        [
                            "Dimensions",
                            "Missing values",
                        ]
                    )

                    with dimensions_tab:
                        render_quality_dimensions(
                            report
                        )

                    with missing_tab:
                        render_missing_values_summary(
                            report
                        )

            st.markdown(
                (
                    '<div class="'
                    'results-section-gap">'
                    "</div>"
                ),
                unsafe_allow_html=True,
            )

            (
                cleaned_data_tab,
                profile_tab,
                ai_tab,
            ) = st.tabs(
                [
                    "Cleaned data",
                    "Column profile",
                    "AI insights",
                ]
            )

            with cleaned_data_tab:
                display_dataframe = (
                    prepare_display_dataframe(
                        cleaned
                    )
                )

                status_columns = [
                    column
                    for column
                    in display_dataframe.columns
                    if column.lower().endswith(
                        "status"
                    )
                ]

                column_configuration = {
                    column: (
                        st.column_config.TextColumn(
                            column,
                            width="small",
                        )
                    )
                    for column in status_columns
                }

                st.dataframe(
                    display_dataframe,
                    width="stretch",
                    hide_index=True,
                    column_config=(
                        column_configuration
                    ),
                )

            with profile_tab:
                render_column_profile(
                    report
                )

            with ai_tab:
                render_ai_panel(
                    report
                )

            st.markdown(
                (
                    '<div class="'
                    'results-navigation-gap">'
                    "</div>"
                ),
                unsafe_allow_html=True,
            )

            (
                _,
                navigation_button,
                __,
            ) = st.columns(
                [1, 1.3, 1]
            )

            with navigation_button:
                if st.button(
                    "Continue to download",
                    type="primary",
                    width="stretch",
                ):
                    st.session_state[
                        pending_tab_key
                    ] = download_tab_label

                    st.rerun()

    with download_tab:
        if not results_are_available:
            st.info(
                "Clean a dataset in the Upload tab "
                "before downloading files."
            )

        else:
            cleaned = st.session_state[
                "cleaned_dataset"
            ]

            report = st.session_state[
                "cleaning_report"
            ]

            stored_source = st.session_state[
                "source_dataset"
            ]

            stored_output_format = (
                st.session_state[
                    "output_format"
                ]
            )

            back_column, _ = st.columns(
                [1, 4]
            )

            with back_column:
                if st.button(
                    "← Back to results",
                    type="tertiary",
                    width="stretch",
                ):
                    st.session_state[
                        pending_tab_key
                    ] = results_tab_label

                    st.rerun()

            st.subheader(
                "Cleaned dataset preview"
            )

            st.caption(
                "This preview shows the dataset "
                "included in the primary download."
            )

            st.dataframe(
                cleaned.head(100),
                width="stretch",
                hide_index=True,
            )

            render_downloads(
                cleaned=cleaned,
                source=stored_source,
                report=report,
                output_format=(
                    stored_output_format
                ),
            )

    render_footer()