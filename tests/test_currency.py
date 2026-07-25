import pandas as pd
import pytest

from src.currency_utils import normalize_currency
from src.pipeline.currency import normalize_currency_column


@pytest.mark.parametrize(
    ("value", "expected_value", "expected_status"),
    [
        ("$1,250.50", "1250.50", "Valid"),
        ("1250", "1250.00", "Valid"),
        (1250, "1250.00", "Valid"),
        (1250.5, "1250.50", "Valid"),
        ("1,250.5", "1250.50", "Valid"),
        ("($45.25)", "-45.25", "Valid"),
        ("-45.25", "-45.25", "Valid"),
        ("", None, "Missing"),
        (None, None, "Missing"),
        ("not money", "not money", "Invalid"),
    ],
)
def test_normalize_currency(
    value,
    expected_value,
    expected_status,
):
    normalized, status = normalize_currency(value)

    assert normalized == expected_value
    assert status == expected_status


def test_normalize_currency_column():
    source = pd.DataFrame(
        {
            "Amount": [
                "$1,250.50",
                "500",
                "bad",
                None,
            ]
        }
    )

    result = normalize_currency_column(
        source,
        column_name="Amount",
    )

    assert result.valid == 2
    assert result.invalid == 1
    assert result.missing == 1
    assert result.standardized == 2
    assert result.detected_column == "Amount"

    assert result.dataframe.loc[0, "Amount"] == "1250.50"
    assert result.dataframe.loc[1, "Amount"] == "500.00"
    assert result.dataframe.loc[2, "Amount"] == "bad"
    assert pd.isna(result.dataframe.loc[3, "Amount"])

    assert result.dataframe[
        "Amount Status"
    ].tolist() == [
        "Valid",
        "Valid",
        "Invalid",
        "Missing",
    ]


def test_currency_pipeline_without_detected_column():
    source = pd.DataFrame(
        {
            "Name": ["Alice", "Bob"],
        }
    )

    result = normalize_currency_column(
        source,
        column_name=None,
    )

    assert result.dataframe.equals(source)
    assert result.valid == 0
    assert result.invalid == 0
    assert result.missing == 0
    assert result.standardized == 0