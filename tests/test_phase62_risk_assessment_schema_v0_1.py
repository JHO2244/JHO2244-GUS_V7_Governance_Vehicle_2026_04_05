"""
GUS v7 — Phase 62
Risk Assessment Schema Tests (v0.1)

STRICT:
- Validate structure only
- No inference
- Fail-closed enforcement
"""

from gus_v7.risk_assessment.risk_assessment_schema_v0_1 import (
    RISK_ASSESSMENT_KEYS,
    REQUIRED_FIELDS,
    VALID_RISK_LEVELS,
    RISK_FLAGS_COUNT_INTEGER,
    NO_NEGATIVE_VALUES,
    INSTABILITY_BOOLEAN_ONLY,
    NO_EXTRA_FIELDS_ALLOWED,
    VALIDATION_RULES,
    FAIL_CLOSED_BEHAVIOR,
)


def test_phase62_risk_assessment_keys_exact_match():
    expected = (
        "risk_level",
        "risk_flags_count",
        "instability_detected",
    )
    assert RISK_ASSESSMENT_KEYS == expected


def test_phase62_required_fields_match_keys():
    assert REQUIRED_FIELDS == RISK_ASSESSMENT_KEYS


def test_phase62_valid_risk_levels_exact_match():
    assert VALID_RISK_LEVELS == ("LOW", "MEDIUM", "HIGH")


def test_phase62_risk_flags_count_integer_lock():
    assert RISK_FLAGS_COUNT_INTEGER is True


def test_phase62_non_negative_lock():
    assert NO_NEGATIVE_VALUES is True


def test_phase62_instability_boolean_only_lock():
    assert INSTABILITY_BOOLEAN_ONLY is True


def test_phase62_no_extra_fields_lock():
    assert NO_EXTRA_FIELDS_ALLOWED is True


def test_phase62_validation_rules_defined():
    assert "R1_STRUCTURE_LOCK" in VALIDATION_RULES
    assert "R7_NO_EXTRA_FIELDS_LOCK" in VALIDATION_RULES


def test_phase62_fail_closed_behavior():
    assert (
        FAIL_CLOSED_BEHAVIOR
        == "ANY_VIOLATION_RESULTS_IN_INVALID_RISK_ASSESSMENT"
    )
