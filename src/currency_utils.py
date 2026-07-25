from decimal import Decimal, InvalidOperation
from typing import Any

import pandas as pd


def normalize_currency(
    value: Any,
) -> tuple[str | None, str]:
    if value is None or pd.isna(value):
        return None, "Missing"

    text = str(value).strip()

    if not text:
        return None, "Missing"

    negative = text.startswith("(") and text.endswith(")")

    cleaned = (
        text.replace("$", "")
        .replace(",", "")
        .replace("(", "")
        .replace(")", "")
        .strip()
    )

    try:
        amount = Decimal(cleaned)
    except InvalidOperation:
        return text, "Invalid"

    if negative:
        amount = -abs(amount)

    formatted = f"${abs(amount):,.2f}"

    if amount < 0:
        formatted = f"-{formatted}"

    return formatted, "Valid"