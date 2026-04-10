"""
GUS v7 — Phase 61
Historical Decision Analytics Schema Tests (v0.1)

STRICT:
- Validate structure only
- No inference
- Fail-closed enforcement
"""

from gus_v7.historical_decision_analytics.historical_decision_analytics_schema_v0_1 import (
    HISTORICAL_DECISION_ANALYTICS_KEYS,
    REQUIRED_FIELDS,
    ALL_FIELDS_INTEGER,
    NO_NEGATIVE_VALUES,
    NO_EXTRA_FIELDS_ALLOWED,
    VALIDATION_RULES,
    FAIL_CLOSED_BEHAVIOR,
)


def test_phase61_history_keys_exact_match():
    expected = (
        "snapshot_count",
        "total_decisions_sum",
        "governance_pass_sum",
        "governance_fail_sum",
        "compliant_snapshot_count",
        "non_compliant_snapshot_count",
        "exception_open_snapshot_count",
        "alert_raised_snapshot_count",
    )
    assert HISTORICAL_DECISION_ANALYTICS_KEYS == expected


def test_phase61_required_fields_match_keys():
    assert REQUIRED_FIELDS == HISTORICAL_DECISION_ANALYTICS_KEYS


def test_phase61_integer_only_lock():
    assert ALL_FIELDS_INTEGER is True


def test_phase61_non_negative_lock():
    assert NO_NEGATIVE_VALUES is True


def test_phase61_no_extra_fields_lock():
    assert NO_EXTRA_FIELDS_ALLOWED is True


def test_phase61_validation_rules_defined():
    assert "H1_STRUCTURE_LOCK" in VALIDATION_RULES
    assert "H5_NO_EXTRA_FIELDS_LOCK" in VALIDATION_RULES


def test_phase61_fail_closed_behavior():
    assert (
        FAIL_CLOSED_BEHAVIOR
        == "ANY_VIOLATION_RESULTS_IN_INVALID_HISTORY_ANALYTICS"
    )
