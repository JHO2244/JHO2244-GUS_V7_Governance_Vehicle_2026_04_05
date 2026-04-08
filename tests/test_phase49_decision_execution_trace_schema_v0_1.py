"""
GUS v7 — Phase 49
Decision Execution Trace Schema Tests (v0.1)

STRICT:
- Validate structure only
- No inference
- Fail-closed enforcement
"""

from gus_v7.decision_execution_trace.decision_execution_trace_schema_v0_1 import (
    DECISION_EXECUTION_TRACE_KEYS,
    VALID_EXECUTION_RESULTS,
    VALID_FINAL_INTEGRITY_VERDICTS,
    REQUIRED_NON_EMPTY_FIELDS,
    NO_EXTRA_FIELDS_ALLOWED,
    IMMUTABLE_AFTER_LOGGING,
    VALIDATION_RULES,
    FAIL_CLOSED_BEHAVIOR,
)


def test_phase49_trace_keys_exact_match():
    expected = (
        "trace_id",
        "decision_id",
        "case_id",
        "evidence_binding_id",
        "integrity_envelope_id",
        "final_integrity_verdict",
        "execution_result",
        "trace_timestamp",
        "trace_sequence",
    )
    assert DECISION_EXECUTION_TRACE_KEYS == expected


def test_phase49_required_fields_match_keys():
    assert set(REQUIRED_NON_EMPTY_FIELDS) == set(DECISION_EXECUTION_TRACE_KEYS)


def test_phase49_valid_execution_results_defined():
    assert VALID_EXECUTION_RESULTS == (
        "EXECUTE",
        "BLOCK",
    )


def test_phase49_valid_final_integrity_verdicts_defined():
    assert VALID_FINAL_INTEGRITY_VERDICTS == (
        "INTEGRITY_CONFIRMED",
        "INTEGRITY_REJECTED",
    )


def test_phase49_no_extra_fields_lock():
    assert NO_EXTRA_FIELDS_ALLOWED is True


def test_phase49_immutability_lock():
    assert IMMUTABLE_AFTER_LOGGING is True


def test_phase49_validation_rules_defined():
    assert "T1_STRUCTURE_LOCK" in VALIDATION_RULES
    assert "T6_IMMUTABILITY_LOCK" in VALIDATION_RULES


def test_phase49_fail_closed_behavior():
    assert (
        FAIL_CLOSED_BEHAVIOR
        == "ANY_VIOLATION_RESULTS_IN_INVALID_TRACE"
    )
