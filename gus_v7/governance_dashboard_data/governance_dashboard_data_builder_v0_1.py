"""
GUS v7 — Phase 60
Governance Dashboard Data Builder (v0.1)

STRICT:
- Deterministic
- Fail-closed
- No inference
- No mutation
- No external calls
"""

from gus_v7.governance_metrics.governance_metrics_schema_v0_1 import (
    GOVERNANCE_METRICS_KEYS,
)

from gus_v7.policy_compliance_reporting.policy_compliance_report_schema_v0_1 import (
    POLICY_COMPLIANCE_REPORT_KEYS,
)

from gus_v7.exception_logging_alerts.exception_alert_schema_v0_1 import (
    EXCEPTION_ALERT_KEYS,
)


def build_governance_dashboard_data_v0_1(
    metrics: dict,
    report: dict,
    alert: dict,
) -> dict:
    """
    Returns:
        unified dashboard data dict

    Fail-closed behavior:
    - malformed inputs -> ValueError
    """

    # -------------------------
    # VALIDATE METRICS
    # -------------------------
    if set(metrics.keys()) != set(GOVERNANCE_METRICS_KEYS):
        raise ValueError("INVALID_METRICS")

    for k in GOVERNANCE_METRICS_KEYS:
        v = metrics[k]
        if not isinstance(v, int) or v < 0:
            raise ValueError("INVALID_METRICS")

    # -------------------------
    # VALIDATE REPORT
    # -------------------------
    if set(report.keys()) != set(POLICY_COMPLIANCE_REPORT_KEYS):
        raise ValueError("INVALID_REPORT")

    for k in POLICY_COMPLIANCE_REPORT_KEYS:
        v = report[k]
        if k == "compliance_result":
            if v not in ("COMPLIANT", "NON_COMPLIANT"):
                raise ValueError("INVALID_REPORT")
        else:
            if not isinstance(v, int) or v < 0:
                raise ValueError("INVALID_REPORT")

    # -------------------------
    # VALIDATE ALERT
    # -------------------------
    if set(alert.keys()) != set(EXCEPTION_ALERT_KEYS):
        raise ValueError("INVALID_ALERT")

    for k in EXCEPTION_ALERT_KEYS:
        v = alert[k]
        if k in ("compliance_result", "exception_status", "alert_status"):
            continue
        if not isinstance(v, int) or v < 0:
            raise ValueError("INVALID_ALERT")

    if alert["compliance_result"] not in ("COMPLIANT", "NON_COMPLIANT"):
        raise ValueError("INVALID_ALERT")

    if alert["exception_status"] not in ("NO_EXCEPTION", "EXCEPTION_OPEN"):
        raise ValueError("INVALID_ALERT")

    if alert["alert_status"] not in ("NO_ALERT", "ALERT_RAISED"):
        raise ValueError("INVALID_ALERT")

    # -------------------------
    # CONSISTENCY CHECK
    # -------------------------
    if report["compliance_result"] != alert["compliance_result"]:
        raise ValueError("INCONSISTENT_INPUTS")

    # -------------------------
    # BUILD OUTPUT
    # -------------------------
    return {
        "total_decisions": metrics["total_decisions"],
        "governance_pass_count": metrics["governance_pass_count"],
        "governance_fail_count": metrics["governance_fail_count"],
        "compliance_result": report["compliance_result"],
        "exception_status": alert["exception_status"],
        "alert_status": alert["alert_status"],
    }
