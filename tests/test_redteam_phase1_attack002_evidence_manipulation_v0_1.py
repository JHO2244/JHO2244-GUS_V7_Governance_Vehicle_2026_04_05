import pytest

from gus_v7.evidence_consistency.evidence_consistency_validator_v0_1 import (
    validate_evidence_consistency_v0_1,
)


def _evidence(
    evidence_id: str,
    timestamp: str,
    content_ref: str = "doc://benchmark/evidence/001",
    content_hash: str = "abc123hash",
    evidence_type: str = "document",
    source_id: str = "SRC-001",
    validation_status: str = "verified",
):
    return {
        "evidence_id": evidence_id,
        "evidence_type": evidence_type,
        "source_id": source_id,
        "timestamp": timestamp,
        "content_ref": content_ref,
        "content_hash": content_hash,
        "validation_status": validation_status,
    }


def test_attack002_duplicate_content_with_different_identity_is_treated_consistent():
    bundle = (
        _evidence("E-001", "2026-04-07T16:45:00Z"),
        _evidence("E-999", "2026-04-07T18:45:00Z"),
    )

    assert validate_evidence_consistency_v0_1(bundle) == "consistent"


def test_attack002_partial_evidence_member_raises_invalid_evidence():
    partial = {
        "evidence_id": "E-001",
        "evidence_type": "document",
        "source_id": "SRC-001",
        "timestamp": "2026-04-07T16:45:00Z",
        "content_ref": "doc://benchmark/evidence/001",
        "content_hash": "",
        "validation_status": "verified",
    }

    bundle = (
        partial,
        _evidence("E-002", "2026-04-07T16:50:00Z"),
    )

    with pytest.raises(ValueError, match="INVALID_EVIDENCE"):
        validate_evidence_consistency_v0_1(bundle)


def test_attack002_conflicting_validation_status_returns_inconsistent():
    bundle = (
        _evidence("E-001", "2026-04-07T16:45:00Z", validation_status="verified"),
        _evidence("E-002", "2026-04-07T16:50:00Z", validation_status="unverified"),
    )

    assert validate_evidence_consistency_v0_1(bundle) == "inconsistent"
