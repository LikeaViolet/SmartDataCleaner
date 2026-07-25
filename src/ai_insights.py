from __future__ import annotations

import json
import os
from typing import Literal
from dataclasses import dataclass


from pydantic import BaseModel, Field

from src.models import CleaningReport

from dotenv import load_dotenv

load_dotenv()




class AIRecommendation(BaseModel):
    priority: Literal["high", "medium", "low"]
    category: Literal[
        "completeness",
        "validity",
        "uniqueness",
        "consistency",
        "schema",
        "usability",
    ]
    title: str = Field(min_length=1, max_length=100)
    explanation: str = Field(min_length=1, max_length=500)
    suggested_action: str = Field(min_length=1, max_length=300)


class AIInsightReport(BaseModel):
    summary: str = Field(min_length=1, max_length=700)
    strengths: list[str] = Field(default_factory=list, max_length=5)
    risks: list[str] = Field(default_factory=list, max_length=5)
    recommendations: list[AIRecommendation] = Field(
        default_factory=list,
        max_length=8,
    )

@dataclass
class AIInsightResult:
    insights: AIInsightReport | None
    error: str | None = None


SYSTEM_PROMPT = """
You are a data-quality analyst reviewing a deterministic cleaning report.

Your job is to explain and prioritize the evidence already present in the
report. Do not invent columns, counts, errors, business meaning, or causes.

Rules:
- Treat the supplied report as the only source of truth.
- Clearly distinguish missing columns from columns that were checked and had
  zero invalid values.
- Do not claim that a value is invalid unless the report says it is invalid.
- Do not recommend removing records merely because values are missing.
- Keep recommendations practical and specific.
- Prioritize genuine risks over cosmetic formatting changes.
- Mention positive findings as well as weaknesses.
- Avoid repeating the same recommendation in different wording.
"""


def generate_ai_insights(
    report: CleaningReport,
    model: str = "gpt-5.6",
) -> AIInsightResult:
    """
    Generate structured AI insights from an existing deterministic report.

    Returns None when no API key is configured or when the API call fails.
    The cleaning workflow should still succeed without AI.
    """
    try:
        from openai import OpenAI
    except ImportError:
        return AIInsightResult(
            insights=None,
            error="The OpenAI SDK is not installed.",
        )



    if not os.getenv("OPENAI_API_KEY"):
        return AIInsightResult(
            insights=None,
            error="OPENAI_API_KEY is not configured.",
        )

    client = OpenAI()

    report_payload = report.to_dict()

    try:
        response = client.responses.parse(
            model=model,
            input=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": (
                        "Analyze this Smart Data Cleaner report and return "
                        "a concise, actionable data-quality assessment:\n\n"
                        + json.dumps(
                            report_payload,
                            indent=2,
                            default=str,
                        )
                    ),
                },
            ],
            text_format=AIInsightReport,
        )
    except Exception as exc:
        return AIInsightResult(
            insights=None,
            error=str(exc),
        )

    return AIInsightResult(
        insights=response.output_parsed,
    )