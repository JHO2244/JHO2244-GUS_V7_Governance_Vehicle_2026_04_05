"""
GUS v7 — Phase 12
Benchmark Case 03 Validator Tests (v0.1)

STRICT:
- Deterministic
- PASS / FAIL / INSUFFICIENT_EVIDENCE only
- Canonical insufficient-evidence benchmark
"""

from gus_v7.validators.benchmark_case_03_validator_v0_1 import (
    FAIL,
    INSUFFICIENT_EVIDENCE,
    validate_benchmark_case_03,
)


def _build_valid_case():
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


def test_phase12_canonical_bc03_case_returns_insufficient():
    case = _build_valid_case()
    assert validate_benchmark_case_03(case) == INSUFFICIENT_EVIDENCE


def test_phase12_fail_wrong_case_id():
    case = _build_valid_case()
    case["case_id"] = "WRONG"
    assert validate_benchmark_case_03(case) == FAIL


def test_phase12_fail_missing_impact_assessment():
    case = _build_valid_case()
    del case["evidence_pack"]["impact_assessment"]
    assert validate_benchmark_case_03(case) == FAIL


def test_phase12_fail_process_order():
    case = _build_valid_case()
    case["process"][0], case["process"][1] = case["process"][1], case["process"][0]
    assert validate_benchmark_case_03(case) == FAIL


def test_phase12_fail_traceability_break():
    case = _build_valid_case()
    case["evidence_pack"]["traceability_links"]["chain_complete"] = True
    assert validate_benchmark_case_03(case) == FAIL


def test_phase12_fail_integrity_flag_break():
    case = _build_valid_case()
    case["integrity_flags"]["impact_unknown"] = False
    assert validate_benchmark_case_03(case) == FAIL
