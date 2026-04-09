"""
GUS v7 — Phase 59
Exception Logging & Alerts Generator (v0.1)

STRICT:
- Deterministic
- Fail-closed
- No inference
- No mutation
- No external calls
"""

from gus_v7.policy_compliance_reporting.policy_compliance_report_schema_v0_1 import (
    POLICY_COMPLIANCE_REPORT_KEYS,
)


REQUIRED_REPORT_KEYS = POLICY_COMPLIANCE_REPORT_KEYS


def generate_exception_alert_v0_1(report: dict) -> dict:
    """
    Returns:
        exception alert dict

    Fail-closed behavior:
    - malformed report -> ValueError
    """

    # -------------------------
    # STRUCTURE VALIDATION
    # -------------------------
    if set(report.keys()) != set(REQUIRED_REPORT_KEYS):
        raise ValueError("INVALID_REPORT")

    for key in REQUIRED_REPORT_KEYS:
        value = report[key]

        if key == "compliance_result":
            if value not in ("COMPLIANT", "NON_COMPLIANT"):
                raise ValueError("INVALID_REPORT")
        else:
            if not isinstance(value, int):
                raise ValueError("INVALID_REPORT")

            if value < 0:
                raise ValueError("INVALID_REPORT")

    # -------------------------
    # ALERT LOGIC
    # -------------------------
    compliance_result = report["compliance_result"]

    if compliance_result == "COMPLIANT":
        exception_status = "NO_EXCEPTION"
        alert_status = "NO_ALERT"
    else:
        exception_status = "EXCEPTION_OPEN"
        alert_status = "ALERT_RAISED"

    return {
        "total_decisions": report["total_decisions"],
        "governance_fail_count": report["governance_fail_count"],
        "compliance_result": compliance_result,
        "exception_status": exception_status,
        "alert_status": alert_status,
    }
