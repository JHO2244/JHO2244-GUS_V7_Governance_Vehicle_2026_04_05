"""
GUS v7 — Phase 63
Governance Notifications and Hooks Builder Tests (v0.1)

STRICT:
- Validate deterministic trigger logic only
- No inference
- Fail-closed enforcement
"""

from gus_v7.governance_notifications_hooks.governance_notifications_hooks_builder_v0_1 import (
    build_governance_notifications_hooks_v0_1,
)


def test_phase63_high_risk_triggers_both():
    dashboard_data = {
        "alert_status": "NO_ALERT",
        "exception_status": "NO_EXCEPTION",
    }
    risk_data = {
        "risk_level": "HIGH",
    }

    result = build_governance_notifications_hooks_v0_1(
        dashboard_data,
        risk_data,
    )

    assert result == {
        "notification_required": True,
        "hook_required": True,
        "notification_reason": "HIGH_RISK",
        "hook_reason": "HIGH_RISK",
    }


def test_phase63_alert_only_triggers_notification():
    dashboard_data = {
        "alert_status": "ALERT_RAISED",
        "exception_status": "NO_EXCEPTION",
    }
    risk_data = {
        "risk_level": "LOW",
    }

    result = build_governance_notifications_hooks_v0_1(
        dashboard_data,
        risk_data,
    )

    assert result == {
        "notification_required": True,
        "hook_required": False,
        "notification_reason": "ALERT_RAISED",
        "hook_reason": "NONE",
    }


def test_phase63_exception_only_triggers_hook():
    dashboard_data = {
        "alert_status": "NO_ALERT",
        "exception_status": "EXCEPTION_OPEN",
    }
    risk_data = {
        "risk_level": "LOW",
    }

    result = build_governance_notifications_hooks_v0_1(
        dashboard_data,
        risk_data,
    )

    assert result == {
        "notification_required": False,
        "hook_required": True,
        "notification_reason": "NONE",
        "hook_reason": "EXCEPTION_OPEN",
    }


def test_phase63_no_triggers_returns_none():
    dashboard_data = {
        "alert_status": "NO_ALERT",
        "exception_status": "NO_EXCEPTION",
    }
    risk_data = {
        "risk_level": "LOW",
    }

    result = build_governance_notifications_hooks_v0_1(
        dashboard_data,
        risk_data,
    )

    assert result == {
        "notification_required": False,
        "hook_required": False,
        "notification_reason": "NONE",
        "hook_reason": "NONE",
    }


def test_phase63_rejects_non_dict_dashboard_data():
    try:
        build_governance_notifications_hooks_v0_1([], {"risk_level": "LOW"})
        assert False
    except ValueError as exc:
        assert str(exc) == "INVALID_INPUT_TYPE"


def test_phase63_rejects_non_dict_risk_data():
    try:
        build_governance_notifications_hooks_v0_1(
            {"alert_status": "NO_ALERT", "exception_status": "NO_EXCEPTION"},
            [],
        )
        assert False
    except ValueError as exc:
        assert str(exc) == "INVALID_INPUT_TYPE"


def test_phase63_rejects_missing_alert_status():
    try:
        build_governance_notifications_hooks_v0_1(
            {"exception_status": "NO_EXCEPTION"},
            {"risk_level": "LOW"},
        )
        assert False
    except ValueError as exc:
        assert str(exc) == "MISSING_ALERT_STATUS"


def test_phase63_rejects_missing_exception_status():
    try:
        build_governance_notifications_hooks_v0_1(
            {"alert_status": "NO_ALERT"},
            {"risk_level": "LOW"},
        )
        assert False
    except ValueError as exc:
        assert str(exc) == "MISSING_EXCEPTION_STATUS"


def test_phase63_rejects_missing_risk_level():
    try:
        build_governance_notifications_hooks_v0_1(
            {"alert_status": "NO_ALERT", "exception_status": "NO_EXCEPTION"},
            {},
        )
        assert False
    except ValueError as exc:
        assert str(exc) == "MISSING_RISK_LEVEL"

def test_phase63_rejects_invalid_alert_status():
    try:
        build_governance_notifications_hooks_v0_1(
            {
                "alert_status": "MAYBE",
                "exception_status": "NO_EXCEPTION",
            },
            {
                "risk_level": "LOW",
            },
        )
        assert False
    except ValueError as exc:
        assert str(exc) == "INVALID_ALERT_STATUS"


def test_phase63_rejects_invalid_exception_status():
    try:
        build_governance_notifications_hooks_v0_1(
            {
                "alert_status": "NO_ALERT",
                "exception_status": "BROKEN",
            },
            {
                "risk_level": "LOW",
            },
        )
        assert False
    except ValueError as exc:
        assert str(exc) == "INVALID_EXCEPTION_STATUS"


def test_phase63_rejects_invalid_risk_level():
    try:
        build_governance_notifications_hooks_v0_1(
            {
                "alert_status": "NO_ALERT",
                "exception_status": "NO_EXCEPTION",
            },
            {
                "risk_level": "BANANA",
            },
        )
        assert False
    except ValueError as exc:
        assert str(exc) == "INVALID_RISK_LEVEL"
