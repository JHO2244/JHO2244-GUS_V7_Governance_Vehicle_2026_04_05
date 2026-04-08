"""
GUS v7 — Phase 41
Decision Integrity Validator Tests (v0.1)

STRICT:
- Validate deterministic decision admissibility
- No inference
- Fail-closed enforcement
"""

from gus_v7.decision_integrity.decision_integrity_validator_v0_1 import (
    validate_decision_integrity_v0_1,
)


def _valid_decision():
    return {
        "decision_id": "DEC-001",
        "case_id": "BC-01",
        "decision_output": "PASS",
        "decision_basis": "criteria_output_alignment",
        "evidence_binding_id": "EB-001",
        "timestamp": "2026-04-08T12:00:00Z",
        "integrity_status": "valid",
    }


def test_phase41_validator_accepts_valid_decision():
    assert validate_decision_integrity_v0_1(_valid_decision()) == "VALID"


def test_phase41_validator_rejects_missing_field():
    decision = _valid_decision()
    del decision["decision_basis"]
    assert validate_decision_integrity_v0_1(decision) == "INVALID"


def test_phase41_validator_rejects_empty_required_field():
    decision = _valid_decision()
    decision["decision_id"] = ""
    assert validate_decision_integrity_v0_1(decision) == "INVALID"


def test_phase41_validator_rejects_invalid_output():
    decision = _valid_decision()
    decision["decision_output"] = "MAYBE"
    assert validate_decision_integrity_v0_1(decision) == "INVALID"


def test_phase41_validator_rejects_invalid_integrity_status():
    decision = _valid_decision()
    decision["integrity_status"] = "unknown"
    assert validate_decision_integrity_v0_1(decision) == "INVALID"


def test_phase41_validator_rejects_extra_field():
    decision = _valid_decision()
    decision["extra"] = "not allowed"
    assert validate_decision_integrity_v0_1(decision) == "INVALID"
