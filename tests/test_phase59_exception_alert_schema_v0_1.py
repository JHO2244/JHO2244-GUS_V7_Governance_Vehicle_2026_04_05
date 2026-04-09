"""
GUS v7 — Phase 59
Exception Logging & Alerts Schema Tests (v0.1)

STRICT:
- Validate structure only
- No inference
- Fail-closed enforcement
"""

from gus_v7.exception_logging_alerts.exception_alert_schema_v0_1 import (
    EXCEPTION_ALERT_KEYS,
    REQUIRED_FIELDS,
    INTEGER_FIELDS,
    VALID_COMPLIANCE_RESULTS,
    VALID_EXCEPTION_STATUS,
    VALID_ALERT_STATUS,
    NO_NEGATIVE_VALUES,
    NO_EXTRA_FIELDS_ALLOWED,
    VALIDATION_RULES,
    FAIL_CLOSED_BEHAVIOR,
)


def test_phase59_alert_keys_exact_match():
    expected = (
        "total_decisions",
        "governance_fail_count",
        "compliance_result",
        "exception_status",
        "alert_status",
    )
    assert EXCEPTION_ALERT_KEYS == expected


def test_phase59_required_fields_match_keys():
    assert REQUIRED_FIELDS == EXCEPTION_ALERT_KEYS


def test_phase59_integer_fields_exact_match():
    assert INTEGER_FIELDS == (
        "total_decisions",
        "governance_fail_count",
    )


def test_phase59_valid_compliance_results_defined():
    assert VALID_COMPLIANCE_RESULTS == (
        "COMPLIANT",
        "NON_COMPLIANT",
    )


def test_phase59_valid_exception_status_defined():
    assert VALID_EXCEPTION_STATUS == (
        "NO_EXCEPTION",
        "EXCEPTION_OPEN",
    )


def test_phase59_valid_alert_status_defined():
    assert VALID_ALERT_STATUS == (
        "NO_ALERT",
        "ALERT_RAISED",
    )


def test_phase59_non_negative_lock():
    assert NO_NEGATIVE_VALUES is True


def test_phase59_no_extra_fields_lock():
    assert NO_EXTRA_FIELDS_ALLOWED is True


def test_phase59_validation_rules_defined():
    assert "E1_STRUCTURE_LOCK" in VALIDATION_RULES
    assert "E8_NO_EXTRA_FIELDS_LOCK" in VALIDATION_RULES


def test_phase59_fail_closed_behavior():
    assert (
        FAIL_CLOSED_BEHAVIOR
        == "ANY_VIOLATION_RESULTS_IN_INVALID_ALERT"
    )
