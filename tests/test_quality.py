import pytest

from src.quality import calculate_quality_score, quality_grade


@pytest.mark.parametrize(
    ("score", "expected"),
    [
        (100, "Excellent"),
        (95, "Excellent"),
        (94.9, "Good"),
        (85, "Good"),
        (84.9, "Fair"),
        (70, "Fair"),
        (69.9, "Poor"),
    ],
)
def test_quality_grade(score, expected):
    assert quality_grade(score) == expected


def test_calculate_quality_score():
    result = calculate_quality_score(
        input_rows=100,
        output_rows=95,
        total_data_cells=400,
        missing_data_cells=20,
        validation_checks=180,
        invalid_values=9,
        duplicate_rows_removed=5,
    )

    assert result.completeness == 95.0
    assert result.validity == 95.0
    assert result.uniqueness == 95.0
    assert result.consistency == 100.0
    assert result.overall == 96.2
    assert result.grade == "Excellent"


def test_empty_dataset_receives_safe_scores():
    result = calculate_quality_score(
        input_rows=0,
        output_rows=0,
        total_data_cells=0,
        missing_data_cells=0,
        validation_checks=0,
        invalid_values=0,
        duplicate_rows_removed=0,
    )

    assert result.completeness == 100.0
    assert result.validity == 100.0
    assert result.uniqueness == 100.0