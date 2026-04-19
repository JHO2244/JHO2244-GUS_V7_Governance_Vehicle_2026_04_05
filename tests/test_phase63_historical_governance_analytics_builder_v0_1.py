"""
GUS v7 — Phase 63
Historical Governance Analytics Builder Tests (v0.1)

STRICT:
- Validate deterministic historical analytics only
- No inference
- Fail-closed enforcement
"""

from gus_v7.historical_governance_analytics.historical_governance_analytics_builder_v0_1 import (
    build_historical_governance_analytics_v0_1,
)


def _history_windows():
    return [
        {
            "total_decisions": 3,
            "execute_count": 2,
            "block_count": 1,
            "integrity_confirmed_count": 2,
            "integrity_rejected_count": 1,
            "governance_pass_count": 2,
            "governance_fail_count": 1,
        },
        {
            "total_decisions": 4,
            "execute_count": 3,
            "block_count": 1,
            "integrity_confirmed_count": 3,
            "integrity_rejected_count": 1,
            "governance_pass_count": 2,
            "governance_fail_count": 2,
        },
        {
            "total_decisions": 3,
            "execute_count": 2,
            "block_count": 1,
            "integrity_confirmed_count": 2,
            "integrity_rejected_count": 1,
            "governance_pass_count": 1,
            "governance_fail_count": 2,
        },
    ]


def test_phase63_builder_accepts_valid_history_windows():
    result = build_historical_governance_analytics_v0_1(_history_windows())

    assert result == {
        "history_window_count": 3,
        "total_decisions_sum": 10,
        "governance_pass_sum": 5,
        "governance_fail_sum": 5,
        "execute_sum": 7,
        "block_sum": 3,
        "integrity_confirmed_sum": 7,
        "integrity_rejected_sum": 3,
        "governance_pass_rate": "0.5000",
        "governance_fail_rate": "0.5000",
        "execute_rate": "0.7000",
        "block_rate": "0.3000",
        "governance_trend": "DECLINING",
        "governance_pattern_summary": "BALANCED",
        "execution_pattern_summary": "EXECUTE_DOMINANT",
        "integrity_pattern_summary": "INTEGRITY_CONFIRMED_DOMINANT",
    }


def test_phase63_builder_rejects_empty_input():
    try:
        build_historical_governance_analytics_v0_1([])
        assert False
    except ValueError as exc:
        assert str(exc) == "INVALID_HISTORY_WINDOWS"


def test_phase63_builder_rejects_non_list_input():
    try:
        build_historical_governance_analytics_v0_1("not-a-list")
        assert False
    except ValueError as exc:
        assert str(exc) == "INVALID_HISTORY_WINDOWS"


def test_phase63_builder_rejects_missing_field():
    windows = _history_windows()
    del windows[0]["execute_count"]

    try:
        build_historical_governance_analytics_v0_1(windows)
        assert False
    except ValueError as exc:
        assert str(exc) == "INVALID_HISTORY_WINDOW"


def test_phase63_builder_rejects_negative_integer():
    windows = _history_windows()
    windows[0]["governance_fail_count"] = -1

    try:
        build_historical_governance_analytics_v0_1(windows)
        assert False
    except ValueError as exc:
        assert str(exc) == "INVALID_HISTORY_WINDOW"


def test_phase63_builder_rejects_non_integer_value():
    windows = _history_windows()
    windows[0]["block_count"] = "1"

    try:
        build_historical_governance_analytics_v0_1(windows)
        assert False
    except ValueError as exc:
        assert str(exc) == "INVALID_HISTORY_WINDOW"


def test_phase63_builder_returns_stable_trend_when_first_and_last_match():
    windows = [
        {
            "total_decisions": 2,
            "execute_count": 1,
            "block_count": 1,
            "integrity_confirmed_count": 1,
            "integrity_rejected_count": 1,
            "governance_pass_count": 1,
            "governance_fail_count": 1,
        },
        {
            "total_decisions": 4,
            "execute_count": 2,
            "block_count": 2,
            "integrity_confirmed_count": 2,
            "integrity_rejected_count": 2,
            "governance_pass_count": 3,
            "governance_fail_count": 1,
        },
        {
            "total_decisions": 2,
            "execute_count": 1,
            "block_count": 1,
            "integrity_confirmed_count": 1,
            "integrity_rejected_count": 1,
            "governance_pass_count": 1,
            "governance_fail_count": 1,
        },
    ]

    result = build_historical_governance_analytics_v0_1(windows)

    assert result["governance_trend"] == "STABLE"
