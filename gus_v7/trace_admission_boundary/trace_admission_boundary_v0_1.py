"""
GUS v7 - Phase 61
Trace Admission Boundary (v0.1)

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
from gus_v7.global_identity_lifecycle.global_identity_lifecycle_validator_v0_1 import (
    validate_global_identity_lifecycle_v0_1,
)


def admit_trace_with_identity_lifecycle_v0_1(
    candidate_trace: dict,
    admitted_history: tuple[dict, ...],
) -> str:
    """
    Returns:
        "TRACE_ADMITTED" or "TRACE_REJECTED"

    Fail-closed behavior:
    - malformed candidate or history -> ValueError("INVALID_TRACE")
    """

    if log_decision_execution_trace_v0_1(candidate_trace) != "VALID":
        raise ValueError("INVALID_TRACE")

    for trace in admitted_history:
        if log_decision_execution_trace_v0_1(trace) != "VALID":
            raise ValueError("INVALID_TRACE")

    lifecycle_result = validate_global_identity_lifecycle_v0_1(
        candidate_trace,
        admitted_history,
    )

    if lifecycle_result == "IDENTITY_LIFECYCLE_INVALID":
        return "TRACE_REJECTED"

    return "TRACE_ADMITTED"

