from __future__ import annotations

from html import escape

import streamlit as st

from src.models import CleaningReport


def _score_status(score: float) -> tuple[str, str]:
    if score >= 90:
        return "Excellent", "#15803D"

    if score >= 80:
        return "Good", "#F04F64"

    if score >= 70:
        return "Needs attention", "#D97706"

    return "High risk", "#DC2626"


def _render_quality_hero(
    score: float,
    rating: str,
    accent_color: str,
) -> None:
    safe_score = max(0.0, min(float(score), 100.0))
    safe_rating = escape(rating)

    st.markdown(
        f"""
<div class="quality-hero">
    <div class="quality-hero__score">
        <div class="quality-hero__label">
            Overall data quality
        </div>
        <div class="quality-hero__value">
            {safe_score:.1f}%
        </div>
    </div>
    <div class="quality-hero__rating">
        <div class="quality-hero__label">
            Rating
        </div>
        <div
            class="quality-hero__badge"
            style="
                color: {accent_color};
                background: {accent_color}14;
                border-color: {accent_color}30;
            "
        >
            {safe_rating}
        </div>
    </div>
</div>
        """,
        unsafe_allow_html=True,
    )

def _inject_metric_styles() -> None:
    st.markdown(
        """
        <style>
        .quality-hero {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 2rem;
            padding: 1.25rem 1.4rem;
            min-height: 10rem;
            margin: 0.25rem 0 1.35rem;
            background: linear-gradient(
                135deg,
                rgba(240, 79, 100, 0.055),
                rgba(255, 255, 255, 0.96) 58%
            );
            border: 1px solid rgba(240, 79, 100, 0.16);
            border-radius: 18px;
            box-shadow:
                0 1px 2px rgba(36, 38, 51, 0.03),
                0 8px 28px rgba(36, 38, 51, 0.035);
        }

        .quality-hero__label {
            margin-bottom: 0.35rem;
            color: #6b7280;
            font-size: 0.9rem;
            font-weight: 500;
        }

        .quality-hero__value {
            color: #242633;
            font-size: clamp(2.75rem, 4vw, 3.75rem);
            font-weight: 650;
            line-height: 1;
            letter-spacing: -0.055em;
        }

        .quality-hero__rating {
            min-width: 10rem;
            text-align: right;
        }

        .quality-hero__badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-width: 7.5rem;
            padding: 0.55rem 1.1rem;
            border: 1px solid;
            border-radius: 999px;
            font-size: 1.1rem;
            font-weight: 650;
        }
        
        .results-navigation-gap {
            height: clamp(2rem, 4vw, 3.5rem);
        }

        div[data-testid="stProgress"] > div > div {
            border-radius: 999px;
        }

        div[data-testid="stProgress"]
        [role="progressbar"] {
            min-height: 0.65rem;
            border-radius: 999px;
        }

        @media (max-width: 700px) {
            .quality-hero {
                align-items: flex-start;
                flex-direction: column;
                gap: 1rem;
                padding: 1.25rem;
            }

            .quality-hero__rating {
                min-width: 0;
                text-align: left;
            }

            .quality-hero__value {
                font-size: 3rem;
            }
            
            .results-section-gap {
                height: clamp(2.5rem, 5vw, 4.5rem);
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _render_dimension_progress(
    label: str,
    score: float,
) -> None:
    safe_score = max(0.0, min(float(score), 100.0))

    st.progress(
        safe_score / 100,
        text=f"**{label}: {safe_score:.1f}%**",
    )


def render_metrics(
    report: CleaningReport,
) -> None:
    _inject_metric_styles()

    quality = report.quality_score
    profile = report.dataset_profile

    rating, accent_color = _score_status(
        quality.overall
    )

    st.subheader("Results overview")

    _render_quality_hero(
        score=quality.overall,
        rating=rating,
        accent_color=accent_color,
    )

    first_row = st.columns(2)
    second_row = st.columns(2)

    first_row[0].metric(
        "Rows imported",
        report.input_rows,
    )

    first_row[1].metric(
        "Rows exported",
        report.output_rows,
        delta=report.output_rows - report.input_rows,
    )

    second_row[0].metric(
        "Duplicates removed",
        report.duplicate_rows_removed,
    )

    second_row[1].metric(
        "Missing cells",
        profile.missing_cells,
    )


def render_quality_dimensions(
    report: CleaningReport,
) -> None:
    quality = report.quality_score

    _render_dimension_progress(
        "Completeness",
        quality.completeness,
    )

    _render_dimension_progress(
        "Validity",
        quality.validity,
    )

    _render_dimension_progress(
        "Uniqueness",
        quality.uniqueness,
    )

    _render_dimension_progress(
        "Consistency",
        quality.consistency,
    )