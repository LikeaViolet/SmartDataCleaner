from io import BytesIO

import pandas as pd

from src.export_utils import (
    build_cleaned_data_export,
    build_quality_issues_export,
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


def test_cleaned_export_removes_status_columns():
    source = pd.DataFrame(
        {
            "Name": ["Alice"],
            "Email": ["alice@example.com"],
            "Email Status": ["Valid"],
        }
    )

    result = build_cleaned_data_export(
        source
    )

    assert list(result.columns) == [
        "Name",
        "Email",
    ]


def test_quality_issues_include_missing_values():
    source = pd.DataFrame(
        {
            "Name": ["Alice", None],
            "Email": [
                "alice@example.com",
                None,
            ],
            "Email Status": [
                "Valid",
                "Missing",
            ],
        }
    )

    result = build_quality_issues_export(
        source
    )

    assert set(result["Column"]) == {
        "Name",
        "Email",
    }

    assert set(result["Status"]) == {
        "Missing",
    }


def test_excel_export_contains_audit_sheets():
    source = pd.DataFrame(
        {
            "Name": ["Alice", None],
            "Email Status": [
                "Valid",
                "Missing",
            ],
        }
    )

    duplicates = pd.DataFrame(
        {
            "Name": ["Alice"],
        }
    )

    result = dataframe_to_excel_bytes(
        source,
        removed_duplicates=duplicates,
    )

    workbook = pd.ExcelFile(
        BytesIO(result)
    )

    assert workbook.sheet_names == [
        "Cleaned Data",
        "Quality Issues",
        "Removed Duplicates",
    ]


def test_excel_cleaned_sheet_excludes_statuses():
    source = pd.DataFrame(
        {
            "Name": ["Alice"],
            "Email Status": ["Valid"],
        }
    )

    result = dataframe_to_excel_bytes(
        source
    )

    restored = pd.read_excel(
        BytesIO(result),
        sheet_name="Cleaned Data",
    )

    assert list(restored.columns) == [
        "Name",
    ]