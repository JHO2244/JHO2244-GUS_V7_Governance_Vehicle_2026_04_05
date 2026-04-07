"""
GUS v7 — Phase 23
Execution Path Isolation Lock Tests (v0.1)

STRICT:
- Deterministic
- Fail-closed
- No execution-path leakage
- Batch path must not delegate to single-case router
"""

from __future__ import annotations

import pytest

from gus_v7.routing.batch_evaluator_v0_1 import evaluate_case_batch_v0_1
from gus_v7.routing.case_validator_router_v0_1 import FAIL


def _build_bc01_case() -> dict:
    return {
        "case_id": "BC-01",
        "case_name": "Transparent Vendor Selection",
        "case_version": "v0.1",
        "case_class": "benchmark_pass",
        "context": {
            "domain": "vendor_selection",
            "service_type": "logistics_services",
            "selection_scope": "region_x",
            "predeclared_requirement": True,
        },
        "agents": {
            "selecting_authority": "Agent_A",
            "candidate_vendors": ["Vendor_1", "Vendor_2", "Vendor_3"],
            "evaluation_mechanism": "Agent_C",
        },
        "process": [
            "requirement_defined",
            "criteria_defined",
            "vendor_pool_fixed",
            "uniform_evaluation_executed",
            "evidence_recorded",
            "decision_logged",
        ],
        "evidence_pack": {
            "requirement_definition": {
                "id": "REQ-001",
                "description": "Provide logistics services for region X",
                "timestamp": "T1",
            },
            "criteria_definition": [
                {"id": "C1", "description": "Cost efficiency"},
                {"id": "C2", "description": "Delivery reliability"},
                {"id": "C3", "description": "Service capacity"},
            ],
            "vendor_list": ["Vendor_1", "Vendor_2", "Vendor_3"],
            "evaluation_records": [
                {
                    "vendor_id": "Vendor_1",
                    "criteria_results": {"C1": "ok", "C2": "ok", "C3": "ok"},
                    "evidence_refs": ["E1"],
                },
                {
                    "vendor_id": "Vendor_2",
                    "criteria_results": {"C1": "ok", "C2": "ok", "C3": "ok"},
                    "evidence_refs": ["E2"],
                },
                {
                    "vendor_id": "Vendor_3",
                    "criteria_results": {"C1": "ok", "C2": "ok", "C3": "ok"},
                    "evidence_refs": ["E3"],
                },
            ],
            "decision_record": {
                "selected_vendor": "Vendor_1",
                "basis": "criteria_output_alignment",
                "timestamp": "T2",
            },
            "traceability_links": {
                "requirement_to_criteria": True,
                "criteria_to_evaluations": True,
                "evaluations_to_decision": True,
                "chain_complete": True,
            },
        },
        "integrity_flags": {
            "criteria_predefined": True,
            "uniform_evaluation": True,
            "evidence_present": True,
            "traceability_complete": True,
            "no_external_influence": True,
        },
        "expected_output": "PASS",
    }


def test_phase23_batch_path_rejects_single_dict_at_batch_boundary() -> None:
    assert evaluate_case_batch_v0_1(_build_bc01_case()) == (FAIL,)


def test_phase23_batch_path_still_accepts_tuple_batch() -> None:
    batch = (_build_bc01_case(), _build_bc01_case())
    result = evaluate_case_batch_v0_1(batch)

    assert isinstance(result, tuple)
    assert len(result) == 2


def test_phase23_batch_path_does_not_delegate_to_single_case_router(monkeypatch) -> None:
    def explode(_case_data):
        raise AssertionError("batch path leaked into single-case router")

    monkeypatch.setattr(
        "gus_v7.routing.batch_evaluator_v0_1.route_and_validate_case",
        explode,
        raising=False,
    )

    batch = (_build_bc01_case(),)
    result = evaluate_case_batch_v0_1(batch)

    assert result != (FAIL,) or result == ("PASS",)
