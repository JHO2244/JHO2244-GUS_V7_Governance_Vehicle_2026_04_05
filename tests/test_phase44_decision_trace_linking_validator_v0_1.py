"""
GUS v7 — Phase 44
Decision Trace Linking Validator Tests (v0.1)

STRICT:
- Validate link integrity only
- No inference
- Fail-closed enforcement
"""

from gus_v7.decision_trace_linking.decision_trace_linking_validator_v0_1 import (
    validate_decision_trace_linking_v0_1,
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


def test_phase44_accepts_valid_trace_link():
    assert (
        validate_decision_trace_linking_v0_1(
            _decision(),
            _evidence_binding(),
            _evidence_trace(),
        )
        == "LINKED"
    )


def test_phase44_rejects_missing_decision_binding_id():
    decision = _decision()
    decision["evidence_binding_id"] = ""
    assert (
        validate_decision_trace_linking_v0_1(
            decision,
            _evidence_binding(),
            _evidence_trace(),
        )
        == "UNLINKED"
    )


def test_phase44_rejects_missing_binding_id():
    binding = _evidence_binding()
    binding["binding_id"] = ""
    assert (
        validate_decision_trace_linking_v0_1(
            _decision(),
            binding,
            _evidence_trace(),
        )
        == "UNLINKED"
    )


def test_phase44_rejects_missing_trace_binding_id():
    trace = _evidence_trace()
    trace["binding_id"] = ""
    assert (
        validate_decision_trace_linking_v0_1(
            _decision(),
            _evidence_binding(),
            trace,
        )
        == "UNLINKED"
    )


def test_phase44_rejects_decision_binding_mismatch():
    decision = _decision()
    decision["evidence_binding_id"] = "EB-999"
    assert (
        validate_decision_trace_linking_v0_1(
            decision,
            _evidence_binding(),
            _evidence_trace(),
        )
        == "UNLINKED"
    )


def test_phase44_rejects_trace_binding_mismatch():
    trace = _evidence_trace()
    trace["binding_id"] = "EB-999"
    assert (
        validate_decision_trace_linking_v0_1(
            _decision(),
            _evidence_binding(),
            trace,
        )
        == "UNLINKED"
    )


def test_phase44_rejects_incomplete_trace_chain():
    trace = _evidence_trace()
    trace["chain_complete"] = False
    assert (
        validate_decision_trace_linking_v0_1(
            _decision(),
            _evidence_binding(),
            trace,
        )
        == "UNLINKED"
    )
