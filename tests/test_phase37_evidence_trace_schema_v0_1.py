"""
GUS v7 — Phase 37
Evidence Trace Linking Schema Tests (v0.1)

STRICT:
- Validate structure only
- No inference
- Fail-closed enforcement
"""

from gus_v7.evidence_trace.evidence_trace_schema_v0_1 import (
    EVIDENCE_TRACE_KEYS,
    EVIDENCE_FINGERPRINTS_TYPE_REQUIRED,
    EVIDENCE_FINGERPRINTS_MIN_ITEMS,
    EVIDENCE_FINGERPRINTS_ORDER_REQUIRED,
    EVIDENCE_FINGERPRINTS_UNIQUE_REQUIRED,
    EVIDENCE_FINGERPRINT_FORMAT_REQUIRED,
    TRACE_INTEGRITY_KEYS,
    VALID_TRACE_STATUS_VALUES,
    LINK_MODE_REQUIRED,
    REQUIRED_NON_EMPTY_FIELDS,
    NO_EXTRA_FIELDS_ALLOWED,
    IMMUTABLE_AFTER_CREATION,
    VALIDATION_RULES,
    FAIL_CLOSED_BEHAVIOR,
)


def test_phase37_trace_keys_exact_match():
    expected = (
        "evaluation_id",
        "evidence_fingerprints",
        "trace_integrity",
    )
    assert EVIDENCE_TRACE_KEYS == expected


def test_phase37_required_fields_match_top_level_keys():
    assert REQUIRED_NON_EMPTY_FIELDS == EVIDENCE_TRACE_KEYS


def test_phase37_fingerprints_type_required():
    assert EVIDENCE_FINGERPRINTS_TYPE_REQUIRED == "tuple"


def test_phase37_fingerprints_min_items():
    assert EVIDENCE_FINGERPRINTS_MIN_ITEMS == 1


def test_phase37_fingerprints_order_required():
    assert EVIDENCE_FINGERPRINTS_ORDER_REQUIRED is True


def test_phase37_fingerprints_unique_required():
    assert EVIDENCE_FINGERPRINTS_UNIQUE_REQUIRED is True


def test_phase37_fingerprint_format_required():
    assert EVIDENCE_FINGERPRINT_FORMAT_REQUIRED == "sha256_hex"


def test_phase37_trace_integrity_keys_exact_match():
    expected = (
        "trace_status",
        "fingerprint_count",
        "all_links_present",
        "link_mode",
    )
    assert TRACE_INTEGRITY_KEYS == expected


def test_phase37_valid_trace_status_values():
    assert VALID_TRACE_STATUS_VALUES == ("unverified", "verified")


def test_phase37_link_mode_required():
    assert LINK_MODE_REQUIRED == "deterministic_trace_link"


def test_phase37_no_extra_fields_lock():
    assert NO_EXTRA_FIELDS_ALLOWED is True


def test_phase37_immutability_lock():
    assert IMMUTABLE_AFTER_CREATION is True


def test_phase37_validation_rules_defined():
    assert VALIDATION_RULES == (
        "T1_STRUCTURE_LOCK",
        "T2_REQUIRED_FIELDS_LOCK",
        "T3_FINGERPRINT_PRESENCE_LOCK",
        "T4_FINGERPRINT_ORDER_LOCK",
        "T5_FINGERPRINT_UNIQUENESS_LOCK",
        "T6_FINGERPRINT_FORMAT_LOCK",
        "T7_TRACE_INTEGRITY_LOCK",
        "T8_NO_EXTRA_FIELDS_LOCK",
        "T9_IMMUTABILITY_LOCK",
    )


def test_phase37_fail_closed_behavior():
    assert FAIL_CLOSED_BEHAVIOR == "ANY_VIOLATION_RESULTS_IN_REJECTION"
