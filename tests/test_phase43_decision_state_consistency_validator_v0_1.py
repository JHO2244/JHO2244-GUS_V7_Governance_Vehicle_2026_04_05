"""
GUS v7 — Phase 43
Decision State Consistency Validator Tests (v0.1)

STRICT:
- Validate internal decision state consistency only
- No inference
- Fail-closed enforcement
"""

from gus_v7.decision_state_consistency.decision_state_consistency_validator_v0_1 import (
    validate_decision_state_consistency_v0_1,
)


def _base_decision():
    return {
        "decision_id": "DEC-001",
        "case_id": "BC-01",
        "decision_output": "PASS",
        "decision_basis": "criteria_output_alignment",
        "evidence_binding_id": "EB-001",
        "timestamp": "2026-04-08T12:00:00Z",
        "integrity_status": "valid",
    }


def test_phase43_accepts_pass_with_valid_status():
    decision = _base_decision()
    decision["decision_output"] = "PASS"
    decision["integrity_status"] = "valid"
    assert validate_decision_state_consistency_v0_1(decision) == "CONSISTENT"


def test_phase43_accepts_fail_with_valid_status():
    decision = _base_decision()
    decision["decision_output"] = "FAIL"
    decision["integrity_status"] = "valid"
    assert validate_decision_state_consistency_v0_1(decision) == "CONSISTENT"


def test_phase43_accepts_insufficient_evidence_with_pending_status():
    decision = _base_decision()
    decision["decision_output"] = "INSUFFICIENT_EVIDENCE"
    decision["integrity_status"] = "pending"
    assert validate_decision_state_consistency_v0_1(decision) == "CONSISTENT"


def test_phase43_accepts_insufficient_evidence_with_valid_status():
    decision = _base_decision()
    decision["decision_output"] = "INSUFFICIENT_EVIDENCE"
    decision["integrity_status"] = "valid"
    assert validate_decision_state_consistency_v0_1(decision) == "CONSISTENT"


def test_phase43_rejects_pass_with_pending_status():
    decision = _base_decision()
    decision["decision_output"] = "PASS"
    decision["integrity_status"] = "pending"
    assert validate_decision_state_consistency_v0_1(decision) == "INCONSISTENT"


def test_phase43_rejects_fail_with_pending_status():
    decision = _base_decision()
    decision["decision_output"] = "FAIL"
    decision["integrity_status"] = "pending"
    assert validate_decision_state_consistency_v0_1(decision) == "INCONSISTENT"


def test_phase43_rejects_any_invalid_status_pairing():
    decision = _base_decision()
    decision["decision_output"] = "FAIL"
    decision["integrity_status"] = "invalid"
    assert validate_decision_state_consistency_v0_1(decision) == "INCONSISTENT"


def test_phase43_rejects_unknown_output():
    decision = _base_decision()
    decision["decision_output"] = "MAYBE"
    assert validate_decision_state_consistency_v0_1(decision) == "INCONSISTENT"


def test_phase43_rejects_unknown_status():
    decision = _base_decision()
    decision["integrity_status"] = "unknown"
    assert validate_decision_state_consistency_v0_1(decision) == "INCONSISTENT"
