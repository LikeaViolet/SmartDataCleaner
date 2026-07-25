from io import BytesIO

import pandas as pd

from src.export_utils import (
    dataframe_to_csv_bytes,
    dataframe_to_excel_bytes,
)


def test_dataframe_to_csv_bytes():
    source = pd.DataFrame(
        {
            "Name": ["Alice"],
            "Email": ["alice@example.com"],
        }
    )

    result = dataframe_to_csv_bytes(source)

    assert isinstance(result, bytes)
    assert b"Name,Email" in result
    assert b"Alice,alice@example.com" in result


def test_dataframe_to_excel_bytes():
    source = pd.DataFrame(
        {
            "Name": ["Alice"],
        }
    )

    result = dataframe_to_excel_bytes(source)

    assert isinstance(result, bytes)
    assert len(result) > 0

    restored = pd.read_excel(BytesIO(result))

    assert restored.loc[0, "Name"] == "Alice"