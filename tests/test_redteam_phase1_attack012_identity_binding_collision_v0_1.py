from gus_v7.decision_integrity_envelope.decision_integrity_envelope_v0_1 import (
    build_decision_integrity_envelope_v0_1,
)
from gus_v7.decision_execution_trace.decision_execution_trace_logger_v0_1 import (
    log_decision_execution_trace_v0_1,
)
from gus_v7.trace_integrity_lock.trace_integrity_lock_v0_1 import (
    lock_trace_integrity_v0_1,
)


def _decision(decision_id: str, case_id: str) -> dict:
    return {
        "decision_id": decision_id,
        "case_id": case_id,
        "decision_output": "PASS",
        "decision_basis": "criteria_output_alignment",
        "evidence_binding_id": "EB-COLLIDE-001",
        "timestamp": "2026-04-13T12:00:00Z",
        "integrity_status": "valid",
    }


def _evidence_binding(decision_id: str, evidence_ids: tuple[str, ...]) -> dict:
    return {
        "binding_id": "EB-COLLIDE-001",
        "decision_id": decision_id,
        "evidence_ids": evidence_ids,
    }


def _evidence_trace() -> dict:
    return {
        "binding_id": "EB-COLLIDE-001",
        "requirement_to_criteria": ("REQ-001", "C1", "C2", "C3"),
        "criteria_to_evaluations": ("C1:V1", "C2:V1", "C3:V1"),
        "evaluations_to_decision": ("V1", "DEC-COLLIDE"),
        "chain_complete": True,
    }


def _trace(
    trace_id: str,
    decision_id: str,
    case_id: str,
    integrity_envelope_id: str,
    trace_sequence: str,
) -> dict:
    return {
        "trace_id": trace_id,
        "decision_id": decision_id,
        "case_id": case_id,
        "evidence_binding_id": "EB-COLLIDE-001",
        "integrity_envelope_id": integrity_envelope_id,
        "final_integrity_verdict": "INTEGRITY_CONFIRMED",
        "execution_result": "EXECUTE",
        "trace_timestamp": "2026-04-13T12:00:00Z",
        "trace_sequence": trace_sequence,
    }


def test_attack012_accepts_distinct_decisions_reusing_same_evidence_binding_id():
    envelope_a = build_decision_integrity_envelope_v0_1(
        _decision("DEC-012-A", "CASE-012-A"),
        _evidence_binding("DEC-012-A", ("EV-001",)),
        _evidence_trace(),
    )
    envelope_b = build_decision_integrity_envelope_v0_1(
        _decision("DEC-012-B", "CASE-012-B"),
        _evidence_binding("DEC-012-B", ("EV-999",)),
        _evidence_trace(),
    )

    assert envelope_a["final_integrity_verdict"] == "INTEGRITY_CONFIRMED"
    assert envelope_b["final_integrity_verdict"] == "INTEGRITY_CONFIRMED"


def test_attack012_accepts_distinct_traces_reusing_same_integrity_envelope_id():
    trace_a = _trace(
        trace_id="TRACE-012-A",
        decision_id="DEC-012-A",
        case_id="CASE-012-A",
        integrity_envelope_id="IE-COLLIDE-001",
        trace_sequence="0001",
    )
    trace_b = _trace(
        trace_id="TRACE-012-B",
        decision_id="DEC-012-B",
        case_id="CASE-012-B",
        integrity_envelope_id="IE-COLLIDE-001",
        trace_sequence="0002",
    )

    assert log_decision_execution_trace_v0_1(trace_a) == "VALID"
    assert log_decision_execution_trace_v0_1(trace_b) == "VALID"


def test_attack012_fingerprints_change_but_collision_ids_are_still_admitted():
    trace_a = _trace(
        trace_id="TRACE-012-A",
        decision_id="DEC-012-A",
        case_id="CASE-012-A",
        integrity_envelope_id="IE-COLLIDE-001",
        trace_sequence="0001",
    )
    trace_b = _trace(
        trace_id="TRACE-012-B",
        decision_id="DEC-012-B",
        case_id="CASE-012-B",
        integrity_envelope_id="IE-COLLIDE-001",
        trace_sequence="0002",
    )

    fingerprint_a = lock_trace_integrity_v0_1(trace_a)
    fingerprint_b = lock_trace_integrity_v0_1(trace_b)

    assert fingerprint_a != fingerprint_b
