"""
GUS v7 — Phase 17
Ingestion Boundary (v0.1)

STRICT:
- Deterministic boundary only
- Fail-closed
- No inference
- No coercion
- No best-effort repair
- Reality must adapt to GUS
"""

from __future__ import annotations

from typing import Any

from gus_v7.routing.case_validator_router_v0_1 import FAIL


def ingest_case_payload_v0_1(payload: Any) -> dict[str, Any] | None:
    """
    Accept only canonical case payload dictionaries.

    Contract:
    - input must already be a dict
    - no string parsing
    - no field coercion
    - no key rewriting
    - no default injection
    - returns the payload unchanged when accepted

    Fail-closed on:
    - non-dict input
    - empty dict input
    - missing case_id
    - non-string case_id
    - empty case_id
    """
    if not isinstance(payload, dict):
        return None

    if len(payload) == 0:
        return None

    case_id = payload.get("case_id")
    if not isinstance(case_id, str) or not case_id:
        return None

    return payload


def ingest_case_batch_v0_1(payload_batch: Any) -> tuple[dict[str, Any], ...] | None:
    """
    Accept only canonical batches of already-structured case payloads.

    Contract:
    - input must be tuple or list
    - each member must pass ingest_case_payload_v0_1
    - preserves input order exactly
    - returns immutable tuple when accepted

    Fail-closed on:
    - invalid container
    - any invalid member
    """
    if not isinstance(payload_batch, (tuple, list)):
        return None

    accepted: list[dict[str, Any]] = []

    for payload in payload_batch:
        accepted_payload = ingest_case_payload_v0_1(payload)
        if accepted_payload is None:
            return None
        accepted.append(accepted_payload)

    return tuple(accepted)


def ingest_or_fail_result_v0_1(payload: Any) -> str:
    """
    Tiny helper for boundary-only fail-closed checks.

    Returns:
    - FAIL when payload is rejected by boundary
    - ACCEPTED when payload passes boundary
    """
    accepted = ingest_case_payload_v0_1(payload)
    if accepted is None:
        return FAIL
    return "ACCEPTED"
