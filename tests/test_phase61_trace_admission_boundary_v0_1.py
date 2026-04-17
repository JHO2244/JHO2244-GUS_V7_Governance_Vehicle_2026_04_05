"""
GUS v7 - Phase 61
Trace Admission Boundary (v0.1)

STRICT:
- Deterministic
- Fail-first boundary enforcement tests
- No mutation
- No inference
- Fail-closed
"""

import pytest

from gus_v7.trace_admission_boundary.trace_admission_boundary_v0_1 import (
    admit_trace_with_identity_lifecycle_v0_1,
)


def _trace() -> dict:
    return {
        "trace_id": "TRACE-061-B-001",
        "decision_id": "DEC-061-B-001",
        "case_id": "BC-061-B-A",
        "evidence_binding_id": "EB-061-B-001",
        "integrity_envelope_id": "IE-061-B-001",
        "final_integrity_verdict": "INTEGRITY_CONFIRMED",
        "execution_result": "EXECUTE",
        "trace_timestamp": "2026-04-17T14:00:00Z",
        "trace_sequence": "0001",
    }


def test_phase61_boundary_accepts_valid_unique_trace():
    candidate = _trace()
    assert (
        admit_trace_with_identity_lifecycle_v0_1(candidate, ())
        == "TRACE_ADMITTED"
    )


def test_phase61_boundary_rejects_reused_identity_trace():
    existing = (_trace(),)
    candidate = dict(_trace())
    candidate["case_id"] = "BC-061-B-REPLAY"
    candidate["trace_timestamp"] = "2026-04-17T14:05:00Z"
    candidate["trace_sequence"] = "0002"

    assert (
        admit_trace_with_identity_lifecycle_v0_1(candidate, existing)
        == "TRACE_REJECTED"
    )


def test_phase61_boundary_rejects_verdict_execution_mismatch():
    candidate = _trace()
    candidate["execution_result"] = "BLOCK"

    with pytest.raises(ValueError, match="INVALID_TRACE"):
        admit_trace_with_identity_lifecycle_v0_1(candidate, ())


def test_phase61_boundary_rejects_malformed_history_fail_closed():
    malformed = _trace()
    del malformed["execution_result"]

    with pytest.raises(ValueError, match="INVALID_TRACE"):
        admit_trace_with_identity_lifecycle_v0_1(_trace(), (malformed,))
