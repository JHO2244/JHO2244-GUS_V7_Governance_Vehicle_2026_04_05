from gus_v7.routing.case_validator_router_v0_1 import route_and_validate_case
from gus_v7.validators.benchmark_case_01_validator_v0_1 import PASS, FAIL
from gus_v7.validators.benchmark_case_03_validator_v0_1 import INSUFFICIENT_EVIDENCE


def _build_bc01_case():
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


def _build_bc02_case():
    return {
        "case_id": "BC-02",
        "case_name": "Conflict-of-Interest Award",
        "case_version": "v0.1",
        "case_class": "benchmark_fail",
        "context": {
            "domain": "vendor_selection",
            "service_type": "logistics_services",
            "selection_scope": "region_y",
            "predeclared_requirement": True,
        },
        "agents": {
            "selecting_authority": "Agent_A",
            "candidate_vendors": ["Vendor_1", "Vendor_2", "Vendor_3"],
            "evaluation_mechanism": "Committee_B",
            "selected_vendor": "Vendor_1",
        },
        "process": [
            "requirement_defined",
            "criteria_defined",
            "vendor_pool_fixed",
            "conflict_present",
            "award_decision_logged",
        ],
        "evidence_pack": {
            "requirement_definition": {
                "id": "REQ-002",
                "description": "Provide logistics services for region Y",
                "timestamp": "T1",
            },
            "criteria_definition": [
                {"id": "C1", "description": "Cost efficiency"},
                {"id": "C2", "description": "Delivery reliability"},
                {"id": "C3", "description": "Service capacity"},
            ],
            "vendor_list": ["Vendor_1", "Vendor_2", "Vendor_3"],
            "conflict_disclosure": {
                "conflict_declared": True,
                "conflicted_party": "Agent_A",
                "relationship_to_selected_vendor": "family_tie",
            },
            "decision_record": {
                "selected_vendor": "Vendor_1",
                "basis": "conflicted_award",
                "timestamp": "T2",
            },
            "traceability_links": {
                "requirement_to_criteria": True,
                "criteria_to_decision": True,
                "conflict_to_decision": True,
                "chain_complete": True,
            },
        },
        "integrity_flags": {
            "criteria_predefined": True,
            "vendor_pool_fixed": True,
            "conflict_declared": True,
            "conflict_unresolved": True,
            "award_integrity_compromised": True,
        },
        "expected_output": "FAIL",
    }


def _build_bc03_case():
    return {
        "case_id": "BC-03",
        "case_name": "Cost-Cutting Unclear Impact",
        "case_version": "v0.1",
        "case_class": "benchmark_insufficient_evidence",
        "context": {
            "domain": "cost_management",
            "service_type": "infrastructure",
            "selection_scope": "region_z",
            "predeclared_requirement": True,
        },
        "agents": {
            "decision_authority": "Agent_X",
            "affected_units": ["Unit_1", "Unit_2"],
            "evaluation_mechanism": "Committee_Y",
        },
        "process": [
            "cost_pressure_identified",
            "reduction_option_defined",
            "impact_review_attempted",
            "decision_logged",
        ],
        "evidence_pack": {
            "cost_reduction_definition": {
                "id": "CR-001",
                "description": "Reduce maintenance budget",
                "timestamp": "T1",
            },
            "impact_assessment": {
                "assessment_present": True,
                "service_impact_evaluated": False,
                "safety_impact_evaluated": False,
                "continuity_impact_evaluated": False,
            },
            "decision_record": {
                "action_taken": "budget_reduction_applied",
                "basis": "incomplete_impact_evidence",
                "timestamp": "T2",
            },
            "traceability_links": {
                "cost_reduction_to_impact_review": True,
                "impact_review_to_decision": False,
                "chain_complete": False,
            },
        },
        "integrity_flags": {
            "evidence_incomplete": True,
            "impact_unknown": True,
            "decision_not_justified": True,
        },
        "expected_output": "INSUFFICIENT_EVIDENCE",
    }


def test_benchmark_pack_0_1_routes_all_three_anchor_cases_correctly() -> None:
    assert route_and_validate_case(_build_bc01_case()) == PASS
    assert route_and_validate_case(_build_bc02_case()) == FAIL
    assert route_and_validate_case(_build_bc03_case()) == INSUFFICIENT_EVIDENCE
