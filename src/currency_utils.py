from __future__ import annotations

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

import pandas as pd


TWOPLACES = Decimal("0.01")


def normalize_currency(
    value: object,
) -> tuple[str | None, str]:
    """
    Normalize a currency-like value into a two-decimal string.

    Examples:
    $1,250.50  -> 1250.50
    1250       -> 1250.00
    ($45.25)   -> -45.25

    Returns:
        (normalized_value, status)

    Status values:
    - Valid
    - Invalid
    - Missing
    """

    if value is None or pd.isna(value):
        return None, "Missing"

    text = str(value).strip()

    if not text:
        return None, "Missing"

    is_negative_parentheses = (
        text.startswith("(")
        and text.endswith(")")
    )

    if is_negative_parentheses:
        text = text[1:-1].strip()

    text = (
        text
        .replace("$", "")
        .replace(",", "")
        .strip()
    )

    if not text:
        return None, "Invalid"

    try:
        amount = Decimal(text)
    except InvalidOperation:
        return str(value).strip(), "Invalid"

    if is_negative_parentheses:
        amount = -amount

    amount = amount.quantize(
        TWOPLACES,
        rounding=ROUND_HALF_UP,
    )

    return format(amount, ".2f"), "Valid"