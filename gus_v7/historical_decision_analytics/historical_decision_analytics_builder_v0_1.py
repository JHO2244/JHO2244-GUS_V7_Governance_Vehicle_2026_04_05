"""
GUS v7 — Phase 61
Historical Decision Analytics Builder (v0.1)

STRICT:
- Deterministic
- Fail-closed
- No inference
- No mutation
- No external calls
"""

from gus_v7.governance_dashboard_data.governance_dashboard_data_schema_v0_1 import (
    GOVERNANCE_DASHBOARD_DATA_KEYS,
    INTEGER_FIELDS,
    VALID_COMPLIANCE_RESULTS,
    VALID_EXCEPTION_STATUS,
    VALID_ALERT_STATUS,
)


def build_historical_decision_analytics_v0_1(
    snapshots: list,
) -> dict:
    """
    Input:
        snapshots: non-empty list of Phase 60 dashboard data dicts

    Output:
        aggregated deterministic history analytics dict

    Fail-closed:
        - invalid structure
        - invalid values
        - empty list
    """

    if not isinstance(snapshots, list) or len(snapshots) == 0:
        raise ValueError("INVALID_SNAPSHOTS")

    snapshot_count = 0
    total_decisions_sum = 0
    governance_pass_sum = 0
    governance_fail_sum = 0
    compliant_snapshot_count = 0
    non_compliant_snapshot_count = 0
    exception_open_snapshot_count = 0
    alert_raised_snapshot_count = 0

    for snap in snapshots:

        # -------------------------
        # STRUCTURE VALIDATION
        # -------------------------
        if set(snap.keys()) != set(GOVERNANCE_DASHBOARD_DATA_KEYS):
            raise ValueError("INVALID_SNAPSHOT")

        # -------------------------
        # INTEGER FIELD VALIDATION
        # -------------------------
        for k in INTEGER_FIELDS:
            v = snap[k]
            if not isinstance(v, int) or v < 0:
                raise ValueError("INVALID_SNAPSHOT")

        # -------------------------
        # ENUM VALIDATION
        # -------------------------
        if snap["compliance_result"] not in VALID_COMPLIANCE_RESULTS:
            raise ValueError("INVALID_SNAPSHOT")

        if snap["exception_status"] not in VALID_EXCEPTION_STATUS:
            raise ValueError("INVALID_SNAPSHOT")

        if snap["alert_status"] not in VALID_ALERT_STATUS:
            raise ValueError("INVALID_SNAPSHOT")

        # -------------------------
        # AGGREGATION
        # -------------------------
        snapshot_count += 1
        total_decisions_sum += snap["total_decisions"]
        governance_pass_sum += snap["governance_pass_count"]
        governance_fail_sum += snap["governance_fail_count"]

        if snap["compliance_result"] == "COMPLIANT":
            compliant_snapshot_count += 1
        else:
            non_compliant_snapshot_count += 1

        if snap["exception_status"] == "EXCEPTION_OPEN":
            exception_open_snapshot_count += 1

        if snap["alert_status"] == "ALERT_RAISED":
            alert_raised_snapshot_count += 1

    return {
        "snapshot_count": snapshot_count,
        "total_decisions_sum": total_decisions_sum,
        "governance_pass_sum": governance_pass_sum,
        "governance_fail_sum": governance_fail_sum,
        "compliant_snapshot_count": compliant_snapshot_count,
        "non_compliant_snapshot_count": non_compliant_snapshot_count,
        "exception_open_snapshot_count": exception_open_snapshot_count,
        "alert_raised_snapshot_count": alert_raised_snapshot_count,
    }
