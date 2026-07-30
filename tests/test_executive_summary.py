from types import SimpleNamespace

from src.ui.executive_summary import (
    build_executive_summary,
)


def make_report(
    *,
    overall: float = 89.8,
    grade: str = "Good",
    duplicates: int = 1,
    missing_cells: int = 5,
):
    return SimpleNamespace(
        quality_score=SimpleNamespace(
            overall=overall,
            grade=grade,
        ),
        dataset_profile=SimpleNamespace(
            missing_cells=missing_cells,
        ),
        duplicate_rows_removed=duplicates,
    )


def test_summary_reports_quality():
    report = make_report()

    result = build_executive_summary(report)

    assert result[0] == (
        "Dataset quality is good at 89.8%."
    )


def test_summary_reports_duplicate_and_missing_counts():
    report = make_report()

    result = build_executive_summary(report)

    assert "1 duplicate record was removed." in result
    assert "5 missing cells remain." in result


def test_summary_recommends_resolving_missing_values():
    report = make_report(missing_cells=5)

    result = build_executive_summary(report)

    assert result[-1] == (
        "Recommended next step: review and resolve missing "
        "values before importing the dataset."
    )


def test_excellent_complete_dataset_is_ready():
    report = make_report(
        overall=96.0,
        grade="Excellent",
        missing_cells=0,
    )

    result = build_executive_summary(report)

    assert result[-1] == (
        "Recommended next step: the dataset is ready for "
        "final review or import."
    )