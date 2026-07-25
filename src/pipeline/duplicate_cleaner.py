import pandas as pd


def remove_duplicates(
    df: pd.DataFrame,
):
    before = len(df)

    cleaned = df.drop_duplicates().reset_index(drop=True)

    removed = before - len(cleaned)

    return cleaned, removed