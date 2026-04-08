"""
GUS v7 — Phase 53
Governance Rules Engine Tests (v0.1)

STRICT:
- Deterministic
- Fail-closed
- No inference
"""

import pytest

from gus_v7.governance_rules.governance_rules_engine_v0_1 import (
    REQUIRED_RECONSTRUCTION_KEYS,
    VALID_EXECUTION_RESULTS,
    apply_governance_rules_v0_1,
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


def test_phase53_required_reconstruction_keys_exact_match():
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


def test_phase53_valid_execution_results_exact_match():
    assert VALID_EXECUTION_RESULTS == ("EXECUTE", "BLOCK")


def test_phase53_passes_confirmed_execute():
    reconstruction = _valid_reconstruction()
    assert apply_governance_rules_v0_1(reconstruction) == "GOVERNANCE_PASS"


def test_phase53_fails_confirmed_block():
    reconstruction = _valid_reconstruction()
    reconstruction["execution_result"] = "BLOCK"
    assert apply_governance_rules_v0_1(reconstruction) == "GOVERNANCE_FAIL"


def test_phase53_passes_unconfirmed_block():
    reconstruction = _valid_reconstruction()
    reconstruction["final_integrity_verdict"] = "INTEGRITY_REJECTED"
    reconstruction["execution_result"] = "BLOCK"
    assert apply_governance_rules_v0_1(reconstruction) == "GOVERNANCE_PASS"


def test_phase53_fails_unconfirmed_execute():
    reconstruction = _valid_reconstruction()
    reconstruction["final_integrity_verdict"] = "INTEGRITY_REJECTED"
    reconstruction["execution_result"] = "EXECUTE"
    assert apply_governance_rules_v0_1(reconstruction) == "GOVERNANCE_FAIL"


def test_phase53_rejects_malformed_reconstruction():
    reconstruction = _valid_reconstruction()
    del reconstruction["reconstructed_path"]
    with pytest.raises(ValueError, match="INVALID_RECONSTRUCTION"):
        apply_governance_rules_v0_1(reconstruction)


def test_phase53_rejects_invalid_execution_result():
    reconstruction = _valid_reconstruction()
    reconstruction["execution_result"] = "ALLOW"
    with pytest.raises(ValueError, match="INVALID_RECONSTRUCTION"):
        apply_governance_rules_v0_1(reconstruction)
