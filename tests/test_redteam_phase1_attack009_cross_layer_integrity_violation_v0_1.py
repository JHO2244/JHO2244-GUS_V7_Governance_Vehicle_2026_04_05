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


def test_attack009_fake_trace_still_confirms_integrity_envelope():
    fake_trace = {
        "binding_id": "EB-001",
        "chain_complete": True,
    }

    envelope = build_decision_integrity_envelope_v0_1(
        _decision(),
        _evidence_binding(),
        fake_trace,
    )

    assert envelope["integrity_result"] == "VALID"
    assert envelope["consistency_result"] == "CONSISTENT"
    assert envelope["trace_result"] == "LINKED"
    assert envelope["replay_result"] == "DETERMINISTIC"
    assert envelope["final_integrity_verdict"] == "INTEGRITY_CONFIRMED"


def test_attack009_empty_trace_paths_still_confirm_integrity_envelope():
    fake_trace = {
        "binding_id": "EB-001",
        "requirement_to_criteria": (),
        "criteria_to_evaluations": (),
        "evaluations_to_decision": (),
        "chain_complete": True,
    }

    envelope = build_decision_integrity_envelope_v0_1(
        _decision(),
        _evidence_binding(),
        fake_trace,
    )

    assert envelope["trace_result"] == "LINKED"
    assert envelope["replay_result"] == "DETERMINISTIC"
    assert envelope["final_integrity_verdict"] == "INTEGRITY_CONFIRMED"


def test_attack009_nonsensical_trace_content_still_confirms_integrity_envelope():
    fake_trace = {
        "binding_id": "EB-001",
        "requirement_to_criteria": ("NOT", "A", "REAL", "CHAIN"),
        "criteria_to_evaluations": ("BROKEN",),
        "evaluations_to_decision": ("FAKE", "LINK"),
        "chain_complete": True,
    }

    envelope = build_decision_integrity_envelope_v0_1(
        _decision(),
        _evidence_binding(),
        fake_trace,
    )

    assert envelope["trace_result"] == "LINKED"
    assert envelope["replay_result"] == "DETERMINISTIC"
    assert envelope["final_integrity_verdict"] == "INTEGRITY_CONFIRMED"
