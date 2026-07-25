import pandas as pd
import pytest

from src.column_detection import (
    detect_columns,
    find_column,
    find_columns,
    normalize_column_name,
)


def test_normalize_column_name():
    assert normalize_column_name("  Email   Address  ") == "email address"


@pytest.mark.parametrize(
    ("field_type", "expected"),
    [
        ("email", "Customer Email"),
        ("phone", "Mobile"),
        ("zip", "Postal Code"),
        ("address", "Street Address"),
        ("date", "Invoice Date"),
    ],
)
def test_find_column(field_type, expected):
    df = pd.DataFrame(
        columns=[
            "Name",
            "Customer Email",
            "Mobile",
            "Postal Code",
            "Street Address",
            "Invoice Date",
        ]
    )

    assert find_column(df, field_type) == expected


def test_find_column_returns_none_when_missing():
    df = pd.DataFrame(columns=["Name", "City"])

    assert find_column(df, "email") is None


def test_find_column_rejects_unknown_type():
    df = pd.DataFrame(columns=["Name"])

    with pytest.raises(ValueError, match="Unsupported field type"):
        find_column(df, "unknown")


def test_find_multiple_currency_columns():
    df = pd.DataFrame(
        columns=[
            "Name",
            "Price",
            "Balance",
            "Revenue",
        ]
    )

    assert find_columns(df, "currency") == [
        "Price",
        "Balance",
        "Revenue",
    ]


def test_detect_columns():
    df = pd.DataFrame(
        columns=[
            "Name",
            "Email Address",
            "Telephone",
            "ZIP Code",
        ]
    )

    detected = detect_columns(
        df,
        field_types=["email", "phone", "zip", "date"],
    )

    assert detected == {
        "email": "Email Address",
        "phone": "Telephone",
        "zip": "ZIP Code",
        "date": None,
    }