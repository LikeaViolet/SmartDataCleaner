
import pandas as pd

from src.validator import validate_email


def validate_email_column(
    df: pd.DataFrame,
    column_name: str | None,
) -> tuple[pd.DataFrame, int, int, int]:
    cleaned = df.copy()

    valid_emails = 0
    invalid_emails = 0
    missing_emails = 0

    if column_name is None or column_name not in cleaned.columns:
        return (
            cleaned,
            valid_emails,
            invalid_emails,
            missing_emails,
        )

    status_column = f"{column_name} Status"

    cleaned[status_column] = cleaned[column_name].apply(
        validate_email
    )

    email_counts = cleaned[status_column].value_counts()

    valid_emails = int(email_counts.get("Valid", 0))
    invalid_emails = int(email_counts.get("Invalid", 0))
    missing_emails = int(email_counts.get("Missing", 0))

    return (
        cleaned,
        valid_emails,
        invalid_emails,
        missing_emails,
    )