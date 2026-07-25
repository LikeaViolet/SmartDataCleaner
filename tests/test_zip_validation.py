import pytest

from src.validator import normalize_zip_code


@pytest.mark.parametrize(
    (
        "value",
        "expected_value",
        "expected_status",
    ),
    [
        ("30301", "30301", "Valid"),
        ("30301-1234", "30301-1234", "Valid"),
        (30301, "30301", "Valid"),
        (30301.0, "30301", "Valid"),
        ("02108", "02108", "Valid"),
        (2108, "02108", "Valid"),
        (" 30301 ", "30301", "Valid"),
        ("30301 1234", "303011234", "Invalid"),
        ("3030A", "3030A", "Invalid"),
        ("30301-12", "30301-12", "Invalid"),
        ("", None, "Missing"),
        ("   ", None, "Missing"),
        (None, None, "Missing"),
    ],
)
def test_normalize_zip_code(
    value,
    expected_value,
    expected_status,
):
    normalized_value, status = normalize_zip_code(value)

    assert normalized_value == expected_value
    assert status == expected_status