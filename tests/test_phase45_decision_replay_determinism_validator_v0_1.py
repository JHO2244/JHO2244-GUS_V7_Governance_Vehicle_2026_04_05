"""
GUS v7 — Phase 45
Decision Replay Determinism Validator Tests (v0.1)

STRICT:
- Validate replay determinism only
- No inference
- Fail-closed enforcement
"""

from gus_v7.decision_replay_determinism.decision_replay_determinism_validator_v0_1 import (
    validate_decision_replay_determinism_v0_1,
)


def _decision():
    return {
        "decision_id": "DEC-001",
        "case_id": "BC-01",
        "decision_output": "PASS",
        "decision_basis": "criteria_output_alignment",
        "evidence_binding_id": "EB-001",
        "timestamp": "2026-04-08T12:00:00Z",
        "integrity_status": "valid",
    }


def _evidence_binding():
    return {
        "binding_id": "EB-001",
        "decision_id": "DEC-001",
        "evidence_ids": ("EV-001", "EV-002"),
    }


def _evidence_trace():
    return {
        "binding_id": "EB-001",
        "requirement_to_criteria": ("REQ-001", "C1", "C2", "C3"),
        "criteria_to_evaluations": ("C1:V1", "C2:V1", "C3:V1"),
        "evaluations_to_decision": ("V1", "DEC-001"),
        "chain_complete": True,
    }


def test_phase45_accepts_deterministic_replay():
    assert (
        validate_decision_replay_determinism_v0_1(
            _decision(),
            _evidence_binding(),
            _evidence_trace(),
        )
        == "DETERMINISTIC"
    )


def test_phase45_accepts_repeatable_invalid_decision_as_deterministic():
    decision = _decision()
    decision["decision_output"] = "MAYBE"
    assert (
        validate_decision_replay_determinism_v0_1(
            decision,
            _evidence_binding(),
            _evidence_trace(),
        )
        == "DETERMINISTIC"
    )


def test_phase45_accepts_repeatable_unlinked_decision_as_deterministic():
    trace = _evidence_trace()
    trace["chain_complete"] = False
    assert (
        validate_decision_replay_determinism_v0_1(
            _decision(),
            _evidence_binding(),
            trace,
        )
        == "DETERMINISTIC"
    )
