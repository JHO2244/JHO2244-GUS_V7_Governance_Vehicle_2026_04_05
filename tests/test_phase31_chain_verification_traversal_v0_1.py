"""
GUS v7 — Phase 31
Chain Verification Traversal Tests (v0.1)

STRICT:
- Verify full chain integrity
- Detect broken sequence or invalid link
- Fail-closed behavior
"""

from __future__ import annotations

from gus_v7.routing.execution_consistency_lock_v0_1 import (
    wrap_canonical_execution_output_v0_1,
    detect_execution_drift_v0_1,
    create_audit_record_v0_1,
    link_audit_record_v0_1,
    verify_audit_chain_sequence_v0_1,
    CHAIN_VALID,
    CHAIN_INVALID,
)


def _make_record(execution_output: str):
    envelope = wrap_canonical_execution_output_v0_1(execution_output)
    drift = detect_execution_drift_v0_1(envelope, execution_output)
    return create_audit_record_v0_1(envelope, drift)


def test_phase31_valid_chain() -> None:
    r1 = _make_record("PASS")
    r2 = _make_record("FAIL")
    r3 = _make_record("INSUFFICIENT_EVIDENCE")

    l1 = link_audit_record_v0_1(None, r1)
    l2 = link_audit_record_v0_1(r1, r2)
    l3 = link_audit_record_v0_1(r2, r3)

    report = verify_audit_chain_sequence_v0_1((l1, l2, l3))

    assert report["chain_status"] == CHAIN_VALID
    assert report["verified_link_count"] == 3


def test_phase31_invalid_root_fails() -> None:
    r1 = _make_record("PASS")
    r2 = _make_record("FAIL")

    l1 = link_audit_record_v0_1(r1, r2)

    report = verify_audit_chain_sequence_v0_1((l1,))

    assert report["chain_status"] == CHAIN_INVALID


def test_phase31_broken_sequence_fails() -> None:
    r1 = _make_record("PASS")
    r2 = _make_record("FAIL")
    r3 = _make_record("INSUFFICIENT_EVIDENCE")

    l1 = link_audit_record_v0_1(None, r1)
    l2 = link_audit_record_v0_1(r1, r2)
    l3 = link_audit_record_v0_1(r1, r3)

    report = verify_audit_chain_sequence_v0_1((l1, l2, l3))

    assert report["chain_status"] == CHAIN_INVALID


def test_phase31_invalid_link_fails() -> None:
    report = verify_audit_chain_sequence_v0_1(("INVALID",))

    assert report["chain_status"] == CHAIN_INVALID


def test_phase31_empty_chain_fails() -> None:
    report = verify_audit_chain_sequence_v0_1(())

    assert report["chain_status"] == CHAIN_INVALID
