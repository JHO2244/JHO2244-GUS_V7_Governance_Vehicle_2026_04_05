"""
GUS v7 — Phase 46
Decision Conflict Detection Validator Tests (v0.1)

STRICT:
- Validate contradiction detection only
- No inference
- Fail-closed enforcement
"""

import pytest

from gus_v7.decision_conflict_detection.decision_conflict_detection_validator_v0_1 import (
    validate_decision_conflict_detection_v0_1,
)


def _decision_a():
    return {
        "decision_id": "DEC-001",
        "case_id": "BC-01",
        "decision_output": "PASS",
        "decision_basis": "criteria_output_alignment",
        "evidence_binding_id": "EB-001",
        "timestamp": "2026-04-08T12:00:00Z",
        "integrity_status": "valid",
    }


def _decision_b():
    return {
        "decision_id": "DEC-002",
        "case_id": "BC-01",
        "decision_output": "FAIL",
        "decision_basis": "criteria_output_alignment",
        "evidence_binding_id": "EB-001",
        "timestamp": "2026-04-08T12:05:00Z",
        "integrity_status": "valid",
    }


def test_phase46_detects_conflict_for_same_case_and_binding_with_different_outputs():
    assert (
        validate_decision_conflict_detection_v0_1(
            _decision_a(),
            _decision_b(),
        )
        == "CONFLICT"
    )


def test_phase46_accepts_same_output_as_no_conflict():
    decision_b = _decision_b()
    decision_b["decision_output"] = "PASS"
    assert (
        validate_decision_conflict_detection_v0_1(
            _decision_a(),
            decision_b,
        )
        == "NO_CONFLICT"
    )


def test_phase46_accepts_different_binding_as_no_conflict():
    decision_b = _decision_b()
    decision_b["evidence_binding_id"] = "EB-999"
    assert (
        validate_decision_conflict_detection_v0_1(
            _decision_a(),
            decision_b,
        )
        == "NO_CONFLICT"
    )


def test_phase46_accepts_different_case_as_no_conflict():
    decision_b = _decision_b()
    decision_b["case_id"] = "BC-99"
    assert (
        validate_decision_conflict_detection_v0_1(
            _decision_a(),
            decision_b,
        )
        == "NO_CONFLICT"
    )


def test_phase46_missing_case_ids_fail_closed():
    decision_a = _decision_a()
    decision_b = _decision_b()
    decision_a["case_id"] = ""

    with pytest.raises(ValueError, match="INVALID_DECISION"):
        validate_decision_conflict_detection_v0_1(
            decision_a,
            decision_b,
        )


def test_phase46_missing_binding_ids_fail_closed():
    decision_a = _decision_a()
    decision_b = _decision_b()
    decision_b["evidence_binding_id"] = ""

    with pytest.raises(ValueError, match="INVALID_DECISION"):
        validate_decision_conflict_detection_v0_1(
            decision_a,
            decision_b,
        )


def test_phase46_missing_outputs_fail_closed():
    decision_a = _decision_a()
    decision_b = _decision_b()
    decision_b["decision_output"] = ""

    with pytest.raises(ValueError, match="INVALID_DECISION"):
        validate_decision_conflict_detection_v0_1(
            decision_a,
            decision_b,
        )
