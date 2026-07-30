from src.ui.metrics import _score_status


def test_excellent_quality_status():
    label, color = _score_status(95)

    assert label == "Excellent"
    assert color == "#15803D"


def test_good_quality_status():
    label, _ = _score_status(85)

    assert label == "Good"


def test_attention_quality_status():
    label, _ = _score_status(75)

    assert label == "Needs attention"


def test_high_risk_quality_status():
    label, _ = _score_status(60)

    assert label == "High risk"