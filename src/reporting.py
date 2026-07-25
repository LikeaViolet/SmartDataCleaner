from pathlib import Path
import json

from src.models import CleaningReport


def save_reports(
    report: CleaningReport,
    output_directory: str | Path,
) -> tuple[Path, Path]:
    output_dir = Path(output_directory)
    output_dir.mkdir(parents=True, exist_ok=True)

    json_path = output_dir / "cleaning_report.json"
    text_path = output_dir / "cleaning_report.txt"

    with json_path.open("w", encoding="utf-8") as file:
        json.dump(
            report.to_dict(),
            file,
            indent=2,
        )

    missing_lines = "\n".join(
        f"  - {column}: {count}"
        for column, count
        in report.missing_values_by_column.items()
    )

    profile = report.dataset_profile
    quality = report.quality_score

    column_profile_lines: list[str] = []

    for column in profile.column_profiles:
        detected_type = (
            column.detected_type
            if column.detected_type is not None
            else "general"
        )

        column_profile_lines.extend(
            [
                "",
                f"{column.name}:",
                f"  Detected type: {detected_type}",
                f"  Pandas dtype: {column.dtype}",
                f"  Non-missing values: {column.non_missing}",
                (
                    "  Missing values: "
                    f"{column.missing} "
                    f"({column.missing_percentage:.1f}%)"
                ),
                (
                    "  Unique values: "
                    f"{column.unique_values} "
                    f"({column.unique_percentage:.1f}%)"
                ),
            ]
        )

    column_profile_text = "\n".join(column_profile_lines)

    lines = []

    lines.append("SMART DATA CLEANER REPORT")
    lines.append("")

    # -------------------------
    # DATA PROFILE
    # -------------------------

    lines.append("DATA PROFILE")
    lines.append(f"Rows: {profile.rows}")
    lines.append(f"Columns: {profile.columns}")
    lines.append(
        f"Duplicate rows: {profile.duplicate_rows} "
        f"({profile.duplicate_percentage:.1f}%)"
    )
    lines.append(
        f"Missing cells: {profile.missing_cells} "
        f"({profile.missing_percentage:.1f}%)"
    )

    lines.append("")
    lines.append("COLUMN PROFILE")

    for column in profile.column_profiles:
        detected = column.detected_type or "general"

        lines.append("")
        lines.append(f"{column.name}:")
        lines.append(f"  Detected type: {detected}")
        lines.append(f"  Pandas dtype: {column.dtype}")
        lines.append(f"  Non-missing values: {column.non_missing}")
        lines.append(
            f"  Missing values: {column.missing} "
            f"({column.missing_percentage:.1f}%)"
        )
        lines.append(
            f"  Unique values: {column.unique_values} "
            f"({column.unique_percentage:.1f}%)"
        )

    # -------------------------
    # DATA QUALITY
    # -------------------------

    lines.append("")
    lines.append("DATA QUALITY")
    lines.append(f"Overall score: {quality.overall}%")
    lines.append(f"Grade: {quality.grade}")
    lines.append(f"Completeness: {quality.completeness}%")
    lines.append(f"Validity: {quality.validity}%")
    lines.append(f"Uniqueness: {quality.uniqueness}%")
    lines.append(f"Consistency: {quality.consistency}%")

    lines.append("")
    lines.append(f"Rows imported: {report.input_rows}")
    lines.append(f"Rows exported: {report.output_rows}")

    lines.append("")
    lines.append("Cleaning:")
    lines.append(f"Blank rows removed: {report.blank_rows_removed}")
    lines.append(f"Duplicate rows removed: {report.duplicate_rows_removed}")
    lines.append(f"Text cells trimmed: {report.text_cells_trimmed}")
    lines.append(f"Title-case cells changed: {report.title_case_cells_changed}")

    lines.append("")
    lines.append("Email validation:")
    lines.append(f"Valid emails: {report.valid_emails}")
    lines.append(f"Invalid emails: {report.invalid_emails}")
    lines.append(f"Missing emails: {report.missing_emails}")

    lines.append("")
    lines.append("Phone validation:")
    lines.append(f"Valid phone numbers: {report.valid_phones}")
    lines.append(f"Invalid phone numbers: {report.invalid_phones}")
    lines.append(f"Missing phone numbers: {report.missing_phones}")
    lines.append(
        f"Phone numbers standardized: "
        f"{report.phone_numbers_standardized}"
    )

    lines.append("")
    lines.append("ZIP code validation:")
    lines.append(f"Valid ZIP codes: {report.valid_zip_codes}")
    lines.append(f"Invalid ZIP codes: {report.invalid_zip_codes}")
    lines.append(f"Missing ZIP codes: {report.missing_zip_codes}")
    lines.append(
        f"ZIP codes standardized: "
        f"{report.zip_codes_standardized}"
    )

    lines.append("")
    lines.append("Date validation:")
    lines.append(f"Valid dates: {report.valid_dates}")
    lines.append(f"Invalid dates: {report.invalid_dates}")
    lines.append(f"Missing dates: {report.missing_dates}")
    lines.append(f"Dates standardized: {report.dates_standardized}")

    lines.append("")
    lines.append("Currency validation:")
    lines.append(f"Valid currency values: {report.valid_currency_values}")
    lines.append(f"Invalid currency values: {report.invalid_currency_values}")
    lines.append(f"Missing currency values: {report.missing_currency_values}")
    lines.append(
        f"Currency values standardized: "
        f"{report.currency_values_standardized}"
    )

    lines.append("")
    lines.append("Missing values by column:")
    lines.append(missing_lines or "  None")

    lines.append("")
    lines.append("Completed successfully.")

    text = "\n".join(lines)

    text_path.write_text(
        text,
        encoding="utf-8",
    )

    return text_path, json_path