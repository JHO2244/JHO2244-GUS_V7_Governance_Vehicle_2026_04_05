from gus_v7.decision_execution_gate.decision_execution_gate_v0_1 import (
    apply_decision_execution_gate_v0_1,
)
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


def test_attack010_replays_previously_confirmed_envelope_after_decision_changes():
    decision = _decision()
    envelope = build_decision_integrity_envelope_v0_1(
        decision,
        _evidence_binding(),
        _evidence_trace(),
    )

    decision["decision_output"] = "MAYBE"
    decision["integrity_status"] = "invalid"

    assert envelope["final_integrity_verdict"] == "INTEGRITY_CONFIRMED"
    assert apply_decision_execution_gate_v0_1(envelope) == "EXECUTE"


def test_attack010_replays_confirmed_envelope_after_trace_changes():
    decision = _decision()
    trace = _evidence_trace()

    envelope = build_decision_integrity_envelope_v0_1(
        decision,
        _evidence_binding(),
        trace,
    )

    trace["chain_complete"] = False
    trace["binding_id"] = "EB-999"

    assert envelope["final_integrity_verdict"] == "INTEGRITY_CONFIRMED"
    assert apply_decision_execution_gate_v0_1(envelope) == "EXECUTE"


def test_attack010_rebinding_confirmed_envelope_to_unrelated_context_still_executes():
    original_envelope = build_decision_integrity_envelope_v0_1(
        _decision(),
        _evidence_binding(),
        _evidence_trace(),
    )

    rebound_envelope = {
        **original_envelope,
        "decision": {
            "decision_id": "DEC-999",
            "case_id": "BC-99",
            "decision_output": "FAIL",
            "decision_basis": "unrelated_context",
            "evidence_binding_id": "EB-999",
            "timestamp": "2099-01-01T00:00:00Z",
            "integrity_status": "invalid",
        },
    }

    assert rebound_envelope["final_integrity_verdict"] == "INTEGRITY_CONFIRMED"
    assert apply_decision_execution_gate_v0_1(rebound_envelope) == "EXECUTE"
