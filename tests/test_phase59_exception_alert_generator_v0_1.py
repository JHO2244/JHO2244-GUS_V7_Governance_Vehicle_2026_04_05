"""
GUS v7 — Phase 59
Exception Logging & Alerts Generator Tests (v0.1)

STRICT:
- Validate deterministic alert generation only
- No inference
- Fail-closed enforcement
"""

from gus_v7.exception_logging_alerts.exception_alert_generator_v0_1 import (
    generate_exception_alert_v0_1,
)


def _compliant_report():
    return {
        "total_decisions": 3,
        "governance_pass_count": 3,
        "governance_fail_count": 0,
        "compliance_result": "COMPLIANT",
    }


def _non_compliant_report():
    return {
        "total_decisions": 3,
        "governance_pass_count": 2,
        "governance_fail_count": 1,
        "compliance_result": "NON_COMPLIANT",
    }


def test_phase59_generator_returns_no_exception_no_alert():
    result = generate_exception_alert_v0_1(_compliant_report())
    assert result == {
        "total_decisions": 3,
        "governance_fail_count": 0,
        "compliance_result": "COMPLIANT",
        "exception_status": "NO_EXCEPTION",
        "alert_status": "NO_ALERT",
    }


def test_phase59_generator_returns_exception_open_alert_raised():
    result = generate_exception_alert_v0_1(_non_compliant_report())
    assert result == {
        "total_decisions": 3,
        "governance_fail_count": 1,
        "compliance_result": "NON_COMPLIANT",
        "exception_status": "EXCEPTION_OPEN",
        "alert_status": "ALERT_RAISED",
    }


def test_phase59_generator_rejects_missing_field():
    report = _compliant_report()
    del report["compliance_result"]
    try:
        generate_exception_alert_v0_1(report)
        assert False
    except ValueError as exc:
        assert str(exc) == "INVALID_REPORT"


def test_phase59_generator_rejects_extra_field():
    report = _compliant_report()
    report["extra"] = 1
    try:
        generate_exception_alert_v0_1(report)
        assert False
    except ValueError as exc:
        assert str(exc) == "INVALID_REPORT"


def test_phase59_generator_rejects_invalid_compliance_result():
    report = _compliant_report()
    report["compliance_result"] = "UNKNOWN"
    try:
        generate_exception_alert_v0_1(report)
        assert False
    except ValueError as exc:
        assert str(exc) == "INVALID_REPORT"


def test_phase59_generator_rejects_non_integer_field():
    report = _compliant_report()
    report["total_decisions"] = "3"
    try:
        generate_exception_alert_v0_1(report)
        assert False
    except ValueError as exc:
        assert str(exc) == "INVALID_REPORT"


def test_phase59_generator_rejects_negative_value():
    report = _compliant_report()
    report["governance_fail_count"] = -1
    try:
        generate_exception_alert_v0_1(report)
        assert False
    except ValueError as exc:
        assert str(exc) == "INVALID_REPORT"
