"""
GUS v7 — Phase 50
Trace Integrity Lock Tests (v0.1)

STRICT:
- Deterministic
- Fail-closed
- No inference
"""

import pytest

from gus_v7.trace_integrity_lock.trace_integrity_lock_v0_1 import (
    TRACE_FINGERPRINT_FIELD_ORDER,
    lock_trace_integrity_v0_1,
)


def _valid_trace():
    return {
        "trace_id": "TRACE-001",
        "decision_id": "DEC-001",
        "case_id": "BC-01",
        "evidence_binding_id": "EB-001",
        "integrity_envelope_id": "IE-001",
        "final_integrity_verdict": "INTEGRITY_CONFIRMED",
        "execution_result": "EXECUTE",
        "trace_timestamp": "2026-04-08T12:00:00Z",
        "trace_sequence": "0001",
    }


def test_phase50_field_order_exact_match():
    assert TRACE_FINGERPRINT_FIELD_ORDER == (
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


def test_phase50_lock_returns_sha256_hex():
    fingerprint = lock_trace_integrity_v0_1(_valid_trace())
    assert isinstance(fingerprint, str)
    assert len(fingerprint) == 64
    assert all(ch in "0123456789abcdef" for ch in fingerprint)


def test_phase50_lock_is_deterministic():
    trace = _valid_trace()
    assert lock_trace_integrity_v0_1(trace) == lock_trace_integrity_v0_1(trace)


def test_phase50_lock_changes_when_trace_changes():
    trace_a = _valid_trace()
    trace_b = _valid_trace()
    trace_b["trace_sequence"] = "0002"
    assert lock_trace_integrity_v0_1(trace_a) != lock_trace_integrity_v0_1(trace_b)


def test_phase50_lock_rejects_invalid_trace():
    trace = _valid_trace()
    trace["execution_result"] = "ALLOW"
    with pytest.raises(ValueError, match="INVALID_TRACE"):
        lock_trace_integrity_v0_1(trace)
        