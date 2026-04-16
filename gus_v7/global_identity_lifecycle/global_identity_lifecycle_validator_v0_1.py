"""
GUS v7 - Phase 61
Global Identity Lifecycle Validator (v0.1)

STRICT:
- Deterministic
- Fail-closed
- No mutation
- No inference
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


def validate_global_identity_lifecycle_v0_1(
    candidate_trace: dict,
    admitted_history: tuple[dict, ...],
) -> str:
    """
    Returns:
        "IDENTITY_LIFECYCLE_VALID" or "IDENTITY_LIFECYCLE_INVALID"

    Fail-closed behavior:
    - malformed candidate or admitted history -> ValueError("INVALID_TRACE")
    """

    if log_decision_execution_trace_v0_1(candidate_trace) != "VALID":
        raise ValueError("INVALID_TRACE")

    for trace in admitted_history:
        if log_decision_execution_trace_v0_1(trace) != "VALID":
            raise ValueError("INVALID_TRACE")

    for trace in admitted_history:
        for field in UNIQUE_ID_FIELDS:
            if candidate_trace[field] == trace[field]:
                return "IDENTITY_LIFECYCLE_INVALID"

    return "IDENTITY_LIFECYCLE_VALID"
