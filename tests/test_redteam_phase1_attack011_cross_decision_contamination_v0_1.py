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


def test_attack011_same_binding_reused_across_different_cases_is_not_flagged():
    decision_a = _decision_a()
    decision_b = {
        "decision_id": "DEC-002",
        "case_id": "BC-99",
        "decision_output": "FAIL",
        "decision_basis": "different_case_reuse",
        "evidence_binding_id": "EB-001",
        "timestamp": "2026-04-08T12:05:00Z",
        "integrity_status": "valid",
    }

    assert (
        validate_decision_conflict_detection_v0_1(decision_a, decision_b)
        == "NO_CONFLICT"
    )


def test_attack011_same_binding_reused_across_different_cases_same_output_is_not_flagged():
    decision_a = _decision_a()
    decision_b = {
        "decision_id": "DEC-003",
        "case_id": "BC-77",
        "decision_output": "PASS",
        "decision_basis": "same_output_binding_reuse",
        "evidence_binding_id": "EB-001",
        "timestamp": "2026-04-08T12:06:00Z",
        "integrity_status": "valid",
    }

    assert (
        validate_decision_conflict_detection_v0_1(decision_a, decision_b)
        == "NO_CONFLICT"
    )


def test_attack011_same_case_different_binding_same_output_is_not_flagged():
    decision_a = _decision_a()
    decision_b = {
        "decision_id": "DEC-004",
        "case_id": "BC-01",
        "decision_output": "PASS",
        "decision_basis": "binding_swapped_same_case",
        "evidence_binding_id": "EB-999",
        "timestamp": "2026-04-08T12:07:00Z",
        "integrity_status": "valid",
    }

    assert (
        validate_decision_conflict_detection_v0_1(decision_a, decision_b)
        == "NO_CONFLICT"
    )

