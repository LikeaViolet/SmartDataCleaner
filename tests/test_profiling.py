import pandas as pd

from src.profiling import profile_dataset


def test_profile_dataset_counts_rows_and_columns():
    source = pd.DataFrame(
        {
            "Name": ["Alice", "Bob", "Bob"],
            "Email": [
                "alice@example.com",
                "bob@example.com",
                "bob@example.com",
            ],
        }
    )

    profile = profile_dataset(source)

    assert profile.rows == 3
    assert profile.columns == 2
    assert profile.duplicate_rows == 1
    assert profile.duplicate_percentage == 33.3


def test_profile_dataset_counts_missing_cells():
    source = pd.DataFrame(
        {
            "Name": ["Alice", None],
            "Phone": ["4045550198", None],
        }
    )

    profile = profile_dataset(source)

    assert profile.missing_cells == 2
    assert profile.missing_percentage == 50.0


def test_profile_dataset_builds_column_profiles():
    source = pd.DataFrame(
        {
            "Customer Email": [
                "alice@example.com",
                "bob@example.com",
                None,
            ],
        }
    )

    profile = profile_dataset(source)
    column = profile.column_profiles[0]

    assert column.name == "Customer Email"
    assert column.non_missing == 2
    assert column.missing == 1
    assert column.missing_percentage == 33.3
    assert column.unique_values == 2
    assert column.unique_percentage == 100.0
    assert column.detected_type == "email"


def test_profile_dataset_handles_empty_dataframe():
    source = pd.DataFrame(
        columns=["Name", "Email"]
    )

    profile = profile_dataset(source)

    assert profile.rows == 0
    assert profile.columns == 2
    assert profile.duplicate_rows == 0
    assert profile.duplicate_percentage == 0.0
    assert profile.missing_cells == 0
    assert profile.missing_percentage == 0.0