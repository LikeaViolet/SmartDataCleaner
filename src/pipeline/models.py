from dataclasses import dataclass

import pandas as pd


@dataclass
class ValidationResult:
    dataframe: pd.DataFrame

    valid: int = 0
    invalid: int = 0
    missing: int = 0
    standardized: int = 0

    detected_column: str | None = None