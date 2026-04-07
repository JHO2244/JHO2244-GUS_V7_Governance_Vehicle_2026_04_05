"""
GUS v7 — Phase 22
Router Entry Contract Enforcement Tests (v0.1)

STRICT:
- Deterministic
- Fail-closed
- No fallback
- No inference
- Enforce Phase 21 contract at router entry
"""

from __future__ import annotations

from gus_v7.routing.case_validator_router_v0_1 import FAIL, PASS, route_and_validate_case


def _build_valid_router_pass_case() -> dict:
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


def test_phase22_router_accepts_valid_single_case_dict() -> None:
    assert route_and_validate_case(_build_valid_router_pass_case()) == PASS


def test_phase22_router_rejects_batch_tuple_at_single_case_boundary() -> None:
    batch = (_build_valid_router_pass_case(), _build_valid_router_pass_case())
    assert route_and_validate_case(batch) == FAIL


def test_phase22_router_rejects_list_fail_closed() -> None:
    payload = [_build_valid_router_pass_case()]
    assert route_and_validate_case(payload) == FAIL


def test_phase22_router_rejects_string_fail_closed() -> None:
    assert route_and_validate_case("not_valid") == FAIL


def test_phase22_router_rejects_none_fail_closed() -> None:
    assert route_and_validate_case(None) == FAIL
