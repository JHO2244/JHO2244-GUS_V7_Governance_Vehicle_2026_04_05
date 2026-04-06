"""
GUS v7 — Phase 14
Batch Evaluation Engine (v0.1)

STRICT:
- Deterministic batch execution only
- Fail-closed
- No inference
- No fallback
- No aggregation logic
- Preserves input order exactly
"""

from __future__ import annotations

from typing import Any

from gus_v7.routing.case_validator_router_v0_1 import (
    FAIL,
    ROUTER_ALLOWED_OUTPUTS_V0_1,
    route_and_validate_case,
)


def evaluate_case_batch_v0_1(case_batch: tuple[dict, ...] | list[dict]) -> tuple[str, ...]:
    """
    Evaluate a batch of case objects deterministically through the canonical
    single-case router.

    Contract:
    - input must be a tuple or list
    - each element is passed to route_and_validate_case unchanged
    - output preserves input order exactly
    - output members must be router-approved outcomes only

    Fail-closed on:
    - invalid batch container type
    - impossible router output contract drift
    """
    if not isinstance(case_batch, (tuple, list)):
        return (FAIL,)

    results: list[str] = []

    for case_data in case_batch:
        result = route_and_validate_case(case_data)
        if result not in ROUTER_ALLOWED_OUTPUTS_V0_1:
            return (FAIL,)
        results.append(result)

    return tuple(results)

