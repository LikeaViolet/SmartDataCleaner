
import pandas as pd

from src.validator import validate_email


def validate_email_column(
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, int, int, int]:
    cleaned = df.copy()

    valid_emails = 0
    invalid_emails = 0
    missing_emails = 0

    if "Email" not in cleaned.columns:
        return (
            cleaned,
            valid_emails,
            invalid_emails,
            missing_emails,
        )

    cleaned["Email Status"] = cleaned["Email"].apply(validate_email)

    email_counts = cleaned["Email Status"].value_counts()

    valid_emails = int(email_counts.get("Valid", 0))
    invalid_emails = int(email_counts.get("Invalid", 0))
    missing_emails = int(email_counts.get("Missing", 0))

    return (
        cleaned,
        valid_emails,
        invalid_emails,
        missing_emails,
    )