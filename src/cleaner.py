# Cleaning workflow
from __future__ import annotations

from typing import Iterable

import pandas as pd

from src.models import CleaningReport
from src.pipeline.blank_rows import remove_blank_rows
from src.pipeline.dates import normalize_date_column
from src.pipeline.duplicate_cleaner import remove_duplicates
from src.pipeline.email import validate_email_column
from src.pipeline.phone import normalize_phone_column
from src.pipeline.currency import normalize_currency_column
from src.pipeline.text_cleaner import (
    title_case_columns as apply_title_case,
    trim_text_columns,
)
from src.pipeline.zip_code import normalize_zip_code_column
from src.column_detection import detect_columns
from src.profiling import profile_dataset
from src.ai_insights import generate_ai_insights
from src.quality import calculate_quality_score

from src.pipeline.broker_activity import (
    calculate_broker_missing_values,
    is_broker_activity_dataframe,
    normalize_broker_activity,
    repair_broker_activity_headers,
)


def clean_dataset(
    df: pd.DataFrame,
    title_case_columns: Iterable[str] | None = None,
    generate_ai: bool = False,
) -> tuple[pd.DataFrame, CleaningReport]:

    """
    Clean a dataset safely.

    Operations:
    - Remove completely blank rows.
    - Trim leading and trailing spaces from text cells.
    - Remove exact duplicate rows.
    - Validate email addresses when an Email column exists.
    - Normalize phone numbers when a Phone column exists.
    - Normalize dates when a Date column exists.
    - Normalize US ZIP codes when a ZIP column exists.
    - Optionally title-case explicitly selected columns.
    """

    broker_activity_detected = (
        is_broker_activity_dataframe(df)
    )

    working_dataframe = df.copy()

    if broker_activity_detected:
        working_dataframe = (
            repair_broker_activity_headers(
                working_dataframe
            )
        )

    original_columns = list(
        working_dataframe.columns
    )

    input_rows = len(working_dataframe)

    dataset_profile = profile_dataset(
        working_dataframe
    )

    cleaned, blank_rows_removed = remove_blank_rows(
        working_dataframe
    )

    cleaned, text_cells_trimmed = trim_text_columns(cleaned)

    (
        cleaned,
        duplicate_rows_removed,
        removed_duplicate_rows,
    ) = remove_duplicates(cleaned)

    if broker_activity_detected:
        cleaned = normalize_broker_activity(
            cleaned
        )

    detected_columns = detect_columns(
        cleaned,
        field_types=[
            "email",
            "phone",
            "zip",
            "address",
            "date",
            "currency",
        ],
    )

    email_column = detected_columns["email"]
    phone_column = detected_columns["phone"]
    zip_column = detected_columns["zip"]
    address_column = detected_columns["address"]
    date_column = detected_columns["date"]
    currency_column = detected_columns["currency"]

    email_result = validate_email_column(
        cleaned,
        column_name=email_column,
    )
    cleaned = email_result.dataframe

    phone_result = normalize_phone_column(
        cleaned,
        column_name=phone_column,
    )
    cleaned = phone_result.dataframe

    if broker_activity_detected:
        date_result = normalize_date_column(
            cleaned,
            column_name=None,
        )
    else:
        date_result = normalize_date_column(
            cleaned,
            column_name=date_column,
        )

    cleaned = date_result.dataframe

    zip_result = normalize_zip_code_column(
        cleaned,
        column_name=zip_column,
    )
    cleaned = zip_result.dataframe

    if broker_activity_detected:
        currency_result = normalize_currency_column(
            cleaned,
            column_name=None,
        )
    else:
        currency_result = normalize_currency_column(
            cleaned,
            column_name=currency_column,
        )

    cleaned = currency_result.dataframe

    valid_emails = email_result.valid
    invalid_emails = email_result.invalid
    missing_emails = email_result.missing

    valid_phones = phone_result.valid
    invalid_phones = phone_result.invalid
    missing_phones = phone_result.missing
    phone_numbers_standardized = phone_result.standardized

    valid_dates = date_result.valid
    invalid_dates = date_result.invalid
    missing_dates = date_result.missing
    dates_standardized = date_result.standardized

    valid_zip_codes = zip_result.valid
    invalid_zip_codes = zip_result.invalid
    missing_zip_codes = zip_result.missing
    zip_codes_standardized = zip_result.standardized

    valid_currency_values = currency_result.valid
    invalid_currency_values = currency_result.invalid
    missing_currency_values = currency_result.missing
    currency_values_standardized = currency_result.standardized

    cleaned, title_case_cells_changed = apply_title_case(
        cleaned,
        title_case_columns,
    )

    if broker_activity_detected:
        (
            missing_values,
            total_data_cells,
        ) = calculate_broker_missing_values(
            cleaned
        )
    else:
        missing_values = {
            str(column): int(
                cleaned[column].isna().sum()
            )
            for column in original_columns
            if column in cleaned.columns
        }

        total_data_cells = (
                len(cleaned)
                * len(original_columns)
        )

    missing_data_cells = sum(
        missing_values.values()
    )

    validation_checks = (
            valid_emails
            + invalid_emails
            + valid_phones
            + invalid_phones
            + valid_zip_codes
            + invalid_zip_codes
            + valid_dates
            + invalid_dates
            + valid_currency_values
            + invalid_currency_values
    )

    invalid_values = (
            invalid_emails
            + invalid_phones
            + invalid_zip_codes
            + invalid_dates
            + invalid_currency_values
    )



    quality_score = calculate_quality_score(
        input_rows=input_rows - blank_rows_removed,
        output_rows=len(cleaned),
        total_data_cells=total_data_cells,
        missing_data_cells=missing_data_cells,
        validation_checks=validation_checks,
        invalid_values=invalid_values,
        duplicate_rows_removed=duplicate_rows_removed,
    )

    report = CleaningReport(
        dataset_profile=dataset_profile,
        input_rows=input_rows,
        output_rows=len(cleaned),
        blank_rows_removed=blank_rows_removed,
        duplicate_rows_removed=duplicate_rows_removed,
        removed_duplicate_rows=(
            removed_duplicate_rows.to_dict(
                orient="records"
            )
        ),
        text_cells_trimmed=text_cells_trimmed,
        title_case_cells_changed=title_case_cells_changed,

        valid_emails=valid_emails,
        invalid_emails=invalid_emails,
        missing_emails=missing_emails,

        valid_phones=valid_phones,
        invalid_phones=invalid_phones,
        missing_phones=missing_phones,
        phone_numbers_standardized=phone_numbers_standardized,

        valid_zip_codes=valid_zip_codes,
        invalid_zip_codes=invalid_zip_codes,
        missing_zip_codes=missing_zip_codes,
        zip_codes_standardized=zip_codes_standardized,

        valid_dates=valid_dates,
        invalid_dates=invalid_dates,
        missing_dates=missing_dates,
        dates_standardized=dates_standardized,

        valid_currency_values=valid_currency_values,
        invalid_currency_values=invalid_currency_values,
        missing_currency_values=missing_currency_values,
        currency_values_standardized=currency_values_standardized,

        missing_values_by_column=missing_values,
        quality_score=quality_score,
    )

    if generate_ai:
        ai_result = generate_ai_insights(report)

        if ai_result.insights is not None:
            insights = ai_result.insights

            report.ai_summary = insights.summary
            report.ai_strengths = insights.strengths
            report.ai_risks = insights.risks
            report.ai_recommendations = [
                recommendation.model_dump()
                for recommendation in insights.recommendations
            ]

        report.ai_error = ai_result.error



    return cleaned, report