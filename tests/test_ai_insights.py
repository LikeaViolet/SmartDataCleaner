import pandas as pd


from src.ai_insights import (
    AIInsightReport,
    AIInsightResult,
    AIRecommendation,
)
from src.cleaner import clean_dataset


def test_ai_is_disabled_by_default():
    source = pd.DataFrame(
        {
            "Name": ["Alice"],
            "Email": ["alice@example.com"],
        }
    )

    _, report = clean_dataset(source)

    assert report.ai_summary is None
    assert report.ai_strengths == []
    assert report.ai_risks == []
    assert report.ai_recommendations == []
    assert report.ai_error is None


def test_cleaner_stores_mocked_ai_insights(monkeypatch):
    mocked_insights = AIInsightReport(
        summary="The dataset is mostly healthy.",
        strengths=["All populated emails are valid."],
        risks=["One duplicate was detected."],
        recommendations=[
            AIRecommendation(
                priority="medium",
                category="uniqueness",
                title="Review duplicate records",
                explanation="A duplicate may distort totals.",
                suggested_action="Confirm the correct retained row.",
            )
        ],
    )

    def fake_generate_ai_insights(report):
        return AIInsightResult(
            insights=mocked_insights,
        )

    monkeypatch.setattr(
        "src.cleaner.generate_ai_insights",
        fake_generate_ai_insights,
    )

    source = pd.DataFrame(
        {
            "Name": ["Alice"],
            "Email": ["alice@example.com"],
        }
    )

    _, report = clean_dataset(
        source,
        generate_ai=True,
    )

    assert report.ai_summary == "The dataset is mostly healthy."
    assert report.ai_strengths == [
        "All populated emails are valid."
    ]
    assert report.ai_risks == [
        "One duplicate was detected."
    ]
    assert len(report.ai_recommendations) == 1
    assert (
        report.ai_recommendations[0]["priority"]
        == "medium"
    )