"""
GUS v7 — Phases 25-28
Cross-Execution Consistency Lock, Canonical Output Fingerprint Lock,
Replay Verification System, and Drift Detection Lock (v0.1)

STRICT:
- Consistency proof layer only
- Canonical envelope layer only
- Replay verification layer only
- Drift detection layer only
- No execution logic changes
- No inference
- No mutation
- No fallback
- Canonical fingerprinting only
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

from gus_v7.routing.case_validator_router_v0_1 import ROUTER_ALLOWED_OUTPUTS_V0_1


CROSS_CASE_REPORT_KEYS_V0_1 = (
    "batch_results",
    "conflict_flags",
    "pattern_signals",
)

CANONICAL_OUTPUT_ENVELOPE_KEYS_V0_1 = (
    "execution_type",
    "execution_output",
    "execution_fingerprint",
)

DRIFT_REPORT_KEYS_V0_1 = (
    "drift_status",
    "baseline_envelope",
    "replayed_envelope",
)


NO_DRIFT = "NO_DRIFT"
DRIFT_DETECTED = "DRIFT_DETECTED"
INVALID_BASELINE = "INVALID_BASELINE"
INVALID_REPLAY = "INVALID_REPLAY"


def _is_allowed_router_output_v0_1(value: Any) -> bool:
    return value in ROUTER_ALLOWED_OUTPUTS_V0_1


def _is_allowed_output_tuple_v0_1(value: Any) -> bool:
    return isinstance(value, tuple) and all(
        _is_allowed_router_output_v0_1(item) for item in value
    )


def _is_valid_cross_case_report_v0_1(value: Any) -> bool:
    if not isinstance(value, dict):
        return False

    if tuple(value.keys()) != CROSS_CASE_REPORT_KEYS_V0_1:
        return False

    batch_results = value.get("batch_results")
    conflict_flags = value.get("conflict_flags")
    pattern_signals = value.get("pattern_signals")

    if not _is_allowed_output_tuple_v0_1(batch_results):
        return False

    if not isinstance(conflict_flags, tuple) or not all(
        isinstance(item, str) for item in conflict_flags
    ):
        return False

    if not isinstance(pattern_signals, tuple) or not all(
        isinstance(item, str) for item in pattern_signals
    ):
        return False

    return True


def _to_canonical_execution_payload_v0_1(
    execution_output: Any,
) -> dict[str, Any] | None:
    if _is_allowed_router_output_v0_1(execution_output):
        return {
            "execution_type": "single_case",
            "execution_output": execution_output,
        }

    if _is_allowed_output_tuple_v0_1(execution_output):
        return {
            "execution_type": "batch_case",
            "execution_output": execution_output,
        }

    if _is_valid_cross_case_report_v0_1(execution_output):
        return {
            "execution_type": "cross_case_report",
            "execution_output": execution_output,
        }

    return None


def _canonicalize_execution_payload_bytes_v0_1(
    canonical_payload: dict[str, Any],
) -> bytes:
    return json.dumps(
        canonical_payload,
        ensure_ascii=True,
        separators=(",", ":"),
    ).encode("utf-8")


def fingerprint_execution_output_v0_1(execution_output: Any) -> str | None:
    """
    Produce a deterministic fingerprint for a canonical execution output.

    Accepted execution-output contracts:
    - PASS / FAIL / INSUFFICIENT_EVIDENCE
    - tuple of router-approved outputs
    - exact cross-case report dict with tuple-valued fields

    Fail-closed on:
    - unsupported output shape
    - non-canonical cross-case report structure
    """
    canonical_payload = _to_canonical_execution_payload_v0_1(execution_output)
    if canonical_payload is None:
        return None

    canonical_bytes = _canonicalize_execution_payload_bytes_v0_1(canonical_payload)
    return hashlib.sha256(canonical_bytes).hexdigest()


def wrap_canonical_execution_output_v0_1(
    execution_output: Any,
) -> dict[str, Any] | None:
    """
    Wrap a canonical execution output inside a deterministic output envelope.

    Envelope contract:
    - execution_type
    - execution_output
    - execution_fingerprint

    Fail-closed on:
    - unsupported output shape
    - fingerprint generation failure
    """
    canonical_payload = _to_canonical_execution_payload_v0_1(execution_output)
    if canonical_payload is None:
        return None

    fingerprint = fingerprint_execution_output_v0_1(execution_output)
    if fingerprint is None:
        return None

    return {
        "execution_type": canonical_payload["execution_type"],
        "execution_output": canonical_payload["execution_output"],
        "execution_fingerprint": fingerprint,
    }


def verify_canonical_execution_output_envelope_v0_1(envelope: Any) -> bool:
    """
    Verify that a canonical output envelope is structurally valid and that the
    embedded fingerprint matches the embedded execution output exactly.
    """
    if not isinstance(envelope, dict):
        return False

    if tuple(envelope.keys()) != CANONICAL_OUTPUT_ENVELOPE_KEYS_V0_1:
        return False

    execution_type = envelope.get("execution_type")
    execution_output = envelope.get("execution_output")
    execution_fingerprint = envelope.get("execution_fingerprint")

    if not isinstance(execution_type, str) or not execution_type:
        return False

    if not isinstance(execution_fingerprint, str) or not execution_fingerprint:
        return False

    expected_envelope = wrap_canonical_execution_output_v0_1(execution_output)
    if expected_envelope is None:
        return False

    return envelope == expected_envelope


def verify_replayed_execution_output_v0_1(
    baseline_envelope: Any,
    replayed_execution_output: Any,
) -> bool:
    """
    Verify that a replayed execution output reproduces the exact same canonical
    output envelope as the baseline envelope.

    Fail-closed on:
    - invalid baseline envelope
    - invalid replayed execution output
    - any envelope mismatch
    """
    if not verify_canonical_execution_output_envelope_v0_1(baseline_envelope):
        return False

    replayed_envelope = wrap_canonical_execution_output_v0_1(
        replayed_execution_output
    )
    if replayed_envelope is None:
        return False

    return baseline_envelope == replayed_envelope


def detect_execution_drift_v0_1(
    baseline_envelope: Any,
    replayed_execution_output: Any,
) -> dict[str, Any]:
    """
    Detect deterministic drift between a baseline canonical envelope and a
    replayed execution output.

    Drift report contract:
    - drift_status
    - baseline_envelope
    - replayed_envelope

    Fail-closed statuses:
    - INVALID_BASELINE
    - INVALID_REPLAY
    """
    if not verify_canonical_execution_output_envelope_v0_1(baseline_envelope):
        return {
            "drift_status": INVALID_BASELINE,
            "baseline_envelope": None,
            "replayed_envelope": None,
        }

    replayed_envelope = wrap_canonical_execution_output_v0_1(
        replayed_execution_output
    )
    if replayed_envelope is None:
        return {
            "drift_status": INVALID_REPLAY,
            "baseline_envelope": baseline_envelope,
            "replayed_envelope": None,
        }

    if baseline_envelope == replayed_envelope:
        return {
            "drift_status": NO_DRIFT,
            "baseline_envelope": baseline_envelope,
            "replayed_envelope": replayed_envelope,
        }

    return {
        "drift_status": DRIFT_DETECTED,
        "baseline_envelope": baseline_envelope,
        "replayed_envelope": replayed_envelope,
    }

# =========================
# Phase 29 — Audit Record
# =========================

AUDIT_RECORD_KEYS_V0_1 = (
    "audit_status",
    "envelope",
    "drift_status",
    "audit_fingerprint",
)

AUDIT_VALID = "AUDIT_VALID"
AUDIT_INVALID = "AUDIT_INVALID"


def _canonicalize_audit_payload_bytes_v0_1(payload: dict[str, Any]) -> bytes:
    return json.dumps(
        payload,
        ensure_ascii=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _fingerprint_audit_payload_v0_1(payload: dict[str, Any]) -> str:
    return hashlib.sha256(
        _canonicalize_audit_payload_bytes_v0_1(payload)
    ).hexdigest()


def create_audit_record_v0_1(
    envelope: Any,
    drift_report: Any,
) -> dict[str, Any]:
    """
    Create a deterministic audit record from a verified envelope and drift report.

    Contract:
    - envelope must pass Phase 26 verification
    - drift_report must match Phase 28 structure

    Output:
    - audit_status
    - envelope
    - drift_status
    - audit_fingerprint

    Fail-closed:
    - invalid envelope
    - invalid drift report
    """
    if not verify_canonical_execution_output_envelope_v0_1(envelope):
        return {
            "audit_status": AUDIT_INVALID,
            "envelope": None,
            "drift_status": None,
            "audit_fingerprint": None,
        }

    if not isinstance(drift_report, dict):
        return {
            "audit_status": AUDIT_INVALID,
            "envelope": envelope,
            "drift_status": None,
            "audit_fingerprint": None,
        }

    drift_status = drift_report.get("drift_status")
    if drift_status not in (
        NO_DRIFT,
        DRIFT_DETECTED,
        INVALID_BASELINE,
        INVALID_REPLAY,
    ):
        return {
            "audit_status": AUDIT_INVALID,
            "envelope": envelope,
            "drift_status": None,
            "audit_fingerprint": None,
        }

    audit_payload = {
        "envelope": envelope,
        "drift_status": drift_status,
    }

    audit_fingerprint = _fingerprint_audit_payload_v0_1(audit_payload)

    return {
        "audit_status": AUDIT_VALID,
        "envelope": envelope,
        "drift_status": drift_status,
        "audit_fingerprint": audit_fingerprint,
    }


def verify_audit_record_v0_1(record: Any) -> bool:
    """
    Verify deterministic integrity of an audit record.
    """
    if not isinstance(record, dict):
        return False

    if tuple(record.keys()) != AUDIT_RECORD_KEYS_V0_1:
        return False

    if record.get("audit_status") != AUDIT_VALID:
        return False

    envelope = record.get("envelope")
    drift_status = record.get("drift_status")
    fingerprint = record.get("audit_fingerprint")

    if not verify_canonical_execution_output_envelope_v0_1(envelope):
        return False

    if drift_status not in (
        NO_DRIFT,
        DRIFT_DETECTED,
        INVALID_BASELINE,
        INVALID_REPLAY,
    ):
        return False

    expected = create_audit_record_v0_1(
        envelope,
        {"drift_status": drift_status},
    )

    if expected.get("audit_fingerprint") != fingerprint:
        return False

    return True

# =========================
# Phase 30 — Audit Chain Linking
# =========================

AUDIT_CHAIN_LINK_KEYS_V0_1 = (
    "previous_audit_fingerprint",
    "current_audit_record",
    "chain_fingerprint",
)


def _canonicalize_chain_payload_bytes_v0_1(payload: dict[str, Any]) -> bytes:
    return json.dumps(
        payload,
        ensure_ascii=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _fingerprint_chain_payload_v0_1(payload: dict[str, Any]) -> str:
    return hashlib.sha256(
        _canonicalize_chain_payload_bytes_v0_1(payload)
    ).hexdigest()


def link_audit_record_v0_1(
    previous_audit_record: Any,
    current_audit_record: Any,
) -> dict[str, Any] | None:
    """
    Link a verified current audit record to an optional verified previous audit
    record, producing a deterministic tamper-evident chain link.

    Contract:
    - previous_audit_record may be None (chain root)
    - current_audit_record must be a valid Phase 29 audit record

    Output:
    - previous_audit_fingerprint
    - current_audit_record
    - chain_fingerprint

    Fail-closed:
    - invalid previous audit record
    - invalid current audit record
    """
    if previous_audit_record is not None:
        if not verify_audit_record_v0_1(previous_audit_record):
            return None
        previous_audit_fingerprint = previous_audit_record["audit_fingerprint"]
    else:
        previous_audit_fingerprint = None

    if not verify_audit_record_v0_1(current_audit_record):
        return None

    chain_payload = {
        "previous_audit_fingerprint": previous_audit_fingerprint,
        "current_audit_record": current_audit_record,
    }

    chain_fingerprint = _fingerprint_chain_payload_v0_1(chain_payload)

    return {
        "previous_audit_fingerprint": previous_audit_fingerprint,
        "current_audit_record": current_audit_record,
        "chain_fingerprint": chain_fingerprint,
    }


def verify_audit_chain_link_v0_1(link: Any) -> bool:
    """
    Verify deterministic integrity of an audit chain link.
    """
    if not isinstance(link, dict):
        return False

    if tuple(link.keys()) != AUDIT_CHAIN_LINK_KEYS_V0_1:
        return False

    previous_audit_fingerprint = link.get("previous_audit_fingerprint")
    current_audit_record = link.get("current_audit_record")
    chain_fingerprint = link.get("chain_fingerprint")

    if previous_audit_fingerprint is not None and not isinstance(
        previous_audit_fingerprint, str
    ):
        return False

    if not isinstance(chain_fingerprint, str) or not chain_fingerprint:
        return False

    if not verify_audit_record_v0_1(current_audit_record):
        return False

    expected = link_audit_record_v0_1(None, current_audit_record)
    if previous_audit_fingerprint is not None:
        synthetic_previous = dict(current_audit_record)
        synthetic_previous["audit_fingerprint"] = previous_audit_fingerprint
        expected_payload = {
            "previous_audit_fingerprint": previous_audit_fingerprint,
            "current_audit_record": current_audit_record,
        }
        expected_chain_fingerprint = _fingerprint_chain_payload_v0_1(
            expected_payload
        )
        return chain_fingerprint == expected_chain_fingerprint

    return expected is not None and link == expected

# =========================
# Phase 31 — Chain Verification Traversal
# =========================

CHAIN_TRAVERSAL_REPORT_KEYS_V0_1 = (
    "chain_status",
    "verified_link_count",
)

CHAIN_VALID = "CHAIN_VALID"
CHAIN_INVALID = "CHAIN_INVALID"


def verify_audit_chain_sequence_v0_1(chain_links: Any) -> dict[str, Any]:
    """
    Verify a full ordered audit chain from root to latest.

    Contract:
    - chain_links must be a tuple of Phase 30 chain links
    - first link must be a root link (previous_audit_fingerprint is None)
    - each next link must reference the previous link's current audit fingerprint

    Output:
    - chain_status
    - verified_link_count

    Fail-closed on:
    - invalid container
    - empty chain
    - invalid link
    - broken fingerprint sequence
    """
    if not isinstance(chain_links, tuple) or len(chain_links) == 0:
        return {
            "chain_status": CHAIN_INVALID,
            "verified_link_count": 0,
        }

    verified_count = 0
    expected_previous_fingerprint = None

    for index, link in enumerate(chain_links):
        if not verify_audit_chain_link_v0_1(link):
            return {
                "chain_status": CHAIN_INVALID,
                "verified_link_count": verified_count,
            }

        actual_previous_fingerprint = link["previous_audit_fingerprint"]
        current_audit_record = link["current_audit_record"]
        current_audit_fingerprint = current_audit_record["audit_fingerprint"]

        if index == 0:
            if actual_previous_fingerprint is not None:
                return {
                    "chain_status": CHAIN_INVALID,
                    "verified_link_count": verified_count,
                }
        else:
            if actual_previous_fingerprint != expected_previous_fingerprint:
                return {
                    "chain_status": CHAIN_INVALID,
                    "verified_link_count": verified_count,
                }

        verified_count += 1
        expected_previous_fingerprint = current_audit_fingerprint

    return {
        "chain_status": CHAIN_VALID,
        "verified_link_count": verified_count,
    }
