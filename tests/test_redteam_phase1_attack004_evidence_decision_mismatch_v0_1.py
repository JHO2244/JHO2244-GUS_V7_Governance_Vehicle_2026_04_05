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


def _consistent_bundle():
    return (
        _evidence("E-001", "doc://evidence/1", "hash-001"),
        _evidence("E-002", "doc://evidence/2", "hash-002"),
    )


def test_attack004_same_evidence_binds_to_pass():
    assert validate_evidence_decision_binding_v0_1(
        "PASS",
        _consistent_bundle(),
    ) == "BOUND"


def test_attack004_same_evidence_binds_to_fail():
    assert validate_evidence_decision_binding_v0_1(
        "FAIL",
        _consistent_bundle(),
    ) == "BOUND"


def test_attack004_same_evidence_binds_to_out_of_scope():
    assert validate_evidence_decision_binding_v0_1(
        "OUT_OF_SCOPE",
        _consistent_bundle(),
    ) == "BOUND"


def test_attack004_invalid_evidence_member_still_fails_closed():
    invalid_bundle = (
        _evidence("E-001", "doc://evidence/1", ""),
        _evidence("E-002", "doc://evidence/2", "hash-002"),
    )

    with pytest.raises(ValueError, match="INVALID_EVIDENCE"):
        validate_evidence_decision_binding_v0_1("PASS", invalid_bundle)
