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


def _supported_all():
    return ("PASS", "FAIL", "INSUFFICIENT_EVIDENCE", "OUT_OF_SCOPE")


def test_phase40_consistent_valid_bundle_returns_bound():
    bundle = (
        _evidence("E-001", "doc://evidence/1", "hash-001"),
        _evidence("E-002", "doc://evidence/2", "hash-002"),
    )
    assert validate_evidence_decision_binding_v0_1("PASS", bundle, _supported_all()) == "BOUND"


def test_phase40_empty_bundle_returns_rejected():
    assert validate_evidence_decision_binding_v0_1("PASS", tuple(), _supported_all()) == "REJECTED"


def test_phase40_inconsistent_bundle_returns_rejected():
    bundle = (
        _evidence("E-001", "doc://evidence/1", "hash-001", source_id="SRC-001"),
        _evidence("E-002", "doc://evidence/2", "hash-002", source_id="SRC-999"),
    )
    assert validate_evidence_decision_binding_v0_1("PASS", bundle, _supported_all()) == "REJECTED"


def test_phase40_invalid_evaluation_result_raises_value_error():
    bundle = (
        _evidence("E-001", "doc://evidence/1", "hash-001"),
        _evidence("E-002", "doc://evidence/2", "hash-002"),
    )
    with pytest.raises(ValueError):
        validate_evidence_decision_binding_v0_1("MAYBE", bundle, _supported_all())


def test_phase40_non_tuple_bundle_raises_value_error():
    bundle = []
    with pytest.raises(ValueError):
        validate_evidence_decision_binding_v0_1("PASS", bundle, _supported_all())  # type: ignore


def test_phase40_invalid_evidence_item_raises_value_error():
    invalid = _evidence("E-001", "doc://evidence/1", "")
    bundle = (
        invalid,
        _evidence("E-002", "doc://evidence/2", "hash-002"),
    )
    with pytest.raises(ValueError):
        validate_evidence_decision_binding_v0_1("PASS", bundle, _supported_all())
