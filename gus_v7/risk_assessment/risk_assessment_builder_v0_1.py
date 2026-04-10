"""
GUS v7 — Phase 62
Risk Assessment Builder (v0.1)

STRICT:
- Deterministic
- Fail-closed
- No inference
- No mutation
- No external calls
"""

from gus_v7.historical_decision_analytics.historical_decision_analytics_schema_v0_1 import (
    HISTORICAL_DECISION_ANALYTICS_KEYS,
)


def build_risk_assessment_v0_1(history: dict) -> dict:
    """
    Input:
        Phase 61 historical analytics dict

    Output:
        risk assessment dict

    Fail-closed:
        - invalid structure
        - invalid values
    """

    # -------------------------
    # STRUCTURE VALIDATION
    # -------------------------
    if set(history.keys()) != set(HISTORICAL_DECISION_ANALYTICS_KEYS):
        raise ValueError("INVALID_HISTORY")

    # -------------------------
    # TYPE + VALUE VALIDATION
    # -------------------------
    for v in history.values():
        if not isinstance(v, int) or v < 0:
            raise ValueError("INVALID_HISTORY")

    # -------------------------
    # SIGNAL DETECTION
    # -------------------------
    failure_pressure = history["governance_fail_sum"] > history["governance_pass_sum"]

    compliance_degradation = (
        history["non_compliant_snapshot_count"]
        > history["compliant_snapshot_count"]
    )

    exception_exposure = history["exception_open_snapshot_count"] > 0

    alert_activity = history["alert_raised_snapshot_count"] > 0

    signals = [
        failure_pressure,
        compliance_degradation,
        exception_exposure,
        alert_activity,
    ]

    risk_flags_count = sum(1 for s in signals if s)

    # -------------------------
    # RISK CLASSIFICATION
    # -------------------------
    if risk_flags_count == 0:
        risk_level = "LOW"
    elif risk_flags_count == 1:
        risk_level = "MEDIUM"
    else:
        risk_level = "HIGH"

    instability_detected = risk_flags_count >= 1

    return {
        "risk_level": risk_level,
        "risk_flags_count": risk_flags_count,
        "instability_detected": instability_detected,
    }
