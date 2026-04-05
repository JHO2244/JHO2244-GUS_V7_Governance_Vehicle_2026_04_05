"""
GUS v7 — Phase 12
Benchmark Case 03 Validator (v0.1)

STRICT:
- Deterministic
- Fail-closed
- No scoring
- No inference
- PASS / FAIL / INSUFFICIENT_EVIDENCE only
"""

from __future__ import annotations

from gus_v7.cases.benchmark_case_03_schema_v0_1 import (
    AGENTS_KEYS,
    CASE_CLASS,
    CASE_ID,
    CASE_NAME,
    CASE_VERSION,
    CONTEXT_DOMAIN_REQUIRED,
    CONTEXT_KEYS,
    COST_REDUCTION_ID_REQUIRED,
    COST_REDUCTION_KEYS,
    DECISION_BASIS_REQUIRED,
    DECISION_KEYS,
    EVIDENCE_PACK_KEYS,
    EXPECTED_OUTPUT,
    IMPACT_ASSESSMENT_KEYS,
    INTEGRITY_FLAG_KEYS,
    PROCESS_SEQUENCE,
    TOP_LEVEL_KEYS,
    TRACEABILITY_KEYS,
)


PASS = "PASS"
FAIL = "FAIL"
INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"


def validate_benchmark_case_03(case_data: dict) -> str:
    """
    Validate Benchmark Case 03 deterministically.

    BC-03 is a canonical INSUFFICIENT_EVIDENCE benchmark:
    a cost-cutting decision exists, but impact evidence is incomplete and
    the system must refuse a PASS/FAIL judgment.

    Returns:
        INSUFFICIENT_EVIDENCE if the canonical insufficient-evidence case
        is correctly represented.
        FAIL on any structural or rule violation.
    """
    if not isinstance(case_data, dict):
        return FAIL

    if tuple(case_data.keys()) != TOP_LEVEL_KEYS:
        return FAIL

    if case_data.get("case_id") != CASE_ID:
        return FAIL
    if case_data.get("case_name") != CASE_NAME:
        return FAIL
    if case_data.get("case_version") != CASE_VERSION:
        return FAIL
    if case_data.get("case_class") != CASE_CLASS:
        return FAIL
    if case_data.get("expected_output") != EXPECTED_OUTPUT:
        return FAIL

    context = case_data.get("context")
    if not isinstance(context, dict):
        return FAIL
    if tuple(context.keys()) != CONTEXT_KEYS:
        return FAIL
    if context.get("domain") != CONTEXT_DOMAIN_REQUIRED:
        return FAIL
    if not isinstance(context.get("service_type"), str) or not context.get("service_type"):
        return FAIL
    if not isinstance(context.get("selection_scope"), str) or not context.get("selection_scope"):
        return FAIL
    if context.get("predeclared_requirement") is not True:
        return FAIL

    agents = case_data.get("agents")
    if not isinstance(agents, dict):
        return FAIL
    if tuple(agents.keys()) != AGENTS_KEYS:
        return FAIL
    if not isinstance(agents.get("decision_authority"), str) or not agents.get("decision_authority"):
        return FAIL

    affected_units = agents.get("affected_units")
    if not isinstance(affected_units, list) or len(affected_units) < 1:
        return FAIL
    if len(affected_units) != len(set(affected_units)):
        return FAIL
    if any(not isinstance(unit, str) or not unit for unit in affected_units):
        return FAIL

    if not isinstance(agents.get("evaluation_mechanism"), str) or not agents.get("evaluation_mechanism"):
        return FAIL

    process = case_data.get("process")
    if not isinstance(process, list):
        return FAIL
    if tuple(process) != PROCESS_SEQUENCE:
        return FAIL

    evidence_pack = case_data.get("evidence_pack")
    if not isinstance(evidence_pack, dict):
        return FAIL
    if tuple(evidence_pack.keys()) != EVIDENCE_PACK_KEYS:
        return FAIL

    cost_reduction_definition = evidence_pack.get("cost_reduction_definition")
    if not isinstance(cost_reduction_definition, dict):
        return FAIL
    if tuple(cost_reduction_definition.keys()) != COST_REDUCTION_KEYS:
        return FAIL
    if cost_reduction_definition.get("id") != COST_REDUCTION_ID_REQUIRED:
        return FAIL
    if not isinstance(cost_reduction_definition.get("description"), str) or not cost_reduction_definition.get("description"):
        return FAIL
    if not isinstance(cost_reduction_definition.get("timestamp"), str) or not cost_reduction_definition.get("timestamp"):
        return FAIL

    impact_assessment = evidence_pack.get("impact_assessment")
    if not isinstance(impact_assessment, dict):
        return FAIL
    if tuple(impact_assessment.keys()) != IMPACT_ASSESSMENT_KEYS:
        return FAIL
    if impact_assessment.get("assessment_present") is not True:
        return FAIL
    if impact_assessment.get("service_impact_evaluated") is not False:
        return FAIL
    if impact_assessment.get("safety_impact_evaluated") is not False:
        return FAIL
    if impact_assessment.get("continuity_impact_evaluated") is not False:
        return FAIL

    decision_record = evidence_pack.get("decision_record")
    if not isinstance(decision_record, dict):
        return FAIL
    if tuple(decision_record.keys()) != DECISION_KEYS:
        return FAIL
    if not isinstance(decision_record.get("action_taken"), str) or not decision_record.get("action_taken"):
        return FAIL
    if decision_record.get("basis") != DECISION_BASIS_REQUIRED:
        return FAIL
    if not isinstance(decision_record.get("timestamp"), str) or not decision_record.get("timestamp"):
        return FAIL

    traceability_links = evidence_pack.get("traceability_links")
    if not isinstance(traceability_links, dict):
        return FAIL
    if tuple(traceability_links.keys()) != TRACEABILITY_KEYS:
        return FAIL
    if traceability_links.get("cost_reduction_to_impact_review") is not True:
        return FAIL
    if traceability_links.get("impact_review_to_decision") is not False:
        return FAIL
    if traceability_links.get("chain_complete") is not False:
        return FAIL

    integrity_flags = case_data.get("integrity_flags")
    if not isinstance(integrity_flags, dict):
        return FAIL
    if tuple(integrity_flags.keys()) != INTEGRITY_FLAG_KEYS:
        return FAIL
    if integrity_flags.get("evidence_incomplete") is not True:
        return FAIL
    if integrity_flags.get("impact_unknown") is not True:
        return FAIL
    if integrity_flags.get("decision_not_justified") is not True:
        return FAIL

    return INSUFFICIENT_EVIDENCE
