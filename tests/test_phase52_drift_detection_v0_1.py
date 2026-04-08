"""
GUS v7 — Phase 52
Drift Detection Tests (v0.1)

STRICT:
- Deterministic
- Fail-closed
- No inference
"""

import pytest

from gus_v7.drift_detection.drift_detection_v0_1 import (
    DRIFT_COMPARISON_FIELDS,
    REQUIRED_RECONSTRUCTION_KEYS,
    detect_drift_v0_1,
)


def _valid_reconstruction():
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
        "reconstructed_path": (
            "decision_id=DEC-001"
            "|case_id=BC-01"
            "|evidence_binding_id=EB-001"
            "|integrity_envelope_id=IE-001"
            "|final_integrity_verdict=INTEGRITY_CONFIRMED"
            "|execution_result=EXECUTE"
            "|trace_id=TRACE-001"
            "|trace_timestamp=2026-04-08T12:00:00Z"
            "|trace_sequence=0001"
        ),
    }


def test_phase52_required_reconstruction_keys_exact_match():
    assert REQUIRED_RECONSTRUCTION_KEYS == (
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


def test_phase52_comparison_fields_exact_match():
    assert DRIFT_COMPARISON_FIELDS == (
        "decision_id",
        "case_id",
        "evidence_binding_id",
        "integrity_envelope_id",
        "final_integrity_verdict",
        "execution_result",
        "reconstructed_path",
    )


def test_phase52_detects_no_drift_for_identical_reconstructions():
    baseline = _valid_reconstruction()
    candidate = _valid_reconstruction()
    assert detect_drift_v0_1(baseline, candidate) == "NO_DRIFT"


def test_phase52_detects_drift_when_comparison_field_changes():
    baseline = _valid_reconstruction()
    candidate = _valid_reconstruction()
    candidate["execution_result"] = "BLOCK"
    candidate["reconstructed_path"] = candidate["reconstructed_path"].replace(
        "execution_result=EXECUTE",
        "execution_result=BLOCK",
    )
    assert detect_drift_v0_1(baseline, candidate) == "DRIFT_DETECTED"


def test_phase52_ignores_non_comparison_field_changes():
    baseline = _valid_reconstruction()
    candidate = _valid_reconstruction()
    candidate["trace_id"] = "TRACE-999"
    candidate["trace_timestamp"] = "2026-04-09T12:00:00Z"
    candidate["trace_sequence"] = "0002"
    assert detect_drift_v0_1(baseline, candidate) == "NO_DRIFT"


def test_phase52_rejects_malformed_baseline():
    baseline = _valid_reconstruction()
    candidate = _valid_reconstruction()
    del baseline["reconstructed_path"]
    with pytest.raises(ValueError, match="INVALID_RECONSTRUCTION"):
        detect_drift_v0_1(baseline, candidate)


def test_phase52_rejects_malformed_candidate():
    baseline = _valid_reconstruction()
    candidate = _valid_reconstruction()
    candidate["decision_id"] = ""
    with pytest.raises(ValueError, match="INVALID_RECONSTRUCTION"):
        detect_drift_v0_1(baseline, candidate)
