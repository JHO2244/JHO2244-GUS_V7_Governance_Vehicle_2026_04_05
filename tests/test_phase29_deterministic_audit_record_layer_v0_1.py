"""
GUS v7 — Phase 29
Deterministic Audit Record Layer Tests (v0.1)

STRICT:
- Only verified envelope + valid drift report allowed
- Deterministic audit fingerprint
- Fail-closed on invalid inputs
"""

from __future__ import annotations

from copy import deepcopy

from gus_v7.routing.case_validator_router_v0_1 import route_and_validate_case
from gus_v7.routing.execution_consistency_lock_v0_1 import (
    wrap_canonical_execution_output_v0_1,
    detect_execution_drift_v0_1,
    create_audit_record_v0_1,
    verify_audit_record_v0_1,
    AUDIT_VALID,
    AUDIT_INVALID,
    NO_DRIFT,
)


def _build_case() -> dict:
    return {
        "case_id": "BC-01",
        "case_name": "Simple Case",
        "case_version": "v0.1",
        "case_class": "benchmark_pass",
        "context": {"domain": "test"},
        "agents": {"a": "A"},
        "process": [],
        "evidence_pack": {},
        "integrity_flags": {"criteria_predefined": True},
        "expected_output": "PASS",
    }


def test_phase29_valid_audit_record() -> None:
    case = _build_case()
    baseline = deepcopy(case)

    output = route_and_validate_case(case)
    envelope = wrap_canonical_execution_output_v0_1(output)
    drift = detect_execution_drift_v0_1(envelope, output)

    record = create_audit_record_v0_1(envelope, drift)

    assert record["audit_status"] == AUDIT_VALID
    assert verify_audit_record_v0_1(record) is True
    assert case == baseline


def test_phase29_deterministic_fingerprint() -> None:
    case = _build_case()

    output = route_and_validate_case(case)
    envelope = wrap_canonical_execution_output_v0_1(output)
    drift = detect_execution_drift_v0_1(envelope, output)

    r1 = create_audit_record_v0_1(envelope, drift)
    r2 = create_audit_record_v0_1(envelope, drift)

    assert r1["audit_fingerprint"] == r2["audit_fingerprint"]


def test_phase29_invalid_envelope_fails_closed() -> None:
    drift = {"drift_status": NO_DRIFT}
    record = create_audit_record_v0_1("INVALID", drift)

    assert record["audit_status"] == AUDIT_INVALID
    assert verify_audit_record_v0_1(record) is False


def test_phase29_invalid_drift_fails_closed() -> None:
    case = _build_case()
    output = route_and_validate_case(case)
    envelope = wrap_canonical_execution_output_v0_1(output)

    record = create_audit_record_v0_1(envelope, "INVALID")

    assert record["audit_status"] == AUDIT_INVALID
    assert verify_audit_record_v0_1(record) is False


def test_phase29_tampered_fingerprint_fails() -> None:
    case = _build_case()
    output = route_and_validate_case(case)
    envelope = wrap_canonical_execution_output_v0_1(output)
    drift = detect_execution_drift_v0_1(envelope, output)

    record = create_audit_record_v0_1(envelope, drift)
    tampered = dict(record)
    tampered["audit_fingerprint"] = "0" * 64

    assert verify_audit_record_v0_1(tampered) is False
