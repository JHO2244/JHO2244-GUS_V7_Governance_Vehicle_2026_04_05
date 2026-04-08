"""
GUS v7 — Phase 49
Decision Execution Trace Logger Tests (v0.1)

STRICT:
- Validate deterministic trace admissibility
- No inference
- Fail-closed enforcement
"""

from gus_v7.decision_execution_trace.decision_execution_trace_logger_v0_1 import (
    log_decision_execution_trace_v0_1,
)


def _valid_trace():
    return {
        "trace_id": "TRACE-001",
        "decision_id": "DEC-001",
        "case_id": "BC-01",
        "evidence_binding_id": "EB-001",
        "integrity_envelope_id": "IE-001",
        "final_integrity_verdict": "INTEGRITY_CONFIRMED",
        "execution_result": "EXECUTE",
        "trace_timestamp": "2026-04-08T12:00:00Z",
        "trace_sequence": "0001",
    }


def test_phase49_logger_accepts_valid_trace():
    assert log_decision_execution_trace_v0_1(_valid_trace()) == "VALID"


def test_phase49_logger_rejects_missing_field():
    trace = _valid_trace()
    del trace["execution_result"]
    assert log_decision_execution_trace_v0_1(trace) == "INVALID"


def test_phase49_logger_rejects_empty_required_field():
    trace = _valid_trace()
    trace["trace_id"] = ""
    assert log_decision_execution_trace_v0_1(trace) == "INVALID"


def test_phase49_logger_rejects_invalid_execution_result():
    trace = _valid_trace()
    trace["execution_result"] = "ALLOW"
    assert log_decision_execution_trace_v0_1(trace) == "INVALID"


def test_phase49_logger_rejects_invalid_integrity_verdict():
    trace = _valid_trace()
    trace["final_integrity_verdict"] = "UNKNOWN"
    assert log_decision_execution_trace_v0_1(trace) == "INVALID"


def test_phase49_logger_rejects_extra_field():
    trace = _valid_trace()
    trace["extra"] = "not allowed"
    assert log_decision_execution_trace_v0_1(trace) == "INVALID"
