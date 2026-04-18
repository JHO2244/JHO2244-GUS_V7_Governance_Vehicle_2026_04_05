"""
GUS v7 - Phase 62
Cross-Machine Determinism (v0.1)

STRICT:
- Deterministic
- Byte-level comparison target
- No mutation
- No inference
- Fail-closed
"""

import json

from gus_v7.trace_integrity_lock.trace_integrity_lock_v0_1 import (
    lock_trace_integrity_v0_1,
)
from gus_v7.trace_to_governance_pipeline.trace_to_governance_pipeline_v0_1 import (
    apply_trace_to_governance_pipeline_v0_1,
)


def _trace() -> dict:
    return {
        "trace_id": "TRACE-062-CM-001",
        "decision_id": "DEC-062-CM-001",
        "case_id": "BC-062-CM-A",
        "evidence_binding_id": "EB-062-CM-001",
        "integrity_envelope_id": "IE-062-CM-001",
        "final_integrity_verdict": "INTEGRITY_CONFIRMED",
        "execution_result": "EXECUTE",
        "trace_timestamp": "2026-04-18T08:00:00Z",
        "trace_sequence": "0001",
    }


def _expected_capture_json() -> str:
    trace = _trace()
    capture = {
        "trace_fingerprint": lock_trace_integrity_v0_1(trace),
        "governance_result": apply_trace_to_governance_pipeline_v0_1(trace, ()),
    }
    return json.dumps(capture, sort_keys=True, separators=(",", ":"))


def test_phase62_capture_is_exact_expected_json():
    assert _expected_capture_json() == (
        '{"governance_result":"GOVERNANCE_PASS",'
        '"trace_fingerprint":"a0e85e615b10fdd8a8b459d582676389f4897d554cdfde83a9a6fe99ab00390e"}'
    )


def test_phase62_capture_is_stable_across_repeated_runs():
    assert _expected_capture_json() == _expected_capture_json()
    