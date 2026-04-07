"""
GUS v7 — Phase 32
Chain Snapshot & Anchor Lock Tests (v0.1)

STRICT:
- Only valid full chain can be anchored
- Deterministic chain fingerprint
- Fail-closed on invalid chain
"""

from __future__ import annotations

from gus_v7.routing.execution_consistency_lock_v0_1 import (
    wrap_canonical_execution_output_v0_1,
    detect_execution_drift_v0_1,
    create_audit_record_v0_1,
    link_audit_record_v0_1,
    create_chain_anchor_v0_1,
    verify_chain_anchor_v0_1,
    ANCHOR_VALID,
    ANCHOR_INVALID,
)


def _make_record(output: str):
    envelope = wrap_canonical_execution_output_v0_1(output)
    drift = detect_execution_drift_v0_1(envelope, output)
    return create_audit_record_v0_1(envelope, drift)


def _make_chain():
    r1 = _make_record("PASS")
    r2 = _make_record("FAIL")
    r3 = _make_record("INSUFFICIENT_EVIDENCE")

    l1 = link_audit_record_v0_1(None, r1)
    l2 = link_audit_record_v0_1(r1, r2)
    l3 = link_audit_record_v0_1(r2, r3)

    return (l1, l2, l3)


def test_phase32_valid_anchor() -> None:
    chain = _make_chain()
    anchor = create_chain_anchor_v0_1(chain)

    assert anchor["anchor_status"] == ANCHOR_VALID
    assert verify_chain_anchor_v0_1(anchor, chain) is True


def test_phase32_deterministic_anchor_fingerprint() -> None:
    chain = _make_chain()

    a1 = create_chain_anchor_v0_1(chain)
    a2 = create_chain_anchor_v0_1(chain)

    assert a1["chain_fingerprint"] == a2["chain_fingerprint"]


def test_phase32_invalid_chain_fails_closed() -> None:
    anchor = create_chain_anchor_v0_1(("INVALID",))

    assert anchor["anchor_status"] == ANCHOR_INVALID


def test_phase32_tampered_anchor_fails() -> None:
    chain = _make_chain()
    anchor = create_chain_anchor_v0_1(chain)

    tampered = dict(anchor)
    tampered["chain_fingerprint"] = "0" * 64

    assert verify_chain_anchor_v0_1(tampered, chain) is False
