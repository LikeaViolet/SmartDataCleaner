import pandas as pd
import pytest

from src.date_utils import normalize_date


@pytest.mark.parametrize(
    ("value", "expected_date", "expected_status"),
    [
        ("7/1/26", "2026-07-01", "Valid"),
        ("July 1, 2026", "2026-07-01", "Valid"),
        ("2026-07-01", "2026-07-01", "Valid"),
        ("07-01-2026", "2026-07-01", "Valid"),
        ("not a date", "not a date", "Invalid"),
        ("", None, "Missing"),
        (None, None, "Missing"),
        (pd.NA, None, "Missing"),
    ],
)
def test_normalize_date(value, expected_date, expected_status):
    date, status = normalize_date(value)

    assert date == expected_date
    assert status == expected_status