"""
GUS v7 — Phase 42
Decision Schema Lock Tests (v0.1)

STRICT:
- Validate schema lock bindings only
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
from gus_v7.decision_schema_lock.decision_schema_lock_v0_1 import (
    CANONICAL_DECISION_SCHEMA_MODULE,
    LOCKED_DECISION_KEYS,
    LOCKED_VALID_DECISION_OUTPUTS,
    LOCKED_VALID_INTEGRITY_STATUS_VALUES,
    LOCKED_REQUIRED_NON_EMPTY_FIELDS,
    LOCKED_NO_EXTRA_FIELDS_ALLOWED,
    LOCKED_IMMUTABLE_AFTER_CREATION,
    LOCKED_VALIDATION_RULES,
    LOCKED_FAIL_CLOSED_BEHAVIOR,
    PARALLEL_SCHEMA_DEFINITIONS_FORBIDDEN,
    SCHEMA_FIELD_DRIFT_FORBIDDEN,
    SCHEMA_OUTPUT_DRIFT_FORBIDDEN,
    SCHEMA_STATUS_DRIFT_FORBIDDEN,
    LOCK_RULES,
    FAIL_CLOSED_LOCK_BEHAVIOR,
)


def test_phase42_canonical_schema_module_locked():
    assert (
        CANONICAL_DECISION_SCHEMA_MODULE
        == "gus_v7.decision_integrity.decision_integrity_schema_v0_1"
    )


def test_phase42_decision_keys_binding_matches_phase41():
    assert LOCKED_DECISION_KEYS == DECISION_KEYS


def test_phase42_decision_outputs_binding_matches_phase41():
    assert LOCKED_VALID_DECISION_OUTPUTS == VALID_DECISION_OUTPUTS


def test_phase42_integrity_status_binding_matches_phase41():
    assert (
        LOCKED_VALID_INTEGRITY_STATUS_VALUES
        == VALID_INTEGRITY_STATUS_VALUES
    )


def test_phase42_required_fields_binding_matches_phase41():
    assert LOCKED_REQUIRED_NON_EMPTY_FIELDS == REQUIRED_NON_EMPTY_FIELDS


def test_phase42_structure_lock_binding_matches_phase41():
    assert LOCKED_NO_EXTRA_FIELDS_ALLOWED is NO_EXTRA_FIELDS_ALLOWED


def test_phase42_immutability_binding_matches_phase41():
    assert LOCKED_IMMUTABLE_AFTER_CREATION is IMMUTABLE_AFTER_CREATION


def test_phase42_validation_rules_binding_matches_phase41():
    assert LOCKED_VALIDATION_RULES == VALIDATION_RULES


def test_phase42_fail_closed_binding_matches_phase41():
    assert LOCKED_FAIL_CLOSED_BEHAVIOR == FAIL_CLOSED_BEHAVIOR


def test_phase42_parallel_schema_definitions_forbidden():
    assert PARALLEL_SCHEMA_DEFINITIONS_FORBIDDEN is True


def test_phase42_schema_field_drift_forbidden():
    assert SCHEMA_FIELD_DRIFT_FORBIDDEN is True


def test_phase42_schema_output_drift_forbidden():
    assert SCHEMA_OUTPUT_DRIFT_FORBIDDEN is True


def test_phase42_schema_status_drift_forbidden():
    assert SCHEMA_STATUS_DRIFT_FORBIDDEN is True


def test_phase42_lock_rules_defined():
    assert "DSL1_AUTHORITY_SOURCE_LOCK" in LOCK_RULES
    assert "DSL6_FAIL_CLOSED_BINDING_LOCK" in LOCK_RULES


def test_phase42_fail_closed_lock_behavior():
    assert (
        FAIL_CLOSED_LOCK_BEHAVIOR
        == "ANY_SCHEMA_MISMATCH_RESULTS_IN_LOCK_FAILURE"
    )
