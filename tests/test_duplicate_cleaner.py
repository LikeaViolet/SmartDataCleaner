import pandas as pd

from src.pipeline.duplicate_cleaner import (
    remove_duplicates,
)


def test_remove_duplicates_returns_removed_rows():
    source = pd.DataFrame(
        {
            "Name": [
                "Alice",
                "Bob",
                "Bob",
            ],
        }
    )

    cleaned, count, removed = (
        remove_duplicates(source)
    )

    assert list(cleaned["Name"]) == [
        "Alice",
        "Bob",
    ]

    assert count == 1

    assert list(removed["Name"]) == [
        "Bob",
    ]


def test_remove_duplicates_empty_audit():
    source = pd.DataFrame(
        {
            "Name": [
                "Alice",
                "Bob",
            ],
        }
    )

    cleaned, count, removed = (
        remove_duplicates(source)
    )

    assert len(cleaned) == 2
    assert count == 0
    assert removed.empty