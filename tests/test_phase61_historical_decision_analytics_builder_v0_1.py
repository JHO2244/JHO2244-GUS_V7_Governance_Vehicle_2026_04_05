"""
GUS v7 — Phase 61
Historical Decision Analytics Builder Tests (v0.1)

STRICT:
- Validate deterministic aggregation only
- No inference
- Fail-closed enforcement
"""

from gus_v7.historical_decision_analytics.historical_decision_analytics_builder_v0_1 import (
    build_historical_decision_analytics_v0_1,
)


def _valid_snapshots():
    return [
        {
            "total_decisions": 3,
            "governance_pass_count": 2,
            "governance_fail_count": 1,
            "compliance_result": "COMPLIANT",
            "exception_status": "NO_EXCEPTION",
            "alert_status": "NO_ALERT",
        },
        {
            "total_decisions": 4,
            "governance_pass_count": 3,
            "governance_fail_count": 1,
            "compliance_result": "NON_COMPLIANT",
            "exception_status": "EXCEPTION_OPEN",
            "alert_status": "ALERT_RAISED",
        },
        {
            "total_decisions": 2,
            "governance_pass_count": 1,
            "governance_fail_count": 1,
            "compliance_result": "COMPLIANT",
            "exception_status": "NO_EXCEPTION",
            "alert_status": "NO_ALERT",
        },
    ]


def test_phase61_builder_accepts_valid_snapshots():
    result = build_historical_decision_analytics_v0_1(_valid_snapshots())
    assert result == {
        "snapshot_count": 3,
        "total_decisions_sum": 9,
        "governance_pass_sum": 6,
        "governance_fail_sum": 3,
        "compliant_snapshot_count": 2,
        "non_compliant_snapshot_count": 1,
        "exception_open_snapshot_count": 1,
        "alert_raised_snapshot_count": 1,
    }


def test_phase61_builder_rejects_empty_input():
    try:
        build_historical_decision_analytics_v0_1([])
        assert False
    except ValueError as exc:
        assert str(exc) == "INVALID_SNAPSHOTS"


def test_phase61_builder_rejects_non_list_input():
    try:
        build_historical_decision_analytics_v0_1("not-a-list")
        assert False
    except ValueError as exc:
        assert str(exc) == "INVALID_SNAPSHOTS"


def test_phase61_builder_rejects_missing_field():
    snapshots = _valid_snapshots()
    del snapshots[0]["alert_status"]
    try:
        build_historical_decision_analytics_v0_1(snapshots)
        assert False
    except ValueError as exc:
        assert str(exc) == "INVALID_SNAPSHOT"


def test_phase61_builder_rejects_extra_field():
    snapshots = _valid_snapshots()
    snapshots[0]["extra"] = "not allowed"
    try:
        build_historical_decision_analytics_v0_1(snapshots)
        assert False
    except ValueError as exc:
        assert str(exc) == "INVALID_SNAPSHOT"


def test_phase61_builder_rejects_negative_integer():
    snapshots = _valid_snapshots()
    snapshots[0]["total_decisions"] = -1
    try:
        build_historical_decision_analytics_v0_1(snapshots)
        assert False
    except ValueError as exc:
        assert str(exc) == "INVALID_SNAPSHOT"


def test_phase61_builder_rejects_invalid_compliance_result():
    snapshots = _valid_snapshots()
    snapshots[0]["compliance_result"] = "MAYBE"
    try:
        build_historical_decision_analytics_v0_1(snapshots)
        assert False
    except ValueError as exc:
        assert str(exc) == "INVALID_SNAPSHOT"


def test_phase61_builder_rejects_invalid_exception_status():
    snapshots = _valid_snapshots()
    snapshots[0]["exception_status"] = "UNKNOWN"
    try:
        build_historical_decision_analytics_v0_1(snapshots)
        assert False
    except ValueError as exc:
        assert str(exc) == "INVALID_SNAPSHOT"


def test_phase61_builder_rejects_invalid_alert_status():
    snapshots = _valid_snapshots()
    snapshots[0]["alert_status"] = "LATER"
    try:
        build_historical_decision_analytics_v0_1(snapshots)
        assert False
    except ValueError as exc:
        assert str(exc) == "INVALID_SNAPSHOT"
