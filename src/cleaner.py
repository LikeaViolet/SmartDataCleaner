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
from src.pipeline.text_cleaner import (
    title_case_columns as apply_title_case,
    trim_text_columns,
)
from src.pipeline.zip_code import normalize_zip_code_column
from src.column_detection import detect_columns
from src.quality import calculate_quality_score


def clean_dataset(
    df: pd.DataFrame,
    title_case_columns: Iterable[str] | None = None,
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


    original_columns = list(df.columns)

    input_rows = len(df)

    cleaned, blank_rows_removed = remove_blank_rows(df)

    cleaned, text_cells_trimmed = trim_text_columns(cleaned)

    cleaned, duplicate_rows_removed = remove_duplicates(cleaned)

    detected_columns = detect_columns(
        cleaned,
        field_types=[
            "email",
            "phone",
            "zip",
            "address",
            "date",
        ],
    )

    email_column = detected_columns["email"]
    phone_column = detected_columns["phone"]
    zip_column = detected_columns["zip"]
    address_column = detected_columns["address"]
    date_column = detected_columns["date"]

    (
        cleaned,
        valid_emails,
        invalid_emails,
        missing_emails,
    ) = validate_email_column(
        cleaned,
        column_name=email_column,
    )

    (
        cleaned,
        valid_phones,
        invalid_phones,
        missing_phones,
        phone_numbers_standardized,
    ) = normalize_phone_column(
        cleaned,
        column_name=phone_column,
    )

    (
        cleaned,
        valid_dates,
        invalid_dates,
        missing_dates,
        dates_standardized,
    ) = normalize_date_column(
        cleaned,
        column_name=date_column,
    )

    (
        cleaned,
        valid_zip_codes,
        invalid_zip_codes,
        missing_zip_codes,
        zip_codes_standardized,
    ) = normalize_zip_code_column(
        cleaned,
        column_name=zip_column,
    )

    cleaned, title_case_cells_changed = apply_title_case(
        cleaned,
        title_case_columns,
    )



    missing_values = {
        str(column): int(cleaned[column].isna().sum())
        for column in original_columns
        if column in cleaned.columns
    }

    total_data_cells = len(cleaned) * len(original_columns)
    missing_data_cells = sum(missing_values.values())

    validation_checks = (
        valid_emails
        + invalid_emails
        + valid_phones
        + invalid_phones
        + valid_zip_codes
        + invalid_zip_codes
    )

    invalid_values = (
        invalid_emails
        + invalid_phones
        + invalid_zip_codes
    )

    validation_checks += valid_dates + invalid_dates
    invalid_values += invalid_dates

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
        input_rows=input_rows,
        output_rows=len(cleaned),
        blank_rows_removed=blank_rows_removed,
        duplicate_rows_removed=duplicate_rows_removed,
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
        missing_values_by_column=missing_values,
        quality_score=quality_score,
    )

    print(df.columns.tolist())

    return cleaned, report