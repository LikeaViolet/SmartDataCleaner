import pandas as pd

from src.validator import normalize_phone


def normalize_phone_column(
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, int, int, int, int]:
    cleaned = df.copy()

    valid_count = 0
    invalid_count = 0
    missing_count = 0
    standardized_count = 0

    if "Phone" not in cleaned.columns:
        return (
            cleaned,
            valid_count,
            invalid_count,
            missing_count,
            standardized_count,
        )

    original_phones = cleaned["Phone"].copy()
    results = cleaned["Phone"].apply(normalize_phone)

    cleaned["Phone"] = results.map(lambda result: result[0])
    cleaned["Phone Status"] = results.map(lambda result: result[1])

    counts = cleaned["Phone Status"].value_counts()

    valid_count = int(counts.get("Valid", 0))
    invalid_count = int(counts.get("Invalid", 0))
    missing_count = int(counts.get("Missing", 0))

    standardized_count = int(
        sum(
            status == "Valid"
            and str(before).strip() != str(after).strip()
            for before, after, status in zip(
                original_phones,
                cleaned["Phone"],
                cleaned["Phone Status"],
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