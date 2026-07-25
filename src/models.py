from dataclasses import asdict, dataclass


@dataclass
class QualityScore:
    completeness: float
    validity: float
    uniqueness: float
    consistency: float
    overall: float
    grade: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class CleaningReport:
    input_rows: int
    output_rows: int

    blank_rows_removed: int
    duplicate_rows_removed: int

    text_cells_trimmed: int
    title_case_cells_changed: int

    valid_emails: int
    invalid_emails: int
    missing_emails: int

    valid_phones: int
    invalid_phones: int
    missing_phones: int
    phone_numbers_standardized: int

    valid_zip_codes: int
    invalid_zip_codes: int
    missing_zip_codes: int
    zip_codes_standardized: int

    valid_dates: int
    invalid_dates: int
    missing_dates: int
    dates_standardized: int



    missing_values_by_column: dict[str, int]

    quality_score: QualityScore

    def to_dict(self) -> dict:
        return asdict(self)