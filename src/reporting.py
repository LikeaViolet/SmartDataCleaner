from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from src.models import CleaningReport


def format_text_report(report: CleaningReport) -> str:
    lines: list[str] = []

    profile = report.dataset_profile
    quality = report.quality_score

    lines.append("SMART DATA CLEANER REPORT")
    lines.append("")

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
        lines.append("")
        lines.append(f"{column.name}:")
        lines.append(
            f"  Detected type: {column.detected_type or 'general'}"
        )
        lines.append(f"  Pandas dtype: {column.dtype}")
        lines.append(
            f"  Non-missing values: {column.non_missing}"
        )
        lines.append(
            f"  Missing values: {column.missing} "
            f"({column.missing_percentage:.1f}%)"
        )
        lines.append(
            f"  Unique values: {column.unique_values} "
            f"({column.unique_percentage:.1f}%)"
        )

    lines.append("")
    lines.append("DATA QUALITY")
    lines.append(f"Overall score: {quality.overall:.1f}%")
    lines.append(f"Grade: {quality.grade}")
    lines.append(
        f"Completeness: {quality.completeness:.1f}%"
    )
    lines.append(f"Validity: {quality.validity:.1f}%")
    lines.append(
        f"Uniqueness: {quality.uniqueness:.1f}%"
    )
    lines.append(
        f"Consistency: {quality.consistency:.1f}%"
    )

    lines.append("")
    lines.append(f"Rows imported: {report.input_rows}")
    lines.append(f"Rows exported: {report.output_rows}")

    lines.append("")
    lines.append("Cleaning:")
    lines.append(
        f"Blank rows removed: {report.blank_rows_removed}"
    )
    lines.append(
        f"Duplicate rows removed: "
        f"{report.duplicate_rows_removed}"
    )
    lines.append(
        f"Text cells trimmed: {report.text_cells_trimmed}"
    )
    lines.append(
        f"Title-case cells changed: "
        f"{report.title_case_cells_changed}"
    )

    lines.append("")
    lines.append("Email validation:")
    lines.append(f"Valid emails: {report.valid_emails}")
    lines.append(f"Invalid emails: {report.invalid_emails}")
    lines.append(f"Missing emails: {report.missing_emails}")

    lines.append("")
    lines.append("Phone validation:")
    lines.append(
        f"Valid phone numbers: {report.valid_phones}"
    )
    lines.append(
        f"Invalid phone numbers: {report.invalid_phones}"
    )
    lines.append(
        f"Missing phone numbers: {report.missing_phones}"
    )
    lines.append(
        f"Phone numbers standardized: "
        f"{report.phone_numbers_standardized}"
    )

    lines.append("")
    lines.append("ZIP code validation:")
    lines.append(
        f"Valid ZIP codes: {report.valid_zip_codes}"
    )
    lines.append(
        f"Invalid ZIP codes: {report.invalid_zip_codes}"
    )
    lines.append(
        f"Missing ZIP codes: {report.missing_zip_codes}"
    )
    lines.append(
        f"ZIP codes standardized: "
        f"{report.zip_codes_standardized}"
    )

    lines.append("")
    lines.append("Date validation:")
    lines.append(f"Valid dates: {report.valid_dates}")
    lines.append(f"Invalid dates: {report.invalid_dates}")
    lines.append(f"Missing dates: {report.missing_dates}")
    lines.append(
        f"Dates standardized: {report.dates_standardized}"
    )

    lines.append("")
    lines.append("Currency validation:")
    lines.append(
        f"Valid currency values: "
        f"{report.valid_currency_values}"
    )
    lines.append(
        f"Invalid currency values: "
        f"{report.invalid_currency_values}"
    )
    lines.append(
        f"Missing currency values: "
        f"{report.missing_currency_values}"
    )
    lines.append(
        f"Currency values standardized: "
        f"{report.currency_values_standardized}"
    )

    lines.append("")
    lines.append("AI DATA QUALITY INSIGHTS")

    if report.ai_summary:
        lines.append("")
        lines.append("Summary:")
        lines.append(report.ai_summary)

        lines.append("")
        lines.append("Strengths:")

        for strength in report.ai_strengths:
            lines.append(f"  - {strength}")

        lines.append("")
        lines.append("Risks:")

        for risk in report.ai_risks:
            lines.append(f"  - {risk}")

        lines.append("")
        lines.append("Recommendations:")

        for recommendation in report.ai_recommendations:
            priority = recommendation["priority"].upper()

            lines.append("")
            lines.append(
                f"  [{priority}] "
                f"{recommendation['title']}"
            )
            lines.append(
                f"    Category: "
                f"{recommendation['category']}"
            )
            lines.append(
                f"    Why: "
                f"{recommendation['explanation']}"
            )
            lines.append(
                f"    Action: "
                f"{recommendation['suggested_action']}"
            )

    elif report.ai_error:
        lines.append(
            f"AI insights unavailable: {report.ai_error}"
        )

    else:
        lines.append(
            "Not generated. Enable AI insights to include "
            "recommendations."
        )

    lines.append("")
    lines.append("Missing values by column:")

    for column, missing in report.missing_values_by_column.items():
        lines.append(f"  - {column}: {missing}")

    lines.append("")
    lines.append("Completed successfully.")

    return "\n".join(lines)


def report_to_dict(report: CleaningReport) -> dict:
    return asdict(report)


def save_reports(
    report: CleaningReport,
    output_directory: Path,
) -> tuple[Path, Path]:
    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    text_path = output_directory / "cleaning_report.txt"
    json_path = output_directory / "cleaning_report.json"

    text_path.write_text(
        format_text_report(report),
        encoding="utf-8",
    )

    json_path.write_text(
        json.dumps(
            report_to_dict(report),
            indent=2,
            default=str,
        ),
        encoding="utf-8",
    )

    return text_path, json_path