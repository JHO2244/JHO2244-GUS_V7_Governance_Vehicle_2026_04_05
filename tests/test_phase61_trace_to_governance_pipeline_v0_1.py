"""
GUS v7 - Phase 61
Trace to Governance Pipeline (v0.1)

STRICT:
- Deterministic
- Fail-first pipeline integration tests
- No mutation
- No inference
- Fail-closed
"""

import pytest

from gus_v7.trace_to_governance_pipeline.trace_to_governance_pipeline_v0_1 import (
    apply_trace_to_governance_pipeline_v0_1,
)


def _trace() -> dict:
    return {
        "trace_id": "TRACE-061-P-001",
        "decision_id": "DEC-061-P-001",
        "case_id": "BC-061-P-A",
        "evidence_binding_id": "EB-061-P-001",
        "integrity_envelope_id": "IE-061-P-001",
        "final_integrity_verdict": "INTEGRITY_CONFIRMED",
        "execution_result": "EXECUTE",
        "trace_timestamp": "2026-04-17T18:30:00Z",
        "trace_sequence": "0001",
    }


def test_phase61_pipeline_passes_valid_unique_trace():
    result = apply_trace_to_governance_pipeline_v0_1(_trace(), ())
    assert result == "GOVERNANCE_PASS"


def test_phase61_pipeline_fails_replayed_identity_trace():
    existing = (_trace(),)
    candidate = dict(_trace())
    candidate["case_id"] = "BC-061-P-REPLAY"
    candidate["trace_timestamp"] = "2026-04-17T18:35:00Z"
    candidate["trace_sequence"] = "0002"

    result = apply_trace_to_governance_pipeline_v0_1(candidate, existing)
    assert result == "GOVERNANCE_FAIL"


def test_phase61_pipeline_fails_rejected_block_trace():
    candidate = dict(_trace())
    candidate["final_integrity_verdict"] = "INTEGRITY_REJECTED"
    candidate["execution_result"] = "BLOCK"

    result = apply_trace_to_governance_pipeline_v0_1(candidate, ())
    assert result == "GOVERNANCE_PASS"


def test_phase61_pipeline_rejects_malformed_history_fail_closed():
    malformed = _trace()
    del malformed["execution_result"]

    with pytest.raises(ValueError, match="INVALID_TRACE"):
        apply_trace_to_governance_pipeline_v0_1(_trace(), (malformed,))
