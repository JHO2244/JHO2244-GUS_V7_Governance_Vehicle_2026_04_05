"""
GUS v7 — Phase 62
Risk Assessment Builder Tests (v0.1)

STRICT:
- Validate deterministic signal counting only
- No inference
- Fail-closed enforcement
"""

from gus_v7.risk_assessment.risk_assessment_builder_v0_1 import (
    build_risk_assessment_v0_1,
)


def _low_history():
    return {
        "snapshot_count": 3,
        "total_decisions_sum": 9,
        "governance_pass_sum": 6,
        "governance_fail_sum": 3,
        "compliant_snapshot_count": 2,
        "non_compliant_snapshot_count": 1,
        "exception_open_snapshot_count": 0,
        "alert_raised_snapshot_count": 0,
    }


def _medium_history():
    return {
        "snapshot_count": 3,
        "total_decisions_sum": 9,
        "governance_pass_sum": 6,
        "governance_fail_sum": 3,
        "compliant_snapshot_count": 2,
        "non_compliant_snapshot_count": 1,
        "exception_open_snapshot_count": 1,
        "alert_raised_snapshot_count": 0,
    }


def _high_history():
    return {
        "snapshot_count": 3,
        "total_decisions_sum": 9,
        "governance_pass_sum": 2,
        "governance_fail_sum": 5,
        "compliant_snapshot_count": 1,
        "non_compliant_snapshot_count": 2,
        "exception_open_snapshot_count": 1,
        "alert_raised_snapshot_count": 1,
    }


def test_phase62_builder_returns_low_risk_when_no_signals():
    result = build_risk_assessment_v0_1(_low_history())
    assert result == {
        "risk_level": "LOW",
        "risk_flags_count": 0,
        "instability_detected": False,
    }


def test_phase62_builder_returns_medium_risk_when_one_signal():
    result = build_risk_assessment_v0_1(_medium_history())
    assert result == {
        "risk_level": "MEDIUM",
        "risk_flags_count": 1,
        "instability_detected": True,
    }


def test_phase62_builder_returns_high_risk_when_two_or_more_signals():
    result = build_risk_assessment_v0_1(_high_history())
    assert result == {
        "risk_level": "HIGH",
        "risk_flags_count": 4,
        "instability_detected": True,
    }


def test_phase62_builder_rejects_missing_field():
    history = _low_history()
    del history["alert_raised_snapshot_count"]
    try:
        build_risk_assessment_v0_1(history)
        assert False
    except ValueError as exc:
        assert str(exc) == "INVALID_HISTORY"


def test_phase62_builder_rejects_extra_field():
    history = _low_history()
    history["extra"] = 1
    try:
        build_risk_assessment_v0_1(history)
        assert False
    except ValueError as exc:
        assert str(exc) == "INVALID_HISTORY"


def test_phase62_builder_rejects_negative_value():
    history = _low_history()
    history["governance_pass_sum"] = -1
    try:
        build_risk_assessment_v0_1(history)
        assert False
    except ValueError as exc:
        assert str(exc) == "INVALID_HISTORY"


def test_phase62_builder_rejects_non_integer_value():
    history = _low_history()
    history["governance_pass_sum"] = "6"
    try:
        build_risk_assessment_v0_1(history)
        assert False
    except ValueError as exc:
        assert str(exc) == "INVALID_HISTORY"
