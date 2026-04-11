"""
GUS v7 — Phase 34
Evidence Binding Schema Contract Tests (v0.1)

STRICT:
- Validate structure only
- No inference
- Fail-closed enforcement
"""

from gus_v7.evidence_binding.evidence_binding_schema_v0_1 import (
    EVIDENCE_BINDING_KEYS,
    EVIDENCE_BUNDLE_TYPE_REQUIRED,
    EVIDENCE_BUNDLE_MIN_ITEMS,
    EVIDENCE_BUNDLE_ORDER_REQUIRED,
    EVIDENCE_BUNDLE_ITEMS_MUST_CONFORM_TO,
    SUPPORTED_EVALUATION_RESULTS_TYPE_REQUIRED,
    SUPPORTED_EVALUATION_RESULTS_MIN_ITEMS,
    VALID_EVALUATION_RESULTS,
    BINDING_INTEGRITY_KEYS,
    VALID_BINDING_STATUS_VALUES,
    BINDING_MODE_REQUIRED,
    REQUIRED_NON_EMPTY_FIELDS,
    NO_EXTRA_FIELDS_ALLOWED,
    IMMUTABLE_AFTER_CREATION,
    VALIDATION_RULES,
    FAIL_CLOSED_BEHAVIOR,
)


def test_phase34_binding_keys_exact_match():
    expected = (
        "evaluation_result",
        "evidence_bundle",
        "supported_evaluation_results",
        "binding_integrity",
    )
    assert EVIDENCE_BINDING_KEYS == expected


def test_phase34_required_fields_match_top_level_keys():
    assert REQUIRED_NON_EMPTY_FIELDS == EVIDENCE_BINDING_KEYS


def test_phase34_evidence_bundle_type_required():
    assert EVIDENCE_BUNDLE_TYPE_REQUIRED == "tuple"


def test_phase34_evidence_bundle_min_items():
    assert EVIDENCE_BUNDLE_MIN_ITEMS == 1


def test_phase34_evidence_bundle_order_required():
    assert EVIDENCE_BUNDLE_ORDER_REQUIRED is True


def test_phase34_evidence_bundle_phase33_conformance_required():
    assert EVIDENCE_BUNDLE_ITEMS_MUST_CONFORM_TO == "PHASE33_EVIDENCE_SCHEMA_V0_1"


def test_phase34_supported_evaluation_results_type_required():
    assert SUPPORTED_EVALUATION_RESULTS_TYPE_REQUIRED == "tuple"


def test_phase34_supported_evaluation_results_min_items():
    assert SUPPORTED_EVALUATION_RESULTS_MIN_ITEMS == 1


def test_phase34_valid_evaluation_results_locked():
    assert VALID_EVALUATION_RESULTS == (
        "PASS",
        "FAIL",
        "INSUFFICIENT_EVIDENCE",
        "OUT_OF_SCOPE",
    )


def test_phase34_binding_integrity_keys_exact_match():
    expected = (
        "binding_status",
        "bundle_count",
        "all_evidence_bound",
        "binding_mode",
    )
    assert BINDING_INTEGRITY_KEYS == expected


def test_phase34_valid_binding_status_values():
    assert VALID_BINDING_STATUS_VALUES == ("unverified", "verified")


def test_phase34_binding_mode_required():
    assert BINDING_MODE_REQUIRED == "deterministic_attachment"


def test_phase34_no_extra_fields_lock():
    assert NO_EXTRA_FIELDS_ALLOWED is True


def test_phase34_immutability_lock():
    assert IMMUTABLE_AFTER_CREATION is True


def test_phase34_validation_rules_defined():
    assert VALIDATION_RULES == (
        "B1_STRUCTURE_LOCK",
        "B2_REQUIRED_FIELDS_LOCK",
        "B3_EVIDENCE_BUNDLE_PRESENCE_LOCK",
        "B4_EVIDENCE_BUNDLE_ORDER_LOCK",
        "B5_PHASE33_CONFORMANCE_LOCK",
        "B6_SUPPORTED_EVALUATION_RESULTS_LOCK",
        "B7_BINDING_INTEGRITY_LOCK",
        "B8_NO_EXTRA_FIELDS_LOCK",
        "B9_IMMUTABILITY_LOCK",
    )


def test_phase34_fail_closed_behavior():
    assert FAIL_CLOSED_BEHAVIOR == "ANY_VIOLATION_RESULTS_IN_REJECTION"
