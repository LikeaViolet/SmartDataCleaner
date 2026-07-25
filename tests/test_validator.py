import pandas as pd
import pytest

from src.validator import validate_email, normalize_zip_code


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("john@example.com", "Valid"),
        (" jane@example.org ", "Valid"),
        ("john@gmail", "Invalid"),
        ("@gmail.com", "Invalid"),
        ("hello", "Invalid"),
        ("", "Missing"),
        ("   ", "Missing"),
        (None, "Missing"),
        (pd.NA, "Missing"),
    ],
)
def test_validate_email(value, expected):
    assert validate_email(value) == expected


@pytest.mark.parametrize(
    ("value", "expected_zip", "expected_status"),
    [
        ("30301", "30301", "Valid"),
        ("30301-1234", "30301-1234", "Valid"),
        (30301, "30301", "Valid"),
        (30301.0, "30301", "Valid"),
        ("02108", "02108", "Valid"),
        (2108, "02108", "Valid"),
        ("3030", "03030", "Valid"),
        ("ABCDE", "ABCDE", "Invalid"),
        ("30301-12", "30301-12", "Invalid"),
        ("", None, "Missing"),
        (None, None, "Missing"),
    ],
)
def test_validate_zip_code(
    value,
    expected_zip,
    expected_status,
):
    normalized, status = normalize_zip_code(value)

    assert normalized == expected_zip
    assert status == expected_status