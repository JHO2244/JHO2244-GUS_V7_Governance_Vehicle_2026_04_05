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


def test_attack007_accepts_trace_with_only_binding_id_and_chain_complete():
    fake_trace = {
        "binding_id": "EB-001",
        "chain_complete": True,
    }

    assert (
        validate_decision_trace_linking_v0_1(
            _decision(),
            _evidence_binding(),
            fake_trace,
        )
        == "LINKED"
    )


def test_attack007_accepts_trace_missing_all_path_segments():
    fake_trace = {
        "binding_id": "EB-001",
        "requirement_to_criteria": (),
        "criteria_to_evaluations": (),
        "evaluations_to_decision": (),
        "chain_complete": True,
    }

    assert (
        validate_decision_trace_linking_v0_1(
            _decision(),
            _evidence_binding(),
            fake_trace,
        )
        == "LINKED"
    )


def test_attack007_accepts_trace_with_nonsensical_path_content():
    fake_trace = {
        "binding_id": "EB-001",
        "requirement_to_criteria": ("NOT", "A", "REAL", "CHAIN"),
        "criteria_to_evaluations": ("BROKEN",),
        "evaluations_to_decision": ("FAKE", "LINK"),
        "chain_complete": True,
    }

    assert (
        validate_decision_trace_linking_v0_1(
            _decision(),
            _evidence_binding(),
            fake_trace,
        )
        == "LINKED"
    )


def test_attack007_accepts_trace_with_unrelated_extra_fields():
    fake_trace = {
        "binding_id": "EB-001",
        "chain_complete": True,
        "forged_trace_id": "TRACE-FAKE-001",
        "forged_case_id": "BC-999",
        "forged_note": "partial trace presented as complete",
    }

    assert (
        validate_decision_trace_linking_v0_1(
            _decision(),
            _evidence_binding(),
            fake_trace,
        )
        == "LINKED"
    )
