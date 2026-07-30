from dataclasses import asdict, dataclass, field
from src.profiling import DatasetProfile


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
    dataset_profile: DatasetProfile
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

    valid_currency_values: int
    invalid_currency_values: int
    missing_currency_values: int
    currency_values_standardized: int


    missing_values_by_column: dict[str, int]

    quality_score: QualityScore

    removed_duplicate_rows: list[
        dict[str, object]
    ] = field(default_factory=list)

    ai_summary: str | None = None
    ai_strengths: list[str] = field(default_factory=list)
    ai_risks: list[str] = field(default_factory=list)
    ai_recommendations: list[dict[str, str]] = field(
        default_factory=list
    )
    ai_error: str | None = None


    def to_dict(self) -> dict:
        return asdict(self)