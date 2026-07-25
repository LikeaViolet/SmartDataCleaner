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
    - Optionally title-case explicitly selected columns.
    """
    input_rows = len(df)

    cleaned, blank_rows_removed = remove_blank_rows(df)

    cleaned, text_cells_trimmed = trim_text_columns(cleaned)

    cleaned, duplicate_rows_removed = remove_duplicates(cleaned)

    (
        cleaned,
        valid_emails,
        invalid_emails,
        missing_emails,
    ) = validate_email_column(cleaned)

    (
        cleaned,
        valid_phones,
        invalid_phones,
        missing_phones,
        phone_numbers_standardized,
    ) = normalize_phone_column(cleaned)

    (
        cleaned,
        valid_dates,
        invalid_dates,
        missing_dates,
        dates_standardized,
    ) = normalize_date_column(cleaned)

    cleaned, title_case_cells_changed = apply_title_case(
        cleaned,
        title_case_columns,
    )

    missing_values = {
        str(column): int(count)
        for column, count in cleaned.isna().sum().items()
    }

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
        valid_dates=valid_dates,
        invalid_dates=invalid_dates,
        missing_dates=missing_dates,
        dates_standardized=dates_standardized,
        missing_values_by_column=missing_values,
    )

    return cleaned, report