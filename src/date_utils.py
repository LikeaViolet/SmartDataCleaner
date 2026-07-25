from typing import Any

import pandas as pd


def normalize_date(value: Any) -> tuple[str | None, str]:
    """
    Convert dates into ISO format (YYYY-MM-DD).

    Returns:
        (normalized_date, status)
    """

    if value is None or pd.isna(value):
        return None, "Missing"

    text = str(value).strip()

    if not text:
        return None, "Missing"

    try:
        date = pd.to_datetime(text, errors="raise")
        return date.strftime("%Y-%m-%d"), "Valid"

    except Exception:
        return text, "Invalid"