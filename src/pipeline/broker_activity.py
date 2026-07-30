from __future__ import annotations

import re
from typing import Any

import pandas as pd


AS_OF_DATE_PATTERN = re.compile(
    r"^\s*(?P<posted>.+?)\s+as\s+of\s+(?P<effective>.+?)\s*$",
    re.IGNORECASE,
)

OPTION_SYMBOL_PATTERN = re.compile(
    r"""
    ^\s*
    (?P<ticker>[A-Z][A-Z0-9.\-]*)
    \s+
    (?P<expiration>\d{1,2}/\d{1,2}/\d{4})
    \s+
    (?P<strike>\d+(?:\.\d+)?)
    \s+
    (?P<option_type>[CP])
    \s*$
    """,
    re.VERBOSE | re.IGNORECASE,
)


def _is_missing(value: Any) -> bool:
    return pd.isna(value) or not str(value).strip()


def parse_accounting_number(
    value: Any,
) -> float | None:
    if _is_missing(value):
        return None

    text = str(value).strip()

    is_negative = (
        text.startswith("(")
        and text.endswith(")")
    )

    text = (
        text.replace("$", "")
        .replace(",", "")
        .replace("(", "")
        .replace(")", "")
        .strip()
    )

    if not text:
        return None

    number = float(text)

    if is_negative:
        return -abs(number)

    return number


def parse_activity_dates(
    value: Any,
) -> tuple[pd.Timestamp | None, pd.Timestamp | None]:
    if _is_missing(value):
        return None, None

    text = str(value).strip()
    match = AS_OF_DATE_PATTERN.match(text)

    if match:
        posted_date = pd.to_datetime(
            match.group("posted"),
            errors="coerce",
        )
        effective_date = pd.to_datetime(
            match.group("effective"),
            errors="coerce",
        )
    else:
        posted_date = pd.to_datetime(
            text,
            errors="coerce",
        )
        effective_date = posted_date

    posted_result = (
        None if pd.isna(posted_date) else posted_date
    )
    effective_result = (
        None if pd.isna(effective_date) else effective_date
    )

    return posted_result, effective_result


def parse_option_symbol(
    value: Any,
) -> dict[str, object]:
    default = {
        "Underlying": None,
        "Expiration": None,
        "Strike": None,
        "Option Type": None,
        "Security Type": "Equity",
    }

    if _is_missing(value):
        default["Security Type"] = None
        return default

    text = str(value).strip().upper()
    match = OPTION_SYMBOL_PATTERN.match(text)

    if not match:
        default["Underlying"] = text
        return default

    option_type = match.group("option_type").upper()

    return {
        "Underlying": match.group("ticker").upper(),
        "Expiration": pd.to_datetime(
            match.group("expiration"),
            errors="coerce",
        ),
        "Strike": float(match.group("strike")),
        "Option Type": (
            "Call" if option_type == "C" else "Put"
        ),
        "Security Type": "Option",
    }


def repair_broker_activity_headers(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    result = dataframe.copy()

    repaired_columns: list[str] = []

    for index, column in enumerate(result.columns):
        name = str(column).strip()

        if (
            not name
            or name.lower().startswith("unnamed:")
        ):
            if index == 7:
                name = "Amount"
            else:
                name = f"Unnamed Column {index + 1}"

        repaired_columns.append(name)

    result.columns = repaired_columns
    return result


def normalize_broker_activity(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    result = repair_broker_activity_headers(
        dataframe
    )

    required_columns = {
        "Date",
        "Action",
        "Symbol",
        "Description",
        "Quantity",
        "Price",
        "Fees & Comm",
        "Amount",
    }

    missing_columns = (
        required_columns - set(result.columns)
    )

    if missing_columns:
        names = ", ".join(sorted(missing_columns))
        raise ValueError(
            "Broker activity data is missing required "
            f"columns: {names}"
        )

    parsed_dates = result["Date"].map(
        parse_activity_dates
    )

    result["Date"] = parsed_dates.map(
        lambda dates: dates[0]
    )
    result["Effective Date"] = parsed_dates.map(
        lambda dates: dates[1]
    )

    result["Action"] = (
        result["Action"]
        .astype("string")
        .str.strip()
        .str.title()
    )

    result["Quantity"] = pd.to_numeric(
        result["Quantity"],
        errors="coerce",
    )

    for column in [
        "Price",
        "Fees & Comm",
        "Amount",
    ]:
        result[column] = result[column].map(
            parse_accounting_number
        )

    parsed_contracts = result["Symbol"].map(
        parse_option_symbol
    )

    parsed_contracts_dataframe = pd.DataFrame(
        parsed_contracts.tolist(),
        index=result.index,
    )

    result = pd.concat(
        [
            result,
            parsed_contracts_dataframe,
        ],
        axis=1,
    )

    ordered_columns = [
        "Date",
        "Effective Date",
        "Action",
        "Security Type",
        "Symbol",
        "Underlying",
        "Expiration",
        "Strike",
        "Option Type",
        "Description",
        "Quantity",
        "Price",
        "Fees & Comm",
        "Amount",
    ]

    return result[ordered_columns]


BROKER_ACTIVITY_REQUIRED_COLUMNS = {
    "Date",
    "Action",
    "Symbol",
    "Description",
    "Quantity",
    "Price",
    "Fees & Comm",
    "Amount",
}


def is_broker_activity_dataframe(
    dataframe: pd.DataFrame,
) -> bool:
    repaired = repair_broker_activity_headers(
        dataframe
    )

    return BROKER_ACTIVITY_REQUIRED_COLUMNS.issubset(
        repaired.columns
    )

def calculate_broker_missing_values(
    dataframe: pd.DataFrame,
) -> tuple[dict[str, int], int]:
    """
    Count only contextually required brokerage fields.

    Expired transactions may omit price, fees, and amount.
    Equity records may omit option-specific fields.
    Commission and fee values are optional because some
    brokers leave them blank when no fee was charged.
    """

    missing: dict[str, int] = {}

    always_required = [
        "Date",
        "Effective Date",
        "Action",
        "Security Type",
        "Symbol",
        "Underlying",
        "Description",
        "Quantity",
    ]

    total_expected_cells = (
        len(dataframe) * len(always_required)
    )

    for column in always_required:
        count = int(dataframe[column].isna().sum())

        if count:
            missing[column] = count

    option_mask = (
        dataframe["Security Type"] == "Option"
    )

    option_required = [
        "Expiration",
        "Strike",
        "Option Type",
    ]

    total_expected_cells += (
        int(option_mask.sum())
        * len(option_required)
    )

    for column in option_required:
        count = int(
            dataframe.loc[
                option_mask,
                column,
            ].isna().sum()
        )

        if count:
            missing[column] = count

    active_trade_mask = (
        dataframe["Action"]
        .astype("string")
        .str.casefold()
        .ne("expired")
    )

    trade_required = [
        "Price",
        "Amount",
    ]

    total_expected_cells += (
        int(active_trade_mask.sum())
        * len(trade_required)
    )

    for column in trade_required:
        count = int(
            dataframe.loc[
                active_trade_mask,
                column,
            ].isna().sum()
        )

        if count:
            missing[column] = count

    return missing, total_expected_cells