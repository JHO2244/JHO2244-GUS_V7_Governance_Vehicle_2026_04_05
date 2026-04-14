from copy import deepcopy

from gus_v7.decision_execution_gate.decision_execution_gate_v0_1 import (
    apply_decision_execution_gate_v0_1,
)
from gus_v7.drift_detection.drift_detection_v0_1 import detect_drift_v0_1


def _validated_envelope() -> dict:
    return {
        "decision": {
            "decision_id": "DEC-014-001",
            "case_id": "BC-01",
            "decision_output": "PASS",
        },
        "integrity_result": "VALID",
        "consistency_result": "CONSISTENT",
        "trace_result": "LINKED",
        "replay_result": "DETERMINISTIC",
        "final_integrity_verdict": "INTEGRITY_CONFIRMED",
        "immutable_after_creation": True,
    }


def _baseline_reconstruction() -> dict:
    return {
        "trace_id": "TRACE-014-001",
        "decision_id": "DEC-014-001",
        "case_id": "BC-01",
        "evidence_binding_id": "EB-014-001",
        "integrity_envelope_id": "IE-014-001",
        "final_integrity_verdict": "INTEGRITY_CONFIRMED",
        "execution_result": "EXECUTE",
        "trace_timestamp": "2026-04-14T12:00:00Z",
        "trace_sequence": "0001",
        "reconstructed_path": (
            "decision_id=DEC-014-001"
            "|case_id=BC-01"
            "|evidence_binding_id=EB-014-001"
            "|integrity_envelope_id=IE-014-001"
            "|final_integrity_verdict=INTEGRITY_CONFIRMED"
            "|execution_result=EXECUTE"
            "|trace_id=TRACE-014-001"
            "|trace_timestamp=2026-04-14T12:00:00Z"
            "|trace_sequence=0001"
        ),
    }


def test_attack014_execution_gate_still_allows_execute_after_candidate_drift_injection():
    envelope = _validated_envelope()
    drifted_candidate = _baseline_reconstruction()
    drifted_candidate["execution_result"] = "BLOCK"
    drifted_candidate["reconstructed_path"] = drifted_candidate["reconstructed_path"].replace(
        "execution_result=EXECUTE",
        "execution_result=BLOCK",
    )

    assert apply_decision_execution_gate_v0_1(envelope) == "EXECUTE"


def test_attack014_drift_detection_detects_post_validation_execution_drift():
    baseline = _baseline_reconstruction()
    candidate = deepcopy(baseline)
    candidate["execution_result"] = "BLOCK"
    candidate["reconstructed_path"] = candidate["reconstructed_path"].replace(
        "execution_result=EXECUTE",
        "execution_result=BLOCK",
    )

    assert detect_drift_v0_1(baseline, candidate) == "DRIFT_DETECTED"


def test_attack014_execution_permission_is_not_bound_to_drift_check():
    envelope = _validated_envelope()
    baseline = _baseline_reconstruction()
    candidate = deepcopy(baseline)
    candidate["final_integrity_verdict"] = "INTEGRITY_REJECTED"
    candidate["reconstructed_path"] = candidate["reconstructed_path"].replace(
        "final_integrity_verdict=INTEGRITY_CONFIRMED",
        "final_integrity_verdict=INTEGRITY_REJECTED",
    )

    assert apply_decision_execution_gate_v0_1(envelope) == "EXECUTE"
    assert detect_drift_v0_1(baseline, candidate) == "DRIFT_DETECTED"
