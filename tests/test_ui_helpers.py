from io import BytesIO

from src.ui.layout import (
    parse_title_case_columns,
    read_uploaded_dataset,
)


def test_parse_title_case_columns():
    result = parse_title_case_columns(
        "Name, City, Customer Name"
    )

    assert result == [
        "Name",
        "City",
        "Customer Name",
    ]


def test_parse_title_case_columns_ignores_blanks():
    result = parse_title_case_columns(
        "Name, , City,"
    )

    assert result == ["Name", "City"]


def test_read_uploaded_csv():
    uploaded = BytesIO(
        b"Name,Email\nAlice,alice@example.com\n"
    )
    uploaded.name = "customers.csv"

    dataframe = read_uploaded_dataset(uploaded)

    assert len(dataframe) == 1
    assert dataframe.loc[0, "Name"] == "Alice"