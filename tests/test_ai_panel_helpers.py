from src.ui.ai_panel import (
    _recommendation_value,
    _sorted_recommendations,
)


def test_recommendation_value_supports_dictionary():
    recommendation = {
        "priority": "high",
    }

    assert (
        _recommendation_value(
            recommendation,
            "priority",
        )
        == "high"
    )


def test_recommendations_are_sorted_by_priority():
    recommendations = [
        {
            "priority": "low",
            "title": "Low",
        },
        {
            "priority": "high",
            "title": "High",
        },
        {
            "priority": "medium",
            "title": "Medium",
        },
    ]

    sorted_recommendations = _sorted_recommendations(
        recommendations
    )

    assert [
        recommendation["priority"]
        for recommendation in sorted_recommendations
    ] == [
        "high",
        "medium",
        "low",
    ]