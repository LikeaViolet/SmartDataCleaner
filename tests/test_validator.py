import pandas as pd
import pytest

from src.validator import validate_email


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