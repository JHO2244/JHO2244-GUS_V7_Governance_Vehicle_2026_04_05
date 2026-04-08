"""
GUS v7 — Phase 50
Trace Integrity Lock (v0.1)

STRICT:
- Deterministic
- Fail-closed
- No inference
- No mutation
- No external calls
"""

import hashlib

from gus_v7.decision_execution_trace.decision_execution_trace_logger_v0_1 import (
    log_decision_execution_trace_v0_1,
)


TRACE_FINGERPRINT_FIELD_ORDER = (
    "trace_id",
    "decision_id",
    "case_id",
    "evidence_binding_id",
    "integrity_envelope_id",
    "final_integrity_verdict",
    "execution_result",
    "trace_timestamp",
    "trace_sequence",
)


def lock_trace_integrity_v0_1(trace: dict) -> str:
    """
    Returns a deterministic SHA-256 fingerprint for a valid execution trace.

    Fail-closed behavior:
    - invalid trace -> ValueError
    """
    if log_decision_execution_trace_v0_1(trace) != "VALID":
        raise ValueError("INVALID_TRACE")

    canonical_parts = []
    for field in TRACE_FINGERPRINT_FIELD_ORDER:
        canonical_parts.append(f"{field}={trace[field]}")

    canonical_payload = "|".join(canonical_parts)
    return hashlib.sha256(canonical_payload.encode("utf-8")).hexdigest()
