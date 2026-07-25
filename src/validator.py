# Validation rules

import re
from typing import Any

import pandas as pd


EMAIL_PATTERN = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)


def validate_email(value: Any) -> str:
    if value is None or pd.isna(value):
        return "Missing"

    email = str(value).strip()

    if not email:
        return "Missing"

    if EMAIL_PATTERN.fullmatch(email):
        return "Valid"

    return "Invalid"


def normalize_phone(value: Any) -> tuple[str | None, str]:
    """
    Normalize US phone numbers.

    Returns:
        (formatted_phone, status)
    """
    if value is None or pd.isna(value):
        return None, "Missing"

    # Pandas may read phone numbers as floats, such as 4045551234.0.
    if isinstance(value, float) and value.is_integer():
        phone = str(int(value))
    else:
        phone = str(value).strip()

    if not phone:
        return None, "Missing"

    digits = re.sub(r"\D", "", phone)

    # Remove a leading US country code.
    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]

    if len(digits) != 10:
        return phone, "Invalid"

    formatted = f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    return formatted, "Valid"

ZIP_CODE_PATTERN = re.compile(r"^\d{5}(?:-\d{4})?$")


def normalize_zip_code(
    value: Any,
) -> tuple[str | None, str]:
    """
    Normalize and validate a US ZIP code.

    Supported formats:
        30301
        30301-1234

    Returns:
        A tuple containing:
        - normalized ZIP code or None
        - Valid, Invalid, or Missing
    """

    if value is None or pd.isna(value):
        return None, "Missing"

    if isinstance(value, float) and value.is_integer():
        text = str(int(value))
    else:
        text = str(value).strip()

    if not text:
        return None, "Missing"

    # Remove common spreadsheet formatting artifacts.
    text = text.replace(" ", "")

    # Recover leading zero from numeric spreadsheet values.
    if text.isdigit() and len(text) < 5:
        text = text.zfill(5)

    if ZIP_CODE_PATTERN.fullmatch(text):
        return text, "Valid"

    return text, "Invalid"