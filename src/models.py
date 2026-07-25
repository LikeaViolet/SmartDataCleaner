from dataclasses import dataclass, asdict


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

    valid_dates: int
    invalid_dates: int
    missing_dates: int
    dates_standardized: int

    missing_values_by_column: dict[str, int]

    def to_dict(self):
        return asdict(self)