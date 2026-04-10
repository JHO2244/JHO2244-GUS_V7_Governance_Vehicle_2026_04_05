"""
GUS v7 — Phase 63
Governance Notifications and Hooks Schema Tests (v0.1)

STRICT:
- Validate structure only
- No inference
- Fail-closed enforcement
"""

from gus_v7.governance_notifications_hooks.governance_notifications_hooks_schema_v0_1 import (
    GOVERNANCE_NOTIFICATIONS_HOOKS_KEYS,
    REQUIRED_FIELDS,
    BOOLEAN_FIELDS,
    VALID_NOTIFICATION_REASONS,
    VALID_HOOK_REASONS,
    NO_EXTRA_FIELDS_ALLOWED,
    VALIDATION_RULES,
    FAIL_CLOSED_BEHAVIOR,
)


def test_phase63_output_keys_exact_match():
    expected = (
        "notification_required",
        "hook_required",
        "notification_reason",
        "hook_reason",
    )
    assert GOVERNANCE_NOTIFICATIONS_HOOKS_KEYS == expected


def test_phase63_required_fields_match_keys():
    assert REQUIRED_FIELDS == GOVERNANCE_NOTIFICATIONS_HOOKS_KEYS


def test_phase63_boolean_fields_exact_match():
    assert BOOLEAN_FIELDS == (
        "notification_required",
        "hook_required",
    )


def test_phase63_valid_notification_reasons_exact_match():
    assert VALID_NOTIFICATION_REASONS == (
        "NONE",
        "HIGH_RISK",
        "ALERT_RAISED",
    )


def test_phase63_valid_hook_reasons_exact_match():
    assert VALID_HOOK_REASONS == (
        "NONE",
        "HIGH_RISK",
        "EXCEPTION_OPEN",
    )


def test_phase63_no_extra_fields_lock():
    assert NO_EXTRA_FIELDS_ALLOWED is True


def test_phase63_validation_rules_defined():
    assert "N1_STRUCTURE_LOCK" in VALIDATION_RULES
    assert "N6_NO_EXTRA_FIELDS_LOCK" in VALIDATION_RULES


def test_phase63_fail_closed_behavior():
    assert (
        FAIL_CLOSED_BEHAVIOR
        == "ANY_VIOLATION_RESULTS_IN_INVALID_NOTIFICATION_HOOK_OUTPUT"
    )
