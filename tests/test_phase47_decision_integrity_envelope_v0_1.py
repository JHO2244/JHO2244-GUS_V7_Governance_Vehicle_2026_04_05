"""
GUS v7 — Phase 47
Decision Integrity Envelope Tests (v0.1)

STRICT:
- Validate envelope aggregation only
- No inference
- Fail-closed enforcement
"""

from gus_v7.decision_integrity_envelope.decision_integrity_envelope_v0_1 import (
    build_decision_integrity_envelope_v0_1,
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


def test_phase47_builds_confirmed_integrity_envelope():
    envelope = build_decision_integrity_envelope_v0_1(
        _decision(),
        _evidence_binding(),
        _evidence_trace(),
    )
    assert envelope["integrity_result"] == "VALID"
    assert envelope["consistency_result"] == "CONSISTENT"
    assert envelope["trace_result"] == "LINKED"
    assert envelope["replay_result"] == "DETERMINISTIC"
    assert envelope["final_integrity_verdict"] == "INTEGRITY_CONFIRMED"
    assert envelope["immutable_after_creation"] is True


def test_phase47_rejects_envelope_when_integrity_fails():
    decision = _decision()
    decision["decision_output"] = "MAYBE"
    envelope = build_decision_integrity_envelope_v0_1(
        decision,
        _evidence_binding(),
        _evidence_trace(),
    )
    assert envelope["integrity_result"] == "INVALID"
    assert envelope["final_integrity_verdict"] == "INTEGRITY_REJECTED"


def test_phase47_rejects_envelope_when_consistency_fails():
    decision = _decision()
    decision["integrity_status"] = "pending"
    envelope = build_decision_integrity_envelope_v0_1(
        decision,
        _evidence_binding(),
        _evidence_trace(),
    )
    assert envelope["consistency_result"] == "INCONSISTENT"
    assert envelope["final_integrity_verdict"] == "INTEGRITY_REJECTED"


def test_phase47_rejects_envelope_when_trace_fails():
    trace = _evidence_trace()
    trace["chain_complete"] = False
    envelope = build_decision_integrity_envelope_v0_1(
        _decision(),
        _evidence_binding(),
        trace,
    )
    assert envelope["trace_result"] == "UNLINKED"
    assert envelope["final_integrity_verdict"] == "INTEGRITY_REJECTED"


def test_phase47_envelope_contains_original_decision_reference():
    decision = _decision()
    envelope = build_decision_integrity_envelope_v0_1(
        decision,
        _evidence_binding(),
        _evidence_trace(),
    )
    assert envelope["decision"] == decision
