"""
GUS v7 — Phase 21
Intake to Core Execution Contract Lock (v0.1)

STRICT:
- Contract-only layer
- No routing logic
- No mutation
- No inference
- No fallback
- No boundary re-validation
"""

from __future__ import annotations

from typing import Any


def accept_execution_contract_v0_1(
    accepted_payload: Any,
) -> dict[str, Any] | tuple[dict[str, Any], ...] | None:
    """
    Accept only canonical Phase 20 payload outputs for execution entry.

    Contract:
    - dict = single-case execution contract
    - tuple = batch execution contract
    - payload is returned unchanged when accepted

    Fail-closed on:
    - any non-dict, non-tuple input
    """
    if isinstance(accepted_payload, dict):
        return accepted_payload

    if isinstance(accepted_payload, tuple):
        return accepted_payload

    return None
