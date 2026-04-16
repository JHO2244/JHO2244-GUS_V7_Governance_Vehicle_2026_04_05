"""
GUS v7 - Phase 62
Provenance Chain Lock Tests (v0.1)

STRICT:
- Deterministic
- Fail-first hardening tests
- No mutation
- No inference
- Fail-closed
"""

import pytest

from gus_v7.provenance_chain_lock.provenance_chain_lock_validator_v0_1 import (
    validate_provenance_chain_lock_v0_1,
)


def _valid_reconstruction() -> dict:
    return {
        "trace_id": "TRACE-062-001",
        "decision_id": "DEC-062-001",
        "case_id": "BC-062-A",
        "evidence_binding_id": "EB-062-001",
        "integrity_envelope_id": "IE-062-001",
        "final_integrity_verdict": "INTEGRITY_CONFIRMED",
        "execution_result": "EXECUTE",
        "trace_timestamp": "2026-04-16T16:30:00Z",
        "trace_sequence": "0001",
        "reconstructed_path": (
            "decision_id=DEC-062-001"
            "|case_id=BC-062-A"
            "|evidence_binding_id=EB-062-001"
            "|integrity_envelope_id=IE-062-001"
            "|final_integrity_verdict=INTEGRITY_CONFIRMED"
            "|execution_result=EXECUTE"
            "|trace_id=TRACE-062-001"
            "|trace_timestamp=2026-04-16T16:30:00Z"
            "|trace_sequence=0001"
        ),
    }


def test_phase62_accepts_valid_provenance_chain():
    assert (
        validate_provenance_chain_lock_v0_1(_valid_reconstruction())
        == "PROVENANCE_CHAIN_VALID"
    )


def test_phase62_rejects_corrupted_reconstructed_path():
    reconstruction = _valid_reconstruction()
    reconstruction["reconstructed_path"] = (
        "decision_id=DEC-FAKE"
        "|case_id=BC-FAKE"
        "|evidence_binding_id=EB-FAKE"
        "|integrity_envelope_id=IE-FAKE"
        "|final_integrity_verdict=INTEGRITY_REJECTED"
        "|execution_result=BLOCK"
        "|trace_id=TRACE-FAKE"
        "|trace_timestamp=1999-01-01T00:00:00Z"
        "|trace_sequence=9999"
    )

    assert (
        validate_provenance_chain_lock_v0_1(reconstruction)
        == "PROVENANCE_CHAIN_INVALID"
    )


def test_phase62_rejects_partial_path_mismatch():
    reconstruction = _valid_reconstruction()
    reconstruction["reconstructed_path"] = reconstruction[
        "reconstructed_path"
    ].replace("case_id=BC-062-A", "case_id=BC-062-B")

    assert (
        validate_provenance_chain_lock_v0_1(reconstruction)
        == "PROVENANCE_CHAIN_INVALID"
    )


def test_phase62_rejects_malformed_reconstruction_fail_closed():
    reconstruction = _valid_reconstruction()
    del reconstruction["execution_result"]

    with pytest.raises(ValueError, match="INVALID_RECONSTRUCTION"):
        validate_provenance_chain_lock_v0_1(reconstruction)
