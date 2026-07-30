from __future__ import annotations

import pandas as pd


def remove_duplicates(
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, int, pd.DataFrame]:
    duplicate_mask = df.duplicated(
        keep="first"
    )

    removed_rows = (
        df.loc[duplicate_mask]
        .copy()
        .reset_index(drop=True)
    )

    cleaned = (
        df.loc[~duplicate_mask]
        .copy()
        .reset_index(drop=True)
    )

    return (
        cleaned,
        len(removed_rows),
        removed_rows,
    )