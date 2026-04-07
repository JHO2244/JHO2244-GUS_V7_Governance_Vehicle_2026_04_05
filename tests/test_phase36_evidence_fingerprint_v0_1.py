"""
GUS v7 — Phase 36
Evidence Fingerprinting Tests (v0.1)

STRICT:
- Deterministic
- Fail-closed
- No inference
"""

import pytest

from gus_v7.evidence.evidence_fingerprint_v0_1 import (
    FINGERPRINT_FIELD_ORDER,
    fingerprint_evidence_v0_1,
)


def _valid_evidence():
    return {
        "evidence_id": "E-001",
        "evidence_type": "document",
        "source_id": "SRC-001",
        "timestamp": "2026-04-07T16:45:00Z",
        "content_ref": "doc://benchmark/evidence/001",
        "content_hash": "abc123hash",
        "validation_status": "verified",
    }


def test_phase36_fingerprint_field_order_locked():
    assert FINGERPRINT_FIELD_ORDER == (
        "evidence_id",
        "evidence_type",
        "source_id",
        "timestamp",
        "content_ref",
        "content_hash",
        "validation_status",
    )


def test_phase36_same_input_same_fingerprint():
    evidence = _valid_evidence()
    first = fingerprint_evidence_v0_1(evidence)
    second = fingerprint_evidence_v0_1(evidence)
    assert first == second


def test_phase36_fingerprint_is_sha256_hex():
    fingerprint = fingerprint_evidence_v0_1(_valid_evidence())
    assert len(fingerprint) == 64
    int(fingerprint, 16)


def test_phase36_changed_field_changes_fingerprint():
    evidence_a = _valid_evidence()
    evidence_b = _valid_evidence()
    evidence_b["content_hash"] = "differenthash"
    assert fingerprint_evidence_v0_1(evidence_a) != fingerprint_evidence_v0_1(evidence_b)


def test_phase36_invalid_evidence_raises_value_error():
    evidence = _valid_evidence()
    evidence["evidence_type"] = "rumor"
    with pytest.raises(ValueError, match="INVALID_EVIDENCE"):
        fingerprint_evidence_v0_1(evidence)
