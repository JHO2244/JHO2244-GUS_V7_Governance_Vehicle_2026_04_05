import pytest

from gus_v7.decision_conflict_detection.decision_conflict_detection_validator_v0_1 import (
    validate_decision_conflict_detection_v0_1,
)


def _decision(case_id, binding_id, output):
    return {
        "case_id": case_id,
        "evidence_binding_id": binding_id,
        "decision_output": output,
    }


def test_attack003_conflicting_decisions_detected():
    a = _decision("CASE-001", "BIND-001", "PASS")
    b = _decision("CASE-001", "BIND-001", "FAIL")

    assert validate_decision_conflict_detection_v0_1(a, b) == "CONFLICT"


def test_attack003_missing_output_fails_closed():
    a = _decision("CASE-001", "BIND-001", "PASS")
    b = {
        "case_id": "CASE-001",
        "evidence_binding_id": "BIND-001",
        # missing decision_output
    }

    with pytest.raises(ValueError, match="INVALID_DECISION"):
        validate_decision_conflict_detection_v0_1(a, b)


def test_attack003_missing_binding_id_fails_closed():
    a = _decision("CASE-001", "BIND-001", "PASS")
    b = {
        "case_id": "CASE-001",
        # missing binding_id
        "decision_output": "FAIL",
    }

    with pytest.raises(ValueError, match="INVALID_DECISION"):
        validate_decision_conflict_detection_v0_1(a, b)


def test_attack003_different_case_no_conflict():
    a = _decision("CASE-001", "BIND-001", "PASS")
    b = _decision("CASE-002", "BIND-001", "FAIL")

    assert validate_decision_conflict_detection_v0_1(a, b) == "NO_CONFLICT"
