"""
GUS v7 — Phase 49
Decision Execution Trace Logger (v0.1)

STRICT:
- Deterministic
- Fail-closed
- No inference
- No mutation
- No external calls
"""

from gus_v7.decision_execution_trace.decision_execution_trace_schema_v0_1 import (
    DECISION_EXECUTION_TRACE_KEYS,
    VALID_EXECUTION_RESULTS,
    VALID_FINAL_INTEGRITY_VERDICTS,
    REQUIRED_NON_EMPTY_FIELDS,
    NO_EXTRA_FIELDS_ALLOWED,
)


def _execution_matches_verdict(trace: dict) -> bool:
    verdict = trace["final_integrity_verdict"]
    execution = trace["execution_result"]

    if verdict == "INTEGRITY_CONFIRMED" and execution == "EXECUTE":
        return True

    if verdict == "INTEGRITY_REJECTED" and execution == "BLOCK":
        return True

    return False


def log_decision_execution_trace_v0_1(trace: dict) -> str:
    """
    Returns:
        "VALID" or "INVALID"
    """

    # -------------------------
    # STRUCTURE CHECK
    # -------------------------
    if NO_EXTRA_FIELDS_ALLOWED:
        if set(trace.keys()) != set(DECISION_EXECUTION_TRACE_KEYS):
            return "INVALID"

    # -------------------------
    # REQUIRED FIELDS CHECK
    # -------------------------
    for field in REQUIRED_NON_EMPTY_FIELDS:
        if field not in trace:
            return "INVALID"
        if trace[field] in (None, "", []):
            return "INVALID"

    # -------------------------
    # EXECUTION RESULT CHECK
    # -------------------------
    if trace["execution_result"] not in VALID_EXECUTION_RESULTS:
        return "INVALID"

    # -------------------------
    # FINAL INTEGRITY VERDICT CHECK
    # -------------------------
    if (
        trace["final_integrity_verdict"]
        not in VALID_FINAL_INTEGRITY_VERDICTS
    ):
        return "INVALID"

    # -------------------------
    # EXECUTION / VERDICT BINDING
    # -------------------------
    if not _execution_matches_verdict(trace):
        return "INVALID"

    return "VALID"
