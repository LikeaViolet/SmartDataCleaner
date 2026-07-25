from pathlib import Path
import json

from src.cleaner import CleaningReport


def save_reports(
    report: CleaningReport,
    output_directory: str | Path,
) -> tuple[Path, Path]:
    output_dir = Path(output_directory)
    output_dir.mkdir(parents=True, exist_ok=True)

    json_path = output_dir / "cleaning_report.json"
    text_path = output_dir / "cleaning_report.txt"

    with json_path.open("w", encoding="utf-8") as file:
        json.dump(report.to_dict(), file, indent=2)

    missing_lines = "\n".join(
        f"  - {column}: {count}"
        for column, count in report.missing_values_by_column.items()
    )

    text = (
        "SMART DATA CLEANER REPORT\n"
        "\n"
        f"Rows imported: {report.input_rows}\n"
        f"Rows exported: {report.output_rows}\n"
        "\n"
        "Cleaning:\n"
        f"Blank rows removed: {report.blank_rows_removed}\n"
        f"Duplicate rows removed: {report.duplicate_rows_removed}\n"
        f"Text cells trimmed: {report.text_cells_trimmed}\n"
        f"Title-case cells changed: {report.title_case_cells_changed}\n"
        "\n"
        "Email validation:\n"
        f"Valid emails: {report.valid_emails}\n"
        f"Invalid emails: {report.invalid_emails}\n"
        f"Missing emails: {report.missing_emails}\n"
        "\n"
        "Phone validation:\n"
        f"Valid phone numbers: {report.valid_phones}\n"
        f"Invalid phone numbers: {report.invalid_phones}\n"
        f"Missing phone numbers: {report.missing_phones}\n"
        f"Phone numbers standardized: {report.phone_numbers_standardized}\n"
        "\n"
        
        "Date validation:\n"
        f"Valid dates: {report.valid_dates}\n"
        f"Invalid dates: {report.invalid_dates}\n"
        f"Missing dates: {report.missing_dates}\n"
        f"Dates standardized: {report.dates_standardized}\n"
        "\n"
        
        "Missing values by column:\n"
        f"{missing_lines or '  None'}\n"
        "\n"
        "Completed successfully.\n"
    )

    text_path.write_text(text, encoding="utf-8")

    return text_path, json_path