import pandas as pd

from src.currency_utils import normalize_currency
from src.pipeline.models import ValidationResult


def normalize_currency_column(
    df: pd.DataFrame,
    column_name: str | None,
) -> ValidationResult:
    cleaned = df.copy()

    if column_name is None or column_name not in cleaned.columns:
        return ValidationResult(
            dataframe=cleaned,
            detected_column=column_name,
        )

    original_values = cleaned[column_name].copy()

    results = cleaned[column_name].apply(
        normalize_currency
    )

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
                original_values,
                cleaned[column_name],
                cleaned[status_column],
            )
        )
    )

    return ValidationResult(
        dataframe=cleaned,
        valid=valid_count,
        invalid=invalid_count,
        missing=missing_count,
        standardized=standardized_count,
        detected_column=column_name,
    )