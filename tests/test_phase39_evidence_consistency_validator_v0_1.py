"""
GUS v7 — Phase 39
Evidence Consistency Validator Tests (v0.1)

STRICT:
- Deterministic
- Fail-closed
- No inference
"""

import pytest

from gus_v7.evidence_consistency.evidence_consistency_validator_v0_1 import (
    CONSISTENCY_LOCK_FIELDS,
    validate_evidence_consistency_v0_1,
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
        "timestamp": "2026-04-07T18:00:00Z",
        "content_ref": content_ref,
        "content_hash": content_hash,
        "validation_status": validation_status,
    }


def test_phase39_consistency_lock_fields_locked():
    assert CONSISTENCY_LOCK_FIELDS == (
        "evidence_type",
        "source_id",
        "validation_status",
    )


def test_phase39_matching_bundle_returns_consistent():
    bundle = (
        _evidence("E-001", "doc://evidence/1", "hash-001"),
        _evidence("E-002", "doc://evidence/2", "hash-002"),
    )
    assert validate_evidence_consistency_v0_1(bundle) == "consistent"


def test_phase39_bundle_with_duplicate_fingerprint_returns_inconsistent():
    bundle = (
        _evidence("E-001", "doc://evidence/1", "hash-001"),
        _evidence("E-001", "doc://evidence/1", "hash-001"),
    )
    assert validate_evidence_consistency_v0_1(bundle) == "inconsistent"


def test_phase39_bundle_with_mismatched_type_returns_inconsistent():
    bundle = (
        _evidence("E-001", "doc://evidence/1", "hash-001", evidence_type="document"),
        _evidence("E-002", "doc://evidence/2", "hash-002", evidence_type="record"),
    )
    assert validate_evidence_consistency_v0_1(bundle) == "inconsistent"


def test_phase39_bundle_with_mismatched_source_returns_inconsistent():
    bundle = (
        _evidence("E-001", "doc://evidence/1", "hash-001", source_id="SRC-001"),
        _evidence("E-002", "doc://evidence/2", "hash-002", source_id="SRC-999"),
    )
    assert validate_evidence_consistency_v0_1(bundle) == "inconsistent"


def test_phase39_bundle_with_mismatched_validation_status_returns_inconsistent():
    bundle = (
        _evidence("E-001", "doc://evidence/1", "hash-001", validation_status="verified"),
        _evidence("E-002", "doc://evidence/2", "hash-002", validation_status="unverified"),
    )
    assert validate_evidence_consistency_v0_1(bundle) == "inconsistent"


def test_phase39_non_tuple_bundle_raises_value_error():
    bundle = [
        _evidence("E-001", "doc://evidence/1", "hash-001"),
        _evidence("E-002", "doc://evidence/2", "hash-002"),
    ]
    with pytest.raises(ValueError, match="INVALID_EVIDENCE_BUNDLE"):
        validate_evidence_consistency_v0_1(bundle)  # type: ignore[arg-type]


def test_phase39_bundle_with_less_than_two_items_raises_value_error():
    bundle = (_evidence("E-001", "doc://evidence/1", "hash-001"),)
    with pytest.raises(ValueError, match="INVALID_EVIDENCE_BUNDLE"):
        validate_evidence_consistency_v0_1(bundle)


def test_phase39_invalid_evidence_item_raises_value_error():
    invalid = _evidence("E-001", "doc://evidence/1", "")
    bundle = (
        invalid,
        _evidence("E-002", "doc://evidence/2", "hash-002"),
    )
    with pytest.raises(ValueError, match="INVALID_EVIDENCE"):
        validate_evidence_consistency_v0_1(bundle)
        