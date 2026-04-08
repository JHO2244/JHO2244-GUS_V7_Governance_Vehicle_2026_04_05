"""
GUS v7 — Phase 41
Decision Integrity Schema Tests (v0.1)

STRICT:
- Validate structure only
- No inference
- Fail-closed enforcement
"""

from gus_v7.decision_integrity.decision_integrity_schema_v0_1 import (
    DECISION_KEYS,
    VALID_DECISION_OUTPUTS,
    VALID_INTEGRITY_STATUS_VALUES,
    REQUIRED_NON_EMPTY_FIELDS,
    NO_EXTRA_FIELDS_ALLOWED,
    IMMUTABLE_AFTER_CREATION,
    VALIDATION_RULES,
    FAIL_CLOSED_BEHAVIOR,
)


def test_phase41_decision_keys_exact_match():
    expected = (
        "decision_id",
        "case_id",
        "decision_output",
        "decision_basis",
        "evidence_binding_id",
        "timestamp",
        "integrity_status",
    )
    assert DECISION_KEYS == expected


def test_phase41_required_fields_match_keys():
    assert set(REQUIRED_NON_EMPTY_FIELDS) == set(DECISION_KEYS)


def test_phase41_valid_decision_outputs_defined():
    assert VALID_DECISION_OUTPUTS == (
        "PASS",
        "FAIL",
        "INSUFFICIENT_EVIDENCE",
        "OUT_OF_SCOPE",
    )


def test_phase41_valid_integrity_status_values():
    assert VALID_INTEGRITY_STATUS_VALUES == (
        "pending",
        "valid",
        "invalid",
    )


def test_phase41_no_extra_fields_lock():
    assert NO_EXTRA_FIELDS_ALLOWED is True


def test_phase41_immutability_lock():
    assert IMMUTABLE_AFTER_CREATION is True


def test_phase41_validation_rules_defined():
    assert "D1_STRUCTURE_LOCK" in VALIDATION_RULES
    assert "D6_IMMUTABILITY_LOCK" in VALIDATION_RULES


def test_phase41_fail_closed_behavior():
    assert (
        FAIL_CLOSED_BEHAVIOR
        == "ANY_VIOLATION_RESULTS_IN_INVALID_DECISION"
    )
