"""
GUS v7 — Phase 58
Policy Compliance Report Generator Tests (v0.1)

STRICT:
- Validate deterministic report generation only
- No inference
- Fail-closed enforcement
"""

from gus_v7.policy_compliance_reporting.policy_compliance_report_generator_v0_1 import (
    generate_policy_compliance_report_v0_1,
)


def _compliant_metrics():
    return {
        "total_decisions": 3,
        "execute_count": 2,
        "block_count": 1,
        "integrity_confirmed_count": 2,
        "integrity_rejected_count": 1,
        "governance_pass_count": 3,
        "governance_fail_count": 0,
    }


def _non_compliant_metrics():
    return {
        "total_decisions": 3,
        "execute_count": 2,
        "block_count": 1,
        "integrity_confirmed_count": 2,
        "integrity_rejected_count": 1,
        "governance_pass_count": 2,
        "governance_fail_count": 1,
    }


def test_phase58_generator_returns_compliant_report():
    result = generate_policy_compliance_report_v0_1(_compliant_metrics())
    assert result == {
        "total_decisions": 3,
        "governance_pass_count": 3,
        "governance_fail_count": 0,
        "compliance_result": "COMPLIANT",
    }


def test_phase58_generator_returns_non_compliant_report():
    result = generate_policy_compliance_report_v0_1(_non_compliant_metrics())
    assert result == {
        "total_decisions": 3,
        "governance_pass_count": 2,
        "governance_fail_count": 1,
        "compliance_result": "NON_COMPLIANT",
    }


def test_phase58_generator_rejects_missing_field():
    metrics = _compliant_metrics()
    del metrics["governance_fail_count"]
    try:
        generate_policy_compliance_report_v0_1(metrics)
        assert False
    except ValueError as exc:
        assert str(exc) == "INVALID_METRICS"


def test_phase58_generator_rejects_extra_field():
    metrics = _compliant_metrics()
    metrics["extra"] = 1
    try:
        generate_policy_compliance_report_v0_1(metrics)
        assert False
    except ValueError as exc:
        assert str(exc) == "INVALID_METRICS"


def test_phase58_generator_rejects_non_integer_field():
    metrics = _compliant_metrics()
    metrics["total_decisions"] = "3"
    try:
        generate_policy_compliance_report_v0_1(metrics)
        assert False
    except ValueError as exc:
        assert str(exc) == "INVALID_METRICS"


def test_phase58_generator_rejects_negative_value():
    metrics = _compliant_metrics()
    metrics["governance_fail_count"] = -1
    try:
        generate_policy_compliance_report_v0_1(metrics)
        assert False
    except ValueError as exc:
        assert str(exc) == "INVALID_METRICS"
