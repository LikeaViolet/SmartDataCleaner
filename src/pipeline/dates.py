import pandas as pd

from src.date_utils import normalize_date


def normalize_date_column(
    df: pd.DataFrame,
    column_name: str | None,
) -> tuple[pd.DataFrame, int, int, int, int]:
    cleaned = df.copy()

    valid_count = 0
    invalid_count = 0
    missing_count = 0
    standardized_count = 0

    if column_name is None or column_name not in cleaned.columns:
        return (
            cleaned,
            valid_count,
            invalid_count,
            missing_count,
            standardized_count,
        )

    original_dates = cleaned[column_name].copy()
    results = cleaned[column_name].apply(normalize_date)

    status_column = f"{column_name} Status"

    cleaned[column_name] = results.map(
        lambda result: result[0]
    )
    cleaned[status_column] = results.map(
        lambda result: result[1]
    )

    counts = cleaned[status_column].value_counts()

    valid_count = int(counts.get("Valid", 0))
    invalid_count = int(counts.get("Invalid", 0))
    missing_count = int(counts.get("Missing", 0))

    standardized_count = int(
        sum(
            status == "Valid"
            and str(before).strip() != str(after).strip()
            for before, after, status in zip(
                original_dates,
                cleaned[column_name],
                cleaned[status_column],
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