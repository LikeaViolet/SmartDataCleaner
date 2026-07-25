from pathlib import Path
import pandas as pd

# Reading/writing files

SUPPORTED_EXTENSIONS = {".csv", ".xlsx", ".xls"}


def read_dataset(path: str | Path) -> pd.DataFrame:
    """Read a CSV or Excel file into a DataFrame."""
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"Input file not found: {file_path}")

    extension = file_path.suffix.lower()
    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type '{extension}'. "
            "Use CSV, XLSX, or XLS."
        )

    if extension == ".csv":
        return pd.read_csv(file_path)

    return pd.read_excel(file_path)


def write_dataset(df: pd.DataFrame, path: str | Path) -> Path:
    """Write a DataFrame to CSV or XLSX based on the output extension."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    extension = output_path.suffix.lower()
    if extension == ".csv":
        df.to_csv(output_path, index=False)
    elif extension == ".xlsx":
        df.to_excel(output_path, index=False)
    else:
        raise ValueError("Output file must end in .csv or .xlsx")

    return output_path
