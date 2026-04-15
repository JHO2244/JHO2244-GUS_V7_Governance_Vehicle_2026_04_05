"""
GUS v7 — Phase 1 Hardening Validator (v0.1)

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


UNIQUE_ID_FIELDS = (
    "trace_id",
    "decision_id",
    "evidence_binding_id",
    "integrity_envelope_id",
)


def _execution_matches_verdict(trace: dict) -> bool:
    verdict = trace["final_integrity_verdict"]
    execution = trace["execution_result"]

    if verdict == "INTEGRITY_CONFIRMED" and execution == "EXECUTE":
        return True

    if verdict == "INTEGRITY_REJECTED" and execution == "BLOCK":
        return True

    return False


def validate_phase1_hardening_v0_1(
    candidate_trace: dict,
    existing_traces: tuple[dict, ...],
) -> str:
    """
    Returns:
        "HARDENING_VALID" or "HARDENING_INVALID"

    Fail-closed behavior:
    - malformed candidate or existing trace -> ValueError("INVALID_TRACE")
    """

    if log_decision_execution_trace_v0_1(candidate_trace) != "VALID":
        raise ValueError("INVALID_TRACE")

    for trace in existing_traces:
        if log_decision_execution_trace_v0_1(trace) != "VALID":
            raise ValueError("INVALID_TRACE")

    if not _execution_matches_verdict(candidate_trace):
        return "HARDENING_INVALID"

    for trace in existing_traces:
        for field in UNIQUE_ID_FIELDS:
            if candidate_trace[field] == trace[field]:
                return "HARDENING_INVALID"

    return "HARDENING_VALID"
