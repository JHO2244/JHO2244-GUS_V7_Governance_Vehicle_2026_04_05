"""
GUS v7 — Phase 51
Audit Reconstruction (v0.1)

STRICT:
- Deterministic
- Fail-closed
- No inference
- No mutation
- No external calls
"""

from gus_v7.decision_execution_trace.decision_execution_trace_logger_v0_1 import (
    log_decision_execution_trace_v0_1,
)


def reconstruct_audit_path_v0_1(trace: dict) -> dict:
    """
    Returns a deterministic reconstruction object for a valid execution trace.

    Fail-closed behavior:
    - invalid trace -> ValueError
    """
    if log_decision_execution_trace_v0_1(trace) != "VALID":
        raise ValueError("INVALID_TRACE")

    reconstructed_path = (
        f"decision_id={trace['decision_id']}"
        f"|case_id={trace['case_id']}"
        f"|evidence_binding_id={trace['evidence_binding_id']}"
        f"|integrity_envelope_id={trace['integrity_envelope_id']}"
        f"|final_integrity_verdict={trace['final_integrity_verdict']}"
        f"|execution_result={trace['execution_result']}"
        f"|trace_id={trace['trace_id']}"
        f"|trace_timestamp={trace['trace_timestamp']}"
        f"|trace_sequence={trace['trace_sequence']}"
    )

    return {
        "trace_id": trace["trace_id"],
        "decision_id": trace["decision_id"],
        "case_id": trace["case_id"],
        "evidence_binding_id": trace["evidence_binding_id"],
        "integrity_envelope_id": trace["integrity_envelope_id"],
        "final_integrity_verdict": trace["final_integrity_verdict"],
        "execution_result": trace["execution_result"],
        "trace_timestamp": trace["trace_timestamp"],
        "trace_sequence": trace["trace_sequence"],
        "reconstructed_path": reconstructed_path,
    }
