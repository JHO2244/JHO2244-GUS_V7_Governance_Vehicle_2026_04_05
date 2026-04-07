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
