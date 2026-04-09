"""
GUS v7 — Phase 60
Governance Dashboard Data Builder Tests (v0.1)

STRICT:
- Validate deterministic dashboard data assembly only
- No inference
- Fail-closed enforcement
"""

from gus_v7.governance_dashboard_data.governance_dashboard_data_builder_v0_1 import (
    build_governance_dashboard_data_v0_1,
)


def _metrics():
    return {
        "total_decisions": 3,
        "execute_count": 2,
        "block_count": 1,
        "integrity_confirmed_count": 2,
        "integrity_rejected_count": 1,
        "governance_pass_count": 2,
        "governance_fail_count": 1,
    }


def _report():
    return {
        "total_decisions": 3,
        "governance_pass_count": 2,
        "governance_fail_count": 1,
        "compliance_result": "NON_COMPLIANT",
    }


def _alert():
    return {
        "total_decisions": 3,
        "governance_fail_count": 1,
        "compliance_result": "NON_COMPLIANT",
        "exception_status": "EXCEPTION_OPEN",
        "alert_status": "ALERT_RAISED",
    }


def test_phase60_builder_returns_dashboard_data():
    result = build_governance_dashboard_data_v0_1(
        _metrics(),
        _report(),
        _alert(),
    )
    assert result == {
        "total_decisions": 3,
        "governance_pass_count": 2,
        "governance_fail_count": 1,
        "compliance_result": "NON_COMPLIANT",
        "exception_status": "EXCEPTION_OPEN",
        "alert_status": "ALERT_RAISED",
    }


def test_phase60_builder_rejects_invalid_metrics():
    metrics = _metrics()
    del metrics["governance_fail_count"]
    try:
        build_governance_dashboard_data_v0_1(metrics, _report(), _alert())
        assert False
    except ValueError as exc:
        assert str(exc) == "INVALID_METRICS"


def test_phase60_builder_rejects_invalid_report():
    report = _report()
    report["extra"] = 1
    try:
        build_governance_dashboard_data_v0_1(_metrics(), report, _alert())
        assert False
    except ValueError as exc:
        assert str(exc) == "INVALID_REPORT"


def test_phase60_builder_rejects_invalid_alert():
    alert = _alert()
    alert["alert_status"] = "MAYBE"
    try:
        build_governance_dashboard_data_v0_1(_metrics(), _report(), alert)
        assert False
    except ValueError as exc:
        assert str(exc) == "INVALID_ALERT"


def test_phase60_builder_rejects_inconsistent_inputs():
    report = _report()
    report["compliance_result"] = "COMPLIANT"
    try:
        build_governance_dashboard_data_v0_1(_metrics(), report, _alert())
        assert False
    except ValueError as exc:
        assert str(exc) == "INCONSISTENT_INPUTS"
