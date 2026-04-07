"""
GUS v7 — Phase 25
Cross-Execution Consistency Lock (v0.1)

STRICT:
- Consistency proof layer only
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

    canonical_bytes = json.dumps(
        canonical_payload,
        ensure_ascii=True,
        separators=(",", ":"),
    ).encode("utf-8")

    return hashlib.sha256(canonical_bytes).hexdigest()
