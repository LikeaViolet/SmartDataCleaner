import pandas as pd

from src.date_utils import normalize_date


def normalize_date_column(
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, int, int, int, int]:
    cleaned = df.copy()

    valid_count = 0
    invalid_count = 0
    missing_count = 0
    standardized_count = 0

    if "Date" not in cleaned.columns:
        return (
            cleaned,
            valid_count,
            invalid_count,
            missing_count,
            standardized_count,
        )

    original_dates = cleaned["Date"].copy()
    results = cleaned["Date"].apply(normalize_date)

    cleaned["Date"] = results.map(lambda result: result[0])
    cleaned["Date Status"] = results.map(lambda result: result[1])

    counts = cleaned["Date Status"].value_counts()

    valid_count = int(counts.get("Valid", 0))
    invalid_count = int(counts.get("Invalid", 0))
    missing_count = int(counts.get("Missing", 0))

    standardized_count = int(
        sum(
            status == "Valid"
            and str(before).strip() != str(after).strip()
            for before, after, status in zip(
                original_dates,
                cleaned["Date"],
                cleaned["Date Status"],
            )
        )
    )

    return (
        cleaned,
        valid_count,
        invalid_count,
        missing_count,
        standardized_count,
    )