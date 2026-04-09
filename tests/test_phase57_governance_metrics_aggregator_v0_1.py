"""
GUS v7 — Phase 57
Governance Metrics Aggregator Tests (v0.1)

STRICT:
- Validate deterministic aggregation only
- No inference
- Fail-closed enforcement
"""

from gus_v7.governance_metrics.governance_metrics_aggregator_v0_1 import (
    aggregate_governance_metrics_v0_1,
)


def _valid_entries():
    return [
        {
            "decision_id": "DEC-001",
            "execution_result": "EXECUTE",
            "final_integrity_verdict": "INTEGRITY_CONFIRMED",
            "governance_result": "GOVERNANCE_PASS",
        },
        {
            "decision_id": "DEC-002",
            "execution_result": "BLOCK",
            "final_integrity_verdict": "INTEGRITY_REJECTED",
            "governance_result": "GOVERNANCE_PASS",
        },
        {
            "decision_id": "DEC-003",
            "execution_result": "EXECUTE",
            "final_integrity_verdict": "INTEGRITY_CONFIRMED",
            "governance_result": "GOVERNANCE_FAIL",
        },
    ]


def test_phase57_aggregator_accepts_valid_entries():
    result = aggregate_governance_metrics_v0_1(_valid_entries())
    assert result == {
        "total_decisions": 3,
        "execute_count": 2,
        "block_count": 1,
        "integrity_confirmed_count": 2,
        "integrity_rejected_count": 1,
        "governance_pass_count": 2,
        "governance_fail_count": 1,
    }


def test_phase57_aggregator_rejects_empty_input():
    try:
        aggregate_governance_metrics_v0_1([])
        assert False
    except ValueError as exc:
        assert str(exc) == "INVALID_INPUT"


def test_phase57_aggregator_rejects_non_list_input():
    try:
        aggregate_governance_metrics_v0_1("not-a-list")
        assert False
    except ValueError as exc:
        assert str(exc) == "INVALID_INPUT"


def test_phase57_aggregator_rejects_missing_field():
    entries = _valid_entries()
    del entries[0]["governance_result"]
    try:
        aggregate_governance_metrics_v0_1(entries)
        assert False
    except ValueError as exc:
        assert str(exc) == "INVALID_ENTRY"


def test_phase57_aggregator_rejects_extra_field():
    entries = _valid_entries()
    entries[0]["extra"] = "not allowed"
    try:
        aggregate_governance_metrics_v0_1(entries)
        assert False
    except ValueError as exc:
        assert str(exc) == "INVALID_ENTRY"


def test_phase57_aggregator_rejects_invalid_execution_result():
    entries = _valid_entries()
    entries[0]["execution_result"] = "ALLOW"
    try:
        aggregate_governance_metrics_v0_1(entries)
        assert False
    except ValueError as exc:
        assert str(exc) == "INVALID_ENTRY"


def test_phase57_aggregator_rejects_invalid_integrity_verdict():
    entries = _valid_entries()
    entries[0]["final_integrity_verdict"] = "UNKNOWN"
    try:
        aggregate_governance_metrics_v0_1(entries)
        assert False
    except ValueError as exc:
        assert str(exc) == "INVALID_ENTRY"


def test_phase57_aggregator_rejects_invalid_governance_result():
    entries = _valid_entries()
    entries[0]["governance_result"] = "MAYBE"
    try:
        aggregate_governance_metrics_v0_1(entries)
        assert False
    except ValueError as exc:
        assert str(exc) == "INVALID_ENTRY"
