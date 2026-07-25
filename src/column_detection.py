from collections.abc import Iterable

import pandas as pd


COLUMN_ALIASES: dict[str, set[str]] = {
    "email": {
        "email",
        "email address",
        "customer email",
        "contact email",
        "e-mail",
    },
    "phone": {
        "phone",
        "phone number",
        "mobile",
        "mobile number",
        "telephone",
        "contact number",
    },
    "zip": {
        "zip",
        "zip code",
        "zipcode",
        "postal code",
        "postalcode",
        "billing zip",
        "shipping zip",
    },
    "address": {
        "address",
        "street address",
        "mailing address",
        "billing address",
        "shipping address",
        "address line 1",
    },
    "date": {
        "date",
        "order date",
        "invoice date",
        "purchase date",
        "transaction date",
        "created date",
        "date of birth",
        "dob",
    },
    "currency": {
        "amount",
        "price",
        "cost",
        "revenue",
        "balance",
        "total",
        "subtotal",
        "payment",
        "sales",
    },
}


def normalize_column_name(column: object) -> str:
    """
    Convert a column label into a normalized comparison value.
    """

    return " ".join(str(column).strip().lower().split())


def find_column(
    df: pd.DataFrame,
    field_type: str,
) -> str | None:
    """
    Find the first DataFrame column matching the requested field type.
    """

    aliases = COLUMN_ALIASES.get(field_type)

    if aliases is None:
        raise ValueError(f"Unsupported field type: {field_type}")

    normalized_aliases = {
        normalize_column_name(alias)
        for alias in aliases
    }

    for column in df.columns:
        normalized_column = normalize_column_name(column)

        if normalized_column in normalized_aliases:
            return str(column)

    return None


def find_columns(
    df: pd.DataFrame,
    field_type: str,
) -> list[str]:
    """
    Find all DataFrame columns matching the requested field type.

    This is useful for datasets containing multiple address, date,
    or currency columns.
    """

    aliases = COLUMN_ALIASES.get(field_type)

    if aliases is None:
        raise ValueError(f"Unsupported field type: {field_type}")

    normalized_aliases = {
        normalize_column_name(alias)
        for alias in aliases
    }

    return [
        str(column)
        for column in df.columns
        if normalize_column_name(column) in normalized_aliases
    ]


def detect_columns(
    df: pd.DataFrame,
    field_types: Iterable[str] | None = None,
) -> dict[str, str | None]:
    """
    Detect one matching column for each requested field type.
    """

    if field_types is None:
        field_types = COLUMN_ALIASES.keys()

    return {
        field_type: find_column(df, field_type)
        for field_type in field_types
    }