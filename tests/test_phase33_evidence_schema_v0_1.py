"""
GUS v7 — Phase 33
Evidence Schema Contract Tests (v0.1)

STRICT:
- Validate structure only
- No inference
- Fail-closed enforcement
"""

import pytest

from gus_v7.evidence.evidence_schema_v0_1 import (
    EVIDENCE_KEYS,
    VALID_EVIDENCE_TYPES,
    VALIDATION_STATUS_VALUES,
    REQUIRED_NON_EMPTY_FIELDS,
    HASH_REQUIRED,
    NO_EXTRA_FIELDS_ALLOWED,
    IMMUTABLE_AFTER_CREATION,
    VALIDATION_RULES,
    FAIL_CLOSED_BEHAVIOR,
)


# =========================
# TEST: STRUCTURE LOCK
# =========================

def test_phase33_evidence_keys_exact_match():
    expected = (
        "evidence_id",
        "evidence_type",
        "source_id",
        "timestamp",
        "content_ref",
        "content_hash",
        "validation_status",
    )
    assert EVIDENCE_KEYS == expected


# =========================
# TEST: REQUIRED FIELDS
# =========================

def test_phase33_required_fields_match_keys():
    assert set(REQUIRED_NON_EMPTY_FIELDS) == set(EVIDENCE_KEYS)


# =========================
# TEST: VALID TYPES
# =========================

def test_phase33_valid_evidence_types_defined():
    assert "document" in VALID_EVIDENCE_TYPES
    assert "record" in VALID_EVIDENCE_TYPES
    assert "log" in VALID_EVIDENCE_TYPES
    assert "measurement" in VALID_EVIDENCE_TYPES
    assert "external_reference" in VALID_EVIDENCE_TYPES


# =========================
# TEST: VALIDATION STATUS
# =========================

def test_phase33_validation_status_values():
    assert VALIDATION_STATUS_VALUES == ("unverified", "verified")


# =========================
# TEST: HASH REQUIREMENT
# =========================

def test_phase33_hash_required():
    assert HASH_REQUIRED is True


# =========================
# TEST: NO EXTRA FIELDS LOCK
# =========================

def test_phase33_no_extra_fields_lock():
    assert NO_EXTRA_FIELDS_ALLOWED is True


# =========================
# TEST: IMMUTABILITY LOCK
# =========================

def test_phase33_immutability_lock():
    assert IMMUTABLE_AFTER_CREATION is True


# =========================
# TEST: VALIDATION RULE IDS
# =========================

def test_phase33_validation_rules_defined():
    assert "E1_STRUCTURE_LOCK" in VALIDATION_RULES
    assert "E6_IMMUTABILITY_LOCK" in VALIDATION_RULES


# =========================
# TEST: FAIL-CLOSED
# =========================

def test_phase33_fail_closed_behavior():
    assert FAIL_CLOSED_BEHAVIOR == "ANY_VIOLATION_RESULTS_IN_REJECTION"
