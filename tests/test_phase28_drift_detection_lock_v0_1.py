"""
GUS v7 — Phase 28
Drift Detection Lock Tests (v0.1)

STRICT:
- Detect no-drift vs drift deterministically
- Fail-closed on invalid baseline or replay
- No mutation of inputs
"""

from __future__ import annotations

from copy import deepcopy

from gus_v7.routing.batch_evaluator_v0_1 import evaluate_case_batch_v0_1
from gus_v7.routing.case_validator_router_v0_1 import route_and_validate_case
from gus_v7.routing.cross_case_reasoner_v0_1 import analyze_case_batch_v0_1
from gus_v7.routing.execution_consistency_lock_v0_1 import (
    detect_execution_drift_v0_1,
    wrap_canonical_execution_output_v0_1,
    NO_DRIFT,
    DRIFT_DETECTED,
    INVALID_BASELINE,
    INVALID_REPLAY,
)


def _build_bc01_case() -> dict:
    return {
        "case_id": "BC-01",
        "case_name": "Transparent Vendor Selection",
        "case_version": "v0.1",
        "case_class": "benchmark_pass",
        "context": {"domain": "vendor_selection"},
        "agents": {"selecting_authority": "Agent_A"},
        "process": [],
        "evidence_pack": {},
        "integrity_flags": {"criteria_predefined": True},
        "expected_output": "PASS",
    }


def test_phase28_no_drift_single_case() -> None:
    case = _build_bc01_case()
    baseline_case = deepcopy(case)

    output = route_and_validate_case(case)
    baseline_envelope = wrap_canonical_execution_output_v0_1(output)

    report = detect_execution_drift_v0_1(baseline_envelope, output)

    assert report["drift_status"] == NO_DRIFT
    assert case == baseline_case


def test_phase28_detects_drift_single_case() -> None:
    case = _build_bc01_case()

    output = route_and_validate_case(case)
    baseline_envelope = wrap_canonical_execution_output_v0_1(output)

    # simulate drift
    drifted_output = "PASS"

    report = detect_execution_drift_v0_1(baseline_envelope, drifted_output)

    assert report["drift_status"] == DRIFT_DETECTED


def test_phase28_invalid_baseline_fails_closed() -> None:
    report = detect_execution_drift_v0_1("INVALID", "PASS")
    assert report["drift_status"] == INVALID_BASELINE


def test_phase28_invalid_replay_fails_closed() -> None:
    baseline_envelope = wrap_canonical_execution_output_v0_1("PASS")
    report = detect_execution_drift_v0_1(baseline_envelope, ["PASS"])

    assert report["drift_status"] == INVALID_REPLAY


def test_phase28_batch_no_drift() -> None:
    batch = (_build_bc01_case(),)
    output = evaluate_case_batch_v0_1(batch)

    baseline_envelope = wrap_canonical_execution_output_v0_1(output)
    report = detect_execution_drift_v0_1(baseline_envelope, output)

    assert report["drift_status"] == NO_DRIFT


def test_phase28_cross_case_no_drift() -> None:
    batch = (_build_bc01_case(),)
    report_output = analyze_case_batch_v0_1(batch)

    baseline_envelope = wrap_canonical_execution_output_v0_1(report_output)
    report = detect_execution_drift_v0_1(baseline_envelope, report_output)

    assert report["drift_status"] == NO_DRIFT
