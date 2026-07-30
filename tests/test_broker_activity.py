import pandas as pd
import pytest

from src.cleaner import clean_dataset
from src.pipeline.broker_activity import (
    calculate_broker_missing_values,
    is_broker_activity_dataframe,
    normalize_broker_activity,
    parse_accounting_number,
    parse_activity_dates,
    parse_option_symbol,
)


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("$0.45 ", 0.45),
        ("$44.34", 44.34),
        ("($20.66)", -20.66),
        ("-$1.30", -1.30),
        ("", None),
        (None, None),
    ],
)
def test_parse_accounting_number(
    source,
    expected,
):
    assert parse_accounting_number(source) == expected


def test_parse_as_of_date():
    posted, effective = parse_activity_dates(
        "06/22/2026 as of 06/18/2026"
    )

    assert posted == pd.Timestamp("2026-06-22")
    assert effective == pd.Timestamp("2026-06-18")


def test_parse_regular_activity_date():
    posted, effective = parse_activity_dates(
        "6/18/26"
    )

    assert posted == pd.Timestamp("2026-06-18")
    assert effective == pd.Timestamp("2026-06-18")


def test_parse_option_symbol():
    result = parse_option_symbol(
        "MU 06/18/2026 1115.00 P"
    )

    assert result == {
        "Underlying": "MU",
        "Expiration": pd.Timestamp("2026-06-18"),
        "Strike": 1115.0,
        "Option Type": "Put",
        "Security Type": "Option",
    }


def test_parse_equity_symbol():
    result = parse_option_symbol("ASTI")

    assert result["Underlying"] == "ASTI"
    assert result["Security Type"] == "Equity"
    assert result["Expiration"] is None
    assert result["Strike"] is None
    assert result["Option Type"] is None


def test_normalize_broker_activity():
    source = pd.DataFrame(
        {
            "Date": [
                "06/22/2026 as of 06/18/2026",
                "6/18/26",
                "6/18/26",
            ],
            "Action": [
                "Expired",
                "Sell to Open",
                "Sell",
            ],
            "Symbol": [
                "MU 06/18/2026 1115.00 P",
                "MU 06/18/2026 1120.00 P",
                "ASTI",
            ],
            "Description": [
                "PUT MICRON TECHNOLOGY IN$1115 EXP 06/18/26",
                "PUT MICRON TECHNOLOGY IN$1120 EXP 06/18/26",
                "ASCENT SOLAR TECHNOL EQUCLASS EQUITY",
            ],
            "Quantity": [-1, 1, 1],
            "Price": [None, "$0.45 ", "$6.15"],
            "Fees & Comm": [None, "$0.66 ", None],
            "Unnamed: 7": [None, "$44.34", "$6.15"],
        }
    )

    result = normalize_broker_activity(source)

    assert list(result["Security Type"]) == [
        "Option",
        "Option",
        "Equity",
    ]

    assert result.loc[0, "Effective Date"] == (
        pd.Timestamp("2026-06-18")
    )

    assert result.loc[1, "Price"] == 0.45
    assert result.loc[1, "Fees & Comm"] == 0.66
    assert result.loc[1, "Amount"] == 44.34

    assert result.loc[2, "Underlying"] == "ASTI"

def make_broker_activity_dataframe():
    return pd.DataFrame(
        {
            "Date": [
                "06/22/2026 as of 06/18/2026",
                "06/22/2026 as of 06/18/2026",
                "6/18/26",
                "6/18/26",
                "6/18/26",
            ],
            "Action": [
                "Expired",
                "Expired",
                "Sell to Open",
                "Buy to Open",
                "Sell",
            ],
            "Symbol": [
                "MU 06/18/2026 1115.00 P",
                "MU 06/18/2026 1120.00 P",
                "MU 06/18/2026 1120.00 P",
                "MU 06/18/2026 1115.00 P",
                "ASTI",
            ],
            "Description": [
                "PUT MICRON TECHNOLOGY IN$1115 EXP 06/18/26",
                "PUT MICRON TECHNOLOGY IN$1120 EXP 06/18/26",
                "PUT MICRON TECHNOLOGY IN$1120 EXP 06/18/26",
                "PUT MICRON TECHNOLOGY IN$1115 EXP 06/18/26",
                "ASCENT SOLAR TECHNOL EQUCLASS EQUITY",
            ],
            "Quantity": [
                -1,
                1,
                1,
                1,
                1,
            ],
            "Price": [
                None,
                None,
                "$0.45 ",
                "$0.20 ",
                "$6.15 ",
            ],
            "Fees & Comm": [
                None,
                None,
                "$0.66 ",
                "$0.66 ",
                None,
            ],
            "Unnamed: 7": [
                None,
                None,
                "$44.34 ",
                "($20.66)",
                "$6.15 ",
            ],
        }
    )


def test_detects_broker_activity_dataframe():
    source = make_broker_activity_dataframe()

    assert is_broker_activity_dataframe(source)


def test_contextual_missing_values_ignore_expected_blanks():
    source = make_broker_activity_dataframe()
    normalized = normalize_broker_activity(source)

    missing, expected_cells = (
        calculate_broker_missing_values(
            normalized
        )
    )

    assert missing == {}
    assert expected_cells > 0


def test_clean_dataset_normalizes_broker_activity():
    source = make_broker_activity_dataframe()

    cleaned, report = clean_dataset(source)

    assert len(cleaned) == 5

    assert "Effective Date" in cleaned.columns
    assert "Security Type" in cleaned.columns
    assert "Underlying" in cleaned.columns
    assert "Expiration" in cleaned.columns
    assert "Strike" in cleaned.columns
    assert "Option Type" in cleaned.columns
    assert "Amount" in cleaned.columns

    assert cleaned.loc[0, "Security Type"] == (
        "Option"
    )

    assert cleaned.loc[4, "Security Type"] == (
        "Equity"
    )

    assert cleaned.loc[2, "Price"] == 0.45
    assert cleaned.loc[3, "Amount"] == -20.66

    assert report.missing_values_by_column == {}
    assert report.quality_score.completeness == 100.0