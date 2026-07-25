import pandas as pd
import pytest

from src.validator import normalize_phone


@pytest.mark.parametrize(
    ("value", "expected_phone", "expected_status"),
    [
        ("4045551234", "(404) 555-1234", "Valid"),
        ("404-555-1234", "(404) 555-1234", "Valid"),
        ("(404) 555-1234", "(404) 555-1234", "Valid"),
        ("1-404-555-1234", "(404) 555-1234", "Valid"),
        ("+1 404 555 1234", "(404) 555-1234", "Valid"),
        (4045551234, "(404) 555-1234", "Valid"),
        (4045551234.0, "(404) 555-1234", "Valid"),
        ("5551234", "5551234", "Invalid"),
        ("not a phone", "not a phone", "Invalid"),
        ("", None, "Missing"),
        ("   ", None, "Missing"),
        (None, None, "Missing"),
        (pd.NA, None, "Missing"),
    ],
)
def test_normalize_phone(
    value,
    expected_phone,
    expected_status,
):
    phone, status = normalize_phone(value)

    assert phone == expected_phone
    assert status == expected_status