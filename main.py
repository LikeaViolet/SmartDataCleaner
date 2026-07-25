from __future__ import annotations

import argparse
from pathlib import Path

from src.cleaner import clean_dataset
from src.io_utils import read_dataset, write_dataset
from src.reporting import save_reports


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Clean CSV or Excel data and generate a change report."
    )
    parser.add_argument(
        "input_file",
        help="Path to the source .csv, .xlsx, or .xls file.",
    )
    parser.add_argument(
        "--output",
        default="output/cleaned_data.xlsx",
        help="Output path ending in .csv or .xlsx.",
    )
    parser.add_argument(
        "--title-case",
        nargs="*",
        default=[],
        metavar="COLUMN",
        help=(
            "Optional columns to convert to title case. "
            "Example: --title-case Name City"
        ),
    )

    parser.add_argument(
        "--ai-insights",
        action="store_true",
        help="Generate AI-powered data-quality insights.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    try:
        source = read_dataset(args.input_file)

        cleaned, report = clean_dataset(
            source,
            title_case_columns=args.title_case,
            generate_ai=args.ai_insights,
        )

        output_path = write_dataset(
            cleaned,
            args.output,
        )

        report_dir = Path(args.output).parent

        text_report, json_report = save_reports(
            report,
            report_dir,
        )

        print("Cleaning completed successfully.")
        print(f"Cleaned file: {output_path}")
        print(f"Text report: {text_report}")
        print(f"JSON report: {json_report}")
        print(
            f"Rows: {report.input_rows} "
            f"-> {report.output_rows} | "
            f"Duplicates removed: "
            f"{report.duplicate_rows_removed}"
        )

        if args.ai_insights:
            if report.ai_summary:
                print("AI insights generated successfully.")
            elif report.ai_error:
                print(
                    "Cleaning succeeded, but AI insights "
                    f"were unavailable: {report.ai_error}"
                )

    except (FileNotFoundError, ValueError) as exc:
        raise SystemExit(
            f"Error: {exc}"
        ) from exc


if __name__ == "__main__":
    main()
