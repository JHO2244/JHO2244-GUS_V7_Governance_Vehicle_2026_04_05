import pytest

from gus_v7.evidence_binding.evidence_decision_binding_validator_v0_1 import (
    validate_evidence_decision_binding_v0_1,
)


def _evidence(
    evidence_id: str,
    content_ref: str,
    content_hash: str,
    evidence_type: str = "document",
    source_id: str = "SRC-001",
    validation_status: str = "verified",
):
    return {
        "evidence_id": evidence_id,
        "evidence_type": evidence_type,
        "source_id": source_id,
        "timestamp": "2026-04-07T18:30:00Z",
        "content_ref": content_ref,
        "content_hash": content_hash,
        "validation_status": validation_status,
    }


def _bundle():
    return (
        _evidence("E-001", "doc://evidence/1", "hash-001"),
        _evidence("E-002", "doc://evidence/2", "hash-002"),
    )


def test_attack004_rejects_unsupported_outcome():
    supported = ("PASS",)

    assert validate_evidence_decision_binding_v0_1(
        "FAIL",
        _bundle(),
        supported,
    ) == "REJECTED"


def test_attack004_accepts_supported_outcome():
    supported = ("PASS",)

    assert validate_evidence_decision_binding_v0_1(
        "PASS",
        _bundle(),
        supported,
    ) == "BOUND"


def test_attack004_invalid_supported_results_fails_closed():
    with pytest.raises(ValueError):
        validate_evidence_decision_binding_v0_1(
            "PASS",
            _bundle(),
            (),
        )
