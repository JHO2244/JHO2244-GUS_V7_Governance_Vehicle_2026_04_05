"""
GUS v7 — Phase 58
Policy Compliance Report Generator (v0.1)

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


REQUIRED_METRICS_KEYS = GOVERNANCE_METRICS_KEYS


def generate_policy_compliance_report_v0_1(metrics: dict) -> dict:
    """
    Returns:
        compliance report dict

    Fail-closed behavior:
    - malformed metrics -> ValueError
    """

    # -------------------------
    # STRUCTURE VALIDATION
    # -------------------------
    if set(metrics.keys()) != set(REQUIRED_METRICS_KEYS):
        raise ValueError("INVALID_METRICS")

    for field in REQUIRED_METRICS_KEYS:
        value = metrics[field]

        if not isinstance(value, int):
            raise ValueError("INVALID_METRICS")

        if value < 0:
            raise ValueError("INVALID_METRICS")

    # -------------------------
    # COMPLIANCE LOGIC
    # -------------------------
    governance_fail_count = metrics["governance_fail_count"]

    if governance_fail_count == 0:
        compliance_result = "COMPLIANT"
    else:
        compliance_result = "NON_COMPLIANT"

    return {
        "total_decisions": metrics["total_decisions"],
        "governance_pass_count": metrics["governance_pass_count"],
        "governance_fail_count": metrics["governance_fail_count"],
        "compliance_result": compliance_result,
    }
