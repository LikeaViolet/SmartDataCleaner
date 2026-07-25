import pandas as pd


def remove_blank_rows(
    df: pd.DataFrame,
):
    before = len(df)

    cleaned = df.dropna(how="all").copy()

    removed = before - len(cleaned)

    return cleaned, removed