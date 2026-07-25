from typing import Iterable

import pandas as pd


def trim_text_columns(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    cleaned = df.copy()
    changed = 0

    for column in cleaned.select_dtypes(include=["object", "string"]).columns:
        original = cleaned[column]

        trimmed = original.map(
            lambda value: value.strip() if isinstance(value, str) else value
        )

        changed += int(
            sum(
                isinstance(before, str)
                and isinstance(after, str)
                and before != after
                for before, after in zip(original, trimmed)
            )
        )

        cleaned[column] = trimmed

    return cleaned, changed


def title_case_columns(
    df: pd.DataFrame,
    columns: Iterable[str] | None,
) -> tuple[pd.DataFrame, int]:
    cleaned = df.copy()
    changed = 0

    for column in columns or []:
        if column not in cleaned.columns:
            raise ValueError(f"Title-case column not found: {column}")

        original = cleaned[column]

        converted = original.map(
            lambda value: value.title() if isinstance(value, str) else value
        )

        changed += int(
            sum(
                isinstance(before, str)
                and isinstance(after, str)
                and before != after
                for before, after in zip(original, converted)
            )
        )

        cleaned[column] = converted

    return cleaned, changed