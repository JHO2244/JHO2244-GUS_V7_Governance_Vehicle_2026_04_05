"""
GUS v7 — Phase 51
Audit Reconstruction Tests (v0.1)

STRICT:
- Deterministic
- Fail-closed
- No inference
"""

import pytest

from gus_v7.audit_reconstruction.audit_reconstruction_v0_1 import (
    reconstruct_audit_path_v0_1,
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


def test_phase51_reconstruction_returns_expected_keys():
    result = reconstruct_audit_path_v0_1(_valid_trace())
    assert tuple(result.keys()) == (
        "trace_id",
        "decision_id",
        "case_id",
        "evidence_binding_id",
        "integrity_envelope_id",
        "final_integrity_verdict",
        "execution_result",
        "trace_timestamp",
        "trace_sequence",
        "reconstructed_path",
    )


def test_phase51_reconstruction_is_deterministic():
    trace = _valid_trace()
    assert reconstruct_audit_path_v0_1(trace) == reconstruct_audit_path_v0_1(trace)


def test_phase51_reconstruction_path_contains_all_core_links():
    result = reconstruct_audit_path_v0_1(_valid_trace())
    assert result["reconstructed_path"] == (
        "decision_id=DEC-001"
        "|case_id=BC-01"
        "|evidence_binding_id=EB-001"
        "|integrity_envelope_id=IE-001"
        "|final_integrity_verdict=INTEGRITY_CONFIRMED"
        "|execution_result=EXECUTE"
        "|trace_id=TRACE-001"
        "|trace_timestamp=2026-04-08T12:00:00Z"
        "|trace_sequence=0001"
    )


def test_phase51_reconstruction_reflects_input_values_exactly():
    trace = _valid_trace()
    trace["execution_result"] = "BLOCK"
    result = reconstruct_audit_path_v0_1(trace)
    assert result["execution_result"] == "BLOCK"
    assert "|execution_result=BLOCK" in result["reconstructed_path"]


def test_phase51_reconstruction_rejects_invalid_trace():
    trace = _valid_trace()
    trace["execution_result"] = "ALLOW"
    with pytest.raises(ValueError, match="INVALID_TRACE"):
        reconstruct_audit_path_v0_1(trace)
