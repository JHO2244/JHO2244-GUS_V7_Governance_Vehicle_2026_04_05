"""
GUS v7 — Phase 30
Audit Chain Linking Tests (v0.1)

STRICT:
- Deterministic chain linking
- Tamper detection via fingerprint mismatch
- Fail-closed on invalid records
"""

from __future__ import annotations

from gus_v7.routing.case_validator_router_v0_1 import route_and_validate_case
from gus_v7.routing.execution_consistency_lock_v0_1 import (
    wrap_canonical_execution_output_v0_1,
    detect_execution_drift_v0_1,
    create_audit_record_v0_1,
    verify_audit_record_v0_1,
    link_audit_record_v0_1,
    verify_audit_chain_link_v0_1,
)


def _build_case() -> dict:
    return {
        "case_id": "BC-01",
        "case_name": "Chain Case",
        "case_version": "v0.1",
        "case_class": "benchmark_pass",
        "context": {"domain": "test"},
        "agents": {"a": "A"},
        "process": [],
        "evidence_pack": {},
        "integrity_flags": {"criteria_predefined": True},
        "expected_output": "PASS",
    }


def _make_record():
    case = _build_case()
    output = route_and_validate_case(case)
    envelope = wrap_canonical_execution_output_v0_1(output)
    drift = detect_execution_drift_v0_1(envelope, output)
    record = create_audit_record_v0_1(envelope, drift)
    assert verify_audit_record_v0_1(record)
    return record


def test_phase30_chain_root_creation() -> None:
    record = _make_record()
    link = link_audit_record_v0_1(None, record)

    assert link is not None
    assert verify_audit_chain_link_v0_1(link) is True


def test_phase30_chain_linking_two_records() -> None:
    r1 = _make_record()
    r2 = _make_record()

    link = link_audit_record_v0_1(r1, r2)

    assert link is not None
    assert verify_audit_chain_link_v0_1(link) is True


def test_phase30_tampered_chain_fingerprint_fails() -> None:
    r = _make_record()
    link = link_audit_record_v0_1(None, r)

    tampered = dict(link)
    tampered["chain_fingerprint"] = "0" * 64

    assert verify_audit_chain_link_v0_1(tampered) is False


def test_phase30_invalid_current_record_fails_closed() -> None:
    link = link_audit_record_v0_1(None, "INVALID")
    assert link is None


def test_phase30_invalid_previous_record_fails_closed() -> None:
    r = _make_record()
    link = link_audit_record_v0_1("INVALID", r)

    assert link is None
