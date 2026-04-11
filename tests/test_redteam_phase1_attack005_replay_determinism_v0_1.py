from copy import deepcopy

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


def test_attack005_replay_is_deterministic_for_same_objects():
    decision = _decision()
    evidence_binding = _evidence_binding()
    evidence_trace = _evidence_trace()

    assert (
        validate_decision_replay_determinism_v0_1(
            decision,
            evidence_binding,
            evidence_trace,
        )
        == "DETERMINISTIC"
    )


def test_attack005_replay_does_not_mutate_inputs():
    decision = _decision()
    evidence_binding = _evidence_binding()
    evidence_trace = _evidence_trace()

    original_decision = deepcopy(decision)
    original_binding = deepcopy(evidence_binding)
    original_trace = deepcopy(evidence_trace)

    validate_decision_replay_determinism_v0_1(
        decision,
        evidence_binding,
        evidence_trace,
    )

    assert decision == original_decision
    assert evidence_binding == original_binding
    assert evidence_trace == original_trace


def test_attack005_invalid_but_repeatable_replay_is_still_deterministic():
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

