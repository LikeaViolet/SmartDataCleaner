import pandas as pd

from src.cleaner import clean_dataset


def test_clean_dataset_removes_blank_duplicates_and_trims_text():
    source = pd.DataFrame(
        {
            "Name": ["  alice smith  ", "alice smith", None],
            "Email": [
                "alice@example.com ",
                "alice@example.com",
                None,
            ],
            "Phone": [
                "4045550198",
                "4045550198",
                None,
            ],
        }
    )

    cleaned, report = clean_dataset(source, title_case_columns=["Name"])

    assert len(cleaned) == 1
    assert cleaned.loc[0, "Name"] == "Alice Smith"
    assert cleaned.loc[0, "Phone"] == "(404) 555-0198"
    assert cleaned.loc[0, "Phone Status"] == "Valid"
    assert cleaned.loc[0, "Email"] == "alice@example.com"
    assert report.blank_rows_removed == 1
    assert report.duplicate_rows_removed == 1
    assert report.text_cells_trimmed == 2
    assert report.valid_phones == 1
    assert report.phone_numbers_standardized == 1
    assert report.dataset_profile.rows == 3
    assert report.dataset_profile.columns == 3
    assert report.dataset_profile.duplicate_rows == 0
    assert report.duplicate_rows_removed == 1
