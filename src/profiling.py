from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from src.column_detection import detect_columns


@dataclass
class ColumnProfile:
    name: str
    dtype: str
    non_missing: int
    missing: int
    missing_percentage: float
    unique_values: int
    unique_percentage: float
    detected_type: str | None = None


@dataclass
class DatasetProfile:
    rows: int
    columns: int
    duplicate_rows: int
    duplicate_percentage: float
    missing_cells: int
    missing_percentage: float
    column_profiles: list[ColumnProfile]


def _safe_percentage(
    numerator: int,
    denominator: int,
) -> float:
    if denominator == 0:
        return 0.0

    return round(
        numerator / denominator * 100,
        1,
    )


def _reverse_detected_columns(
    df: pd.DataFrame,
) -> dict[str, str]:
    detected = detect_columns(
        df,
        field_types=[
            "email",
            "phone",
            "zip",
            "address",
            "date",
            "currency",
        ],
    )

    return {
        column_name: field_type
        for field_type, column_name in detected.items()
        if column_name is not None
    }


def profile_dataset(
    df: pd.DataFrame,
) -> DatasetProfile:
    rows = len(df)
    columns = len(df.columns)

    duplicate_rows = int(df.duplicated().sum())

    total_cells = rows * columns
    missing_cells = int(df.isna().sum().sum())

    detected_types = _reverse_detected_columns(df)

    column_profiles: list[ColumnProfile] = []

    for column in df.columns:
        series = df[column]

        missing = int(series.isna().sum())
        non_missing = int(series.notna().sum())
        unique_values = int(series.nunique(dropna=True))

        column_profiles.append(
            ColumnProfile(
                name=str(column),
                dtype=str(series.dtype),
                non_missing=non_missing,
                missing=missing,
                missing_percentage=_safe_percentage(
                    missing,
                    rows,
                ),
                unique_values=unique_values,
                unique_percentage=_safe_percentage(
                    unique_values,
                    non_missing,
                ),
                detected_type=detected_types.get(column),
            )
        )

    return DatasetProfile(
        rows=rows,
        columns=columns,
        duplicate_rows=duplicate_rows,
        duplicate_percentage=_safe_percentage(
            duplicate_rows,
            rows,
        ),
        missing_cells=missing_cells,
        missing_percentage=_safe_percentage(
            missing_cells,
            total_cells,
        ),
        column_profiles=column_profiles,
    )