"""
GUS v7 — Phase 38
Evidence Consistency Schema Tests (v0.1)

STRICT:
- Validate structure only
- No inference
- Fail-closed enforcement
"""

from gus_v7.evidence_consistency.evidence_consistency_schema_v0_1 import (
    EVIDENCE_CONSISTENCY_KEYS,
    EVIDENCE_FINGERPRINTS_TYPE_REQUIRED,
    EVIDENCE_FINGERPRINTS_MIN_ITEMS,
    EVIDENCE_FINGERPRINTS_ORDER_REQUIRED,
    EVIDENCE_FINGERPRINTS_UNIQUE_REQUIRED,
    VALID_CONSISTENCY_RESULTS,
    CONSISTENCY_INTEGRITY_KEYS,
    VALID_CONSISTENCY_STATUS_VALUES,
    CONSISTENCY_MODE_REQUIRED,
    REQUIRED_NON_EMPTY_FIELDS,
    NO_EXTRA_FIELDS_ALLOWED,
    IMMUTABLE_AFTER_CREATION,
    VALIDATION_RULES,
    FAIL_CLOSED_BEHAVIOR,
)


def test_phase38_consistency_keys_exact_match():
    expected = (
        "evaluation_id",
        "evidence_fingerprints",
        "consistency_result",
        "consistency_integrity",
    )
    assert EVIDENCE_CONSISTENCY_KEYS == expected


def test_phase38_required_fields_match_top_level_keys():
    assert REQUIRED_NON_EMPTY_FIELDS == EVIDENCE_CONSISTENCY_KEYS


def test_phase38_fingerprints_type_required():
    assert EVIDENCE_FINGERPRINTS_TYPE_REQUIRED == "tuple"


def test_phase38_fingerprints_min_items():
    assert EVIDENCE_FINGERPRINTS_MIN_ITEMS == 2


def test_phase38_fingerprints_order_required():
    assert EVIDENCE_FINGERPRINTS_ORDER_REQUIRED is True


def test_phase38_fingerprints_unique_required():
    assert EVIDENCE_FINGERPRINTS_UNIQUE_REQUIRED is True


def test_phase38_valid_consistency_results():
    assert VALID_CONSISTENCY_RESULTS == ("consistent", "inconsistent")


def test_phase38_consistency_integrity_keys_exact_match():
    expected = (
        "consistency_status",
        "checked_pairs",
        "conflicts_detected",
        "consistency_mode",
    )
    assert CONSISTENCY_INTEGRITY_KEYS == expected


def test_phase38_valid_consistency_status_values():
    assert VALID_CONSISTENCY_STATUS_VALUES == ("unverified", "verified")


def test_phase38_consistency_mode_required():
    assert CONSISTENCY_MODE_REQUIRED == "deterministic_structural_consistency"


def test_phase38_no_extra_fields_lock():
    assert NO_EXTRA_FIELDS_ALLOWED is True


def test_phase38_immutability_lock():
    assert IMMUTABLE_AFTER_CREATION is True


def test_phase38_validation_rules_defined():
    assert VALIDATION_RULES == (
        "C1_STRUCTURE_LOCK",
        "C2_REQUIRED_FIELDS_LOCK",
        "C3_MIN_EVIDENCE_LOCK",
        "C4_FINGERPRINT_ORDER_LOCK",
        "C5_FINGERPRINT_UNIQUENESS_LOCK",
        "C6_CONSISTENCY_RESULT_LOCK",
        "C7_INTEGRITY_LOCK",
        "C8_NO_EXTRA_FIELDS_LOCK",
        "C9_IMMUTABILITY_LOCK",
    )


def test_phase38_fail_closed_behavior():
    assert FAIL_CLOSED_BEHAVIOR == "ANY_VIOLATION_RESULTS_IN_REJECTION"
