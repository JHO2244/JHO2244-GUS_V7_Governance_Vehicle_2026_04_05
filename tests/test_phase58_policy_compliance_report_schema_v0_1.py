"""
GUS v7 — Phase 58
Policy Compliance Report Schema Tests (v0.1)

STRICT:
- Validate structure only
- No inference
- Fail-closed enforcement
"""

from gus_v7.policy_compliance_reporting.policy_compliance_report_schema_v0_1 import (
    POLICY_COMPLIANCE_REPORT_KEYS,
    REQUIRED_FIELDS,
    INTEGER_FIELDS,
    VALID_COMPLIANCE_RESULTS,
    NO_NEGATIVE_VALUES,
    NO_EXTRA_FIELDS_ALLOWED,
    VALIDATION_RULES,
    FAIL_CLOSED_BEHAVIOR,
)


def test_phase58_report_keys_exact_match():
    expected = (
        "total_decisions",
        "governance_pass_count",
        "governance_fail_count",
        "compliance_result",
    )
    assert POLICY_COMPLIANCE_REPORT_KEYS == expected


def test_phase58_required_fields_match_keys():
    assert REQUIRED_FIELDS == POLICY_COMPLIANCE_REPORT_KEYS


def test_phase58_integer_fields_exact_match():
    assert INTEGER_FIELDS == (
        "total_decisions",
        "governance_pass_count",
        "governance_fail_count",
    )


def test_phase58_valid_compliance_results_defined():
    assert VALID_COMPLIANCE_RESULTS == (
        "COMPLIANT",
        "NON_COMPLIANT",
    )


def test_phase58_non_negative_lock():
    assert NO_NEGATIVE_VALUES is True


def test_phase58_no_extra_fields_lock():
    assert NO_EXTRA_FIELDS_ALLOWED is True


def test_phase58_validation_rules_defined():
    assert "R1_STRUCTURE_LOCK" in VALIDATION_RULES
    assert "R6_NO_EXTRA_FIELDS_LOCK" in VALIDATION_RULES


def test_phase58_fail_closed_behavior():
    assert (
        FAIL_CLOSED_BEHAVIOR
        == "ANY_VIOLATION_RESULTS_IN_INVALID_REPORT"
    )
