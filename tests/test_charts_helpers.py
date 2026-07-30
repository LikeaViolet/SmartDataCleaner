from types import SimpleNamespace

from src.ui.charts import (
    build_missing_values_dataframe,
)


def test_build_missing_values_dataframe():
    report = SimpleNamespace(
        input_rows=5,
        missing_values_by_column={
            "Name": 1,
            "Email": 2,
            "City": 0,
        },
    )

    result = build_missing_values_dataframe(report)

    assert list(result["Column"]) == [
        "Email",
        "Name",
    ]

    assert list(result["Missing values"]) == [
        2,
        1,
    ]

    assert list(result["Missing %"]) == [
        40.0,
        20.0,
    ]


def test_build_missing_values_dataframe_empty():
    report = SimpleNamespace(
        input_rows=5,
        missing_values_by_column={
            "Name": 0,
            "Email": 0,
        },
    )

    result = build_missing_values_dataframe(report)

    assert result.empty