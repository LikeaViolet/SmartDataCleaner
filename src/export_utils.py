from __future__ import annotations

from io import BytesIO

import pandas as pd


def dataframe_to_csv_bytes(df: pd.DataFrame) -> bytes:
    """Convert a dataframe into downloadable CSV bytes."""

    return df.to_csv(index=False).encode("utf-8")


def dataframe_to_excel_bytes(df: pd.DataFrame) -> bytes:
    """Convert a dataframe into downloadable Excel bytes."""

    buffer = BytesIO()

    with pd.ExcelWriter(
        buffer,
        engine="openpyxl",
    ) as writer:
        df.to_excel(
            writer,
            index=False,
            sheet_name="Cleaned Data",
        )

    buffer.seek(0)
    return buffer.getvalue()