"""
GUS v7 - Phase 1 Hardening
Identity Uniqueness + Validation/Execution Binding Tests (v0.1)

STRICT:
- Fail-first hardening tests
- Deterministic
- Fail-closed
- No inference
- No mutation
"""

import pytest

from gus_v7.phase1_hardening.phase1_hardening_validator_v0_1 import (
    validate_phase1_hardening_v0_1,
)


def _valid_trace() -> dict:
    return {
        "trace_id": "TRACE-001",
        "decision_id": "DEC-001",
        "case_id": "BC-01",
        "evidence_binding_id": "EB-001",
        "integrity_envelope_id": "IE-001",
        "final_integrity_verdict": "INTEGRITY_CONFIRMED",
        "execution_result": "EXECUTE",
        "trace_timestamp": "2026-04-15T12:00:00Z",
        "trace_sequence": "0001",
    }


def test_phase1_hardening_accepts_valid_unique_trace_with_bound_execution():
    candidate = _valid_trace()
    existing_traces = ()
    assert (
        validate_phase1_hardening_v0_1(candidate, existing_traces)
        == "HARDENING_VALID"
    )


def test_phase1_hardening_rejects_trace_id_collision():
    existing = (_valid_trace(),)
    candidate = _valid_trace()
    candidate["decision_id"] = "DEC-002"
    candidate["case_id"] = "BC-02"
    candidate["evidence_binding_id"] = "EB-002"
    candidate["integrity_envelope_id"] = "IE-002"

    assert (
        validate_phase1_hardening_v0_1(candidate, existing)
        == "HARDENING_INVALID"
    )


def test_phase1_hardening_rejects_decision_id_collision():
    existing = (_valid_trace(),)
    candidate = _valid_trace()
    candidate["trace_id"] = "TRACE-002"
    candidate["case_id"] = "BC-02"
    candidate["evidence_binding_id"] = "EB-002"
    candidate["integrity_envelope_id"] = "IE-002"

    assert (
        validate_phase1_hardening_v0_1(candidate, existing)
        == "HARDENING_INVALID"
    )


def test_phase1_hardening_rejects_evidence_binding_id_collision():
    existing = (_valid_trace(),)
    candidate = _valid_trace()
    candidate["trace_id"] = "TRACE-002"
    candidate["decision_id"] = "DEC-002"
    candidate["case_id"] = "BC-02"
    candidate["integrity_envelope_id"] = "IE-002"

    assert (
        validate_phase1_hardening_v0_1(candidate, existing)
        == "HARDENING_INVALID"
    )


def test_phase1_hardening_rejects_integrity_envelope_id_collision():
    existing = (_valid_trace(),)
    candidate = _valid_trace()
    candidate["trace_id"] = "TRACE-002"
    candidate["decision_id"] = "DEC-002"
    candidate["case_id"] = "BC-02"
    candidate["evidence_binding_id"] = "EB-002"

    assert (
        validate_phase1_hardening_v0_1(candidate, existing)
        == "HARDENING_INVALID"
    )


def test_phase1_hardening_rejects_execute_when_integrity_rejected():
    candidate = _valid_trace()
    candidate["final_integrity_verdict"] = "INTEGRITY_REJECTED"
    candidate["execution_result"] = "EXECUTE"

    with pytest.raises(ValueError, match="INVALID_TRACE"):
        validate_phase1_hardening_v0_1(candidate, ())


def test_phase1_hardening_rejects_block_when_integrity_confirmed():
    candidate = _valid_trace()
    candidate["execution_result"] = "BLOCK"

    with pytest.raises(ValueError, match="INVALID_TRACE"):
        validate_phase1_hardening_v0_1(candidate, ())


def test_phase1_hardening_rejects_malformed_candidate_fail_closed():
    candidate = _valid_trace()
    del candidate["trace_id"]

    with pytest.raises(ValueError, match="INVALID_TRACE"):
        validate_phase1_hardening_v0_1(candidate, ())


def test_phase1_hardening_rejects_malformed_existing_trace_fail_closed():
    existing = (_valid_trace(),)
    malformed = dict(existing[0])
    del malformed["execution_result"]

    with pytest.raises(ValueError, match="INVALID_TRACE"):
        validate_phase1_hardening_v0_1(_valid_trace(), (malformed,))
