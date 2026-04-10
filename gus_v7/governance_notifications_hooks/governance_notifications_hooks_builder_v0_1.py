"""
GUS v7 — Phase 63
Governance Notifications and Hooks Builder (v0.1)

STRICT:
- Deterministic
- No external effects
- No async
- No inference
- Fail-closed
"""

from gus_v7.governance_notifications_hooks.governance_notifications_hooks_schema_v0_1 import (
    GOVERNANCE_NOTIFICATIONS_HOOKS_KEYS,
    VALID_NOTIFICATION_REASONS,
    VALID_HOOK_REASONS,
)


def build_governance_notifications_hooks_v0_1(
    dashboard_data: dict,
    risk_data: dict,
) -> dict:
    """
    Deterministic evaluation of notification and hook triggers.

    Expected inputs (fail-closed if missing):
    - dashboard_data["alert_status"]
    - dashboard_data["exception_status"]
    - risk_data["risk_level"]
    """

    # =========================
    # FAIL-CLOSED INPUT CHECK
    # =========================

    if not isinstance(dashboard_data, dict) or not isinstance(risk_data, dict):
        raise ValueError("INVALID_INPUT_TYPE")

    required_dashboard_fields = ("alert_status", "exception_status")
    for field in required_dashboard_fields:
        if field not in dashboard_data:
            raise ValueError(f"MISSING_{field.upper()}")

    if "risk_level" not in risk_data:
        raise ValueError("MISSING_RISK_LEVEL")

    alert_status = dashboard_data["alert_status"]
    exception_status = dashboard_data["exception_status"]
    risk_level = risk_data["risk_level"]

    # =========================
    # VALUE LOCK (CRITICAL)
    # =========================

    valid_alert_status = ("NO_ALERT", "ALERT_RAISED")
    valid_exception_status = ("NO_EXCEPTION", "EXCEPTION_OPEN")
    valid_risk_level = ("LOW", "MEDIUM", "HIGH")

    if alert_status not in valid_alert_status:
        raise ValueError("INVALID_ALERT_STATUS")

    if exception_status not in valid_exception_status:
        raise ValueError("INVALID_EXCEPTION_STATUS")

    if risk_level not in valid_risk_level:
        raise ValueError("INVALID_RISK_LEVEL")

    # =========================
    # INITIAL STATE
    # =========================

    notification_required = False
    hook_required = False
    notification_reason = "NONE"
    hook_reason = "NONE"

    # =========================
    # RULES
    # =========================

    # HIGH RISK → both
    if risk_level == "HIGH":
        notification_required = True
        hook_required = True
        notification_reason = "HIGH_RISK"
        hook_reason = "HIGH_RISK"

    else:
        # ALERT → notification
        if alert_status == "ALERT_RAISED":
            notification_required = True
            notification_reason = "ALERT_RAISED"

        # EXCEPTION → hook
        if exception_status == "EXCEPTION_OPEN":
            hook_required = True
            hook_reason = "EXCEPTION_OPEN"

    # =========================
    # OUTPUT
    # =========================

    output = {
        "notification_required": notification_required,
        "hook_required": hook_required,
        "notification_reason": notification_reason,
        "hook_reason": hook_reason,
    }

    # Final safety lock (structure)
    if tuple(output.keys()) != GOVERNANCE_NOTIFICATIONS_HOOKS_KEYS:
        raise ValueError("STRUCTURE_VIOLATION")

    if notification_reason not in VALID_NOTIFICATION_REASONS:
        raise ValueError("INVALID_NOTIFICATION_REASON")

    if hook_reason not in VALID_HOOK_REASONS:
        raise ValueError("INVALID_HOOK_REASON")

    return output
