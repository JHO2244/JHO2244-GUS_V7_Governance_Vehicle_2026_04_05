"""
GUS v7 — Phase 16
Cross-Case Reasoner (v0.1)

STRICT:
- Deterministic cross-case analysis only
- No inference
- No alteration of per-case results
- No probabilistic reasoning
- Pattern signals only from explicit batch outputs
"""

from __future__ import annotations

from gus_v7.routing.case_validator_router_v0_1 import (
    FAIL,
    INSUFFICIENT_EVIDENCE,
    PASS,
    ROUTER_ALLOWED_OUTPUTS_V0_1,
)
from gus_v7.routing.batch_evaluator_v0_1 import evaluate_case_batch_v0_1


def analyze_case_batch_v0_1(case_batch: tuple[dict, ...] | list[dict]) -> dict[str, tuple[str, ...]]:
    """
    Evaluate a batch and produce deterministic cross-case pattern signals.

    Contract:
    - batch_results preserves evaluation order exactly
    - conflict_flags contains explicit cross-case pattern markers
    - pattern_signals contains explicit batch-state markers
    - no per-case result is modified

    Fail-closed on:
    - impossible batch result contract drift
    """
    batch_results = evaluate_case_batch_v0_1(case_batch)

    if not isinstance(batch_results, tuple):
        return {
            "batch_results": (FAIL,),
            "conflict_flags": ("BATCH_RESULT_CONTRACT_DRIFT",),
            "pattern_signals": ("BATCH_RESULT_CONTRACT_DRIFT",),
        }

    if any(result not in ROUTER_ALLOWED_OUTPUTS_V0_1 for result in batch_results):
        return {
            "batch_results": (FAIL,),
            "conflict_flags": ("BATCH_RESULT_CONTRACT_DRIFT",),
            "pattern_signals": ("BATCH_RESULT_CONTRACT_DRIFT",),
        }

    conflict_flags: list[str] = []
    pattern_signals: list[str] = []

    fail_count = batch_results.count(FAIL)
    insufficient_count = batch_results.count(INSUFFICIENT_EVIDENCE)
    pass_count = batch_results.count(PASS)

    if fail_count >= 2:
        conflict_flags.append("REPEATED_FAIL_PATTERN")

    if insufficient_count >= 2:
        conflict_flags.append("REPEATED_INSUFFICIENT_EVIDENCE_PATTERN")

    distinct_results = set(batch_results)
    if len(distinct_results) >= 2:
        pattern_signals.append("MIXED_RESULT_BATCH")

    if pass_count == len(batch_results) and len(batch_results) > 0:
        pattern_signals.append("ALL_PASS_BATCH")
    elif fail_count == len(batch_results) and len(batch_results) > 0:
        pattern_signals.append("ALL_FAIL_BATCH")
    elif insufficient_count == len(batch_results) and len(batch_results) > 0:
        pattern_signals.append("ALL_INSUFFICIENT_EVIDENCE_BATCH")

    return {
        "batch_results": batch_results,
        "conflict_flags": tuple(conflict_flags),
        "pattern_signals": tuple(pattern_signals),
    }
