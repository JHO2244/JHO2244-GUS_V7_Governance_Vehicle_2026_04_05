"""
GUS v7 - Phase 61
Global Identity Lifecycle Tests (v0.1)

STRICT:
- Deterministic
- Fail-first hardening tests
- No mutation
- No inference
- Fail-closed
"""

import pytest

from gus_v7.global_identity_lifecycle.global_identity_lifecycle_validator_v0_1 import (
    validate_global_identity_lifecycle_v0_1,
)


def _trace() -> dict:
    return {
        "trace_id": "TRACE-061-001",
        "decision_id": "DEC-061-001",
        "case_id": "BC-061-A",
        "evidence_binding_id": "EB-061-001",
        "integrity_envelope_id": "IE-061-001",
        "final_integrity_verdict": "INTEGRITY_CONFIRMED",
        "execution_result": "EXECUTE",
        "trace_timestamp": "2026-04-15T17:00:00Z",
        "trace_sequence": "0001",
    }


def test_phase61_accepts_unique_trace_against_empty_history():
    candidate = _trace()
    assert (
        validate_global_identity_lifecycle_v0_1(candidate, ())
        == "IDENTITY_LIFECYCLE_VALID"
    )


def test_phase61_rejects_reused_trace_id_across_history():
    existing = (_trace(),)
    candidate = dict(_trace())
    candidate["decision_id"] = "DEC-061-002"
    candidate["case_id"] = "BC-061-B"
    candidate["evidence_binding_id"] = "EB-061-002"
    candidate["integrity_envelope_id"] = "IE-061-002"

    assert (
        validate_global_identity_lifecycle_v0_1(candidate, existing)
        == "IDENTITY_LIFECYCLE_INVALID"
    )


def test_phase61_rejects_reused_decision_id_across_history():
    existing = (_trace(),)
    candidate = dict(_trace())
    candidate["trace_id"] = "TRACE-061-002"
    candidate["case_id"] = "BC-061-B"
    candidate["evidence_binding_id"] = "EB-061-002"
    candidate["integrity_envelope_id"] = "IE-061-002"

    assert (
        validate_global_identity_lifecycle_v0_1(candidate, existing)
        == "IDENTITY_LIFECYCLE_INVALID"
    )


def test_phase61_rejects_reused_evidence_binding_id_across_history():
    existing = (_trace(),)
    candidate = dict(_trace())
    candidate["trace_id"] = "TRACE-061-002"
    candidate["decision_id"] = "DEC-061-002"
    candidate["case_id"] = "BC-061-B"
    candidate["integrity_envelope_id"] = "IE-061-002"

    assert (
        validate_global_identity_lifecycle_v0_1(candidate, existing)
        == "IDENTITY_LIFECYCLE_INVALID"
    )


def test_phase61_rejects_reused_integrity_envelope_id_across_history():
    existing = (_trace(),)
    candidate = dict(_trace())
    candidate["trace_id"] = "TRACE-061-002"
    candidate["decision_id"] = "DEC-061-002"
    candidate["case_id"] = "BC-061-B"
    candidate["evidence_binding_id"] = "EB-061-002"

    assert (
        validate_global_identity_lifecycle_v0_1(candidate, existing)
        == "IDENTITY_LIFECYCLE_INVALID"
    )


def test_phase61_rejects_replay_of_same_identity_set_in_new_context():
    existing = (_trace(),)
    candidate = dict(_trace())
    candidate["case_id"] = "BC-061-REPLAY"
    candidate["trace_timestamp"] = "2026-04-15T17:05:00Z"
    candidate["trace_sequence"] = "0002"

    assert (
        validate_global_identity_lifecycle_v0_1(candidate, existing)
        == "IDENTITY_LIFECYCLE_INVALID"
    )


def test_phase61_rejects_malformed_candidate_fail_closed():
    candidate = _trace()
    del candidate["trace_id"]

    with pytest.raises(ValueError, match="INVALID_TRACE"):
        validate_global_identity_lifecycle_v0_1(candidate, ())


def test_phase61_rejects_malformed_history_fail_closed():
    malformed = _trace()
    del malformed["execution_result"]

    with pytest.raises(ValueError, match="INVALID_TRACE"):
        validate_global_identity_lifecycle_v0_1(_trace(), (malformed,))
        