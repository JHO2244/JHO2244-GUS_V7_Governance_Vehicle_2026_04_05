"""
GUS v7 — Phase 57
Governance Metrics Aggregation Schema Tests (v0.1)

STRICT:
- Validate structure only
- No inference
- Fail-closed enforcement
"""

from gus_v7.governance_metrics.governance_metrics_schema_v0_1 import (
    GOVERNANCE_METRICS_KEYS,
    REQUIRED_FIELDS,
    ALL_FIELDS_INTEGER,
    NO_NEGATIVE_VALUES,
    NO_EXTRA_FIELDS_ALLOWED,
    VALIDATION_RULES,
    FAIL_CLOSED_BEHAVIOR,
)


def test_phase57_metrics_keys_exact_match():
    expected = (
        "total_decisions",
        "execute_count",
        "block_count",
        "integrity_confirmed_count",
        "integrity_rejected_count",
        "governance_pass_count",
        "governance_fail_count",
    )
    assert GOVERNANCE_METRICS_KEYS == expected


def test_phase57_required_fields_match_keys():
    assert REQUIRED_FIELDS == GOVERNANCE_METRICS_KEYS


def test_phase57_integer_only_lock():
    assert ALL_FIELDS_INTEGER is True


def test_phase57_non_negative_lock():
    assert NO_NEGATIVE_VALUES is True


def test_phase57_no_extra_fields_lock():
    assert NO_EXTRA_FIELDS_ALLOWED is True


def test_phase57_validation_rules_defined():
    assert "M1_STRUCTURE_LOCK" in VALIDATION_RULES
    assert "M5_NO_EXTRA_FIELDS_LOCK" in VALIDATION_RULES


def test_phase57_fail_closed_behavior():
    assert (
        FAIL_CLOSED_BEHAVIOR
        == "ANY_VIOLATION_RESULTS_IN_INVALID_METRICS"
    )
