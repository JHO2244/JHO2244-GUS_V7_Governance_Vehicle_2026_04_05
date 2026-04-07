"""
GUS v7 — Phase 35
Evidence Validator Tests (v0.1)

STRICT:
- Deterministic
- Fail-closed
- No inference
"""

from gus_v7.evidence.evidence_validator_v0_1 import validate_evidence_v0_1


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


def test_phase35_valid_evidence_returns_valid():
    assert validate_evidence_v0_1(_valid_evidence()) == "VALID"


def test_phase35_missing_field_returns_invalid():
    evidence = _valid_evidence()
    del evidence["source_id"]
    assert validate_evidence_v0_1(evidence) == "INVALID"


def test_phase35_empty_required_field_returns_invalid():
    evidence = _valid_evidence()
    evidence["content_ref"] = ""
    assert validate_evidence_v0_1(evidence) == "INVALID"


def test_phase35_invalid_evidence_type_returns_invalid():
    evidence = _valid_evidence()
    evidence["evidence_type"] = "rumor"
    assert validate_evidence_v0_1(evidence) == "INVALID"


def test_phase35_invalid_validation_status_returns_invalid():
    evidence = _valid_evidence()
    evidence["validation_status"] = "pending"
    assert validate_evidence_v0_1(evidence) == "INVALID"


def test_phase35_missing_hash_returns_invalid():
    evidence = _valid_evidence()
    evidence["content_hash"] = ""
    assert validate_evidence_v0_1(evidence) == "INVALID"


def test_phase35_extra_field_returns_invalid():
    evidence = _valid_evidence()
    evidence["extra_field"] = "not allowed"
    assert validate_evidence_v0_1(evidence) == "INVALID"
