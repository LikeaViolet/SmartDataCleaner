from src.models import QualityScore


def _percentage(part: int, whole: int) -> float:
    if whole <= 0:
        return 100.0

    return round(max(0.0, min(100.0, part / whole * 100)), 1)


def quality_grade(score: float) -> str:
    if score >= 95:
        return "Excellent"

    if score >= 85:
        return "Good"

    if score >= 70:
        return "Fair"

    return "Poor"


def calculate_quality_score(
    *,
    input_rows: int,
    output_rows: int,
    total_data_cells: int,
    missing_data_cells: int,
    validation_checks: int,
    invalid_values: int,
    duplicate_rows_removed: int,
) -> QualityScore:
    """
    Calculate quality metrics after cleaning.

    Completeness:
        Percentage of ordinary data cells that are populated.

    Validity:
        Percentage of checked email, phone, and date values that are valid.

    Uniqueness:
        Percentage of original nonblank rows that were not duplicates.

    Consistency:
        Temporarily 100 until specific post-cleaning consistency rules exist.
    """

    populated_cells = max(total_data_cells - missing_data_cells, 0)
    completeness = _percentage(populated_cells, total_data_cells)

    valid_checks = max(validation_checks - invalid_values, 0)
    validity = _percentage(valid_checks, validation_checks)

    unique_rows = max(input_rows - duplicate_rows_removed, 0)
    uniqueness = _percentage(unique_rows, input_rows)

    # Do not penalize values that the cleaner successfully corrected.
    consistency = 100.0

    overall = round(
        (
            completeness
            + validity
            + uniqueness
            + consistency
        )
        / 4,
        1,
    )

    return QualityScore(
        completeness=completeness,
        validity=validity,
        uniqueness=uniqueness,
        consistency=consistency,
        overall=overall,
        grade=quality_grade(overall),
    )