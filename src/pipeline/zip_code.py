import pandas as pd

from src.pipeline.models import ValidationResult
from src.validator import normalize_zip_code


def normalize_zip_code_column(
    df: pd.DataFrame,
    column_name: str | None,
) -> ValidationResult:
    cleaned = df.copy()

    valid_zip_codes = 0
    invalid_zip_codes = 0
    missing_zip_codes = 0
    zip_codes_standardized = 0

    if column_name is None or column_name not in cleaned.columns:
        return ValidationResult(
            dataframe=cleaned,
            valid=0,
            invalid=0,
            missing=0,
            standardized=0,
            detected_column=None,
        )

    original_zip_values = cleaned[column_name].copy()
    zip_results = cleaned[column_name].apply(
        normalize_zip_code
    )

    status_column = f"{column_name} Status"

    cleaned[column_name] = zip_results.apply(
        lambda result: result[0]
    )
    cleaned[status_column] = zip_results.apply(
        lambda result: result[1]
    )

    valid_zip_codes = int(
        (cleaned[status_column] == "Valid").sum()
    )
    invalid_zip_codes = int(
        (cleaned[status_column] == "Invalid").sum()
    )
    missing_zip_codes = int(
        (cleaned[status_column] == "Missing").sum()
    )

    zip_codes_standardized = sum(
        1
        for original, normalized, status in zip(
            original_zip_values,
            cleaned[column_name],
            cleaned[status_column],
        )
        if status == "Valid"
        and not pd.isna(original)
        and str(original).strip() != str(normalized)
    )

    return ValidationResult(
        dataframe=cleaned,
        valid=valid_zip_codes,
        invalid=invalid_zip_codes,
        missing=missing_zip_codes,
        standardized=zip_codes_standardized,
        detected_column=column_name,
    )