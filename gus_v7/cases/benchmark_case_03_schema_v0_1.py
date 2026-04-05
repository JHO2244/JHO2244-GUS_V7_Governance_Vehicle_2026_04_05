"""
GUS v7 — Phase 12
Benchmark Case 03 Schema (v0.1)

STRICT:
- No execution logic
- No inference
- Schema only (structure + validation rules as constants)
- Deterministic / fail-closed ready
"""

# =========================
# CASE IDENTITY (LOCKED)
# =========================

CASE_ID = "BC-03"
CASE_NAME = "Cost-Cutting Unclear Impact"
CASE_VERSION = "v0.1"
CASE_CLASS = "benchmark_insufficient_evidence"
EXPECTED_OUTPUT = "INSUFFICIENT_EVIDENCE"


# =========================
# TOP-LEVEL SCHEMA KEYS
# =========================

TOP_LEVEL_KEYS = (
    "case_id",
    "case_name",
    "case_version",
    "case_class",
    "context",
    "agents",
    "process",
    "evidence_pack",
    "integrity_flags",
    "expected_output",
)


# =========================
# CONTEXT SCHEMA
# =========================

CONTEXT_KEYS = (
    "domain",
    "service_type",
    "selection_scope",
    "predeclared_requirement",
)

CONTEXT_DOMAIN_REQUIRED = "cost_management"


# =========================
# AGENTS SCHEMA
# =========================

AGENTS_KEYS = (
    "decision_authority",
    "affected_units",
    "evaluation_mechanism",
)


# =========================
# PROCESS (STRICT ORDER LOCK)
# =========================

PROCESS_SEQUENCE = (
    "cost_pressure_identified",
    "reduction_option_defined",
    "impact_review_attempted",
    "decision_logged",
)


# =========================
# EVIDENCE PACK SCHEMA
# =========================

EVIDENCE_PACK_KEYS = (
    "cost_reduction_definition",
    "impact_assessment",
    "decision_record",
    "traceability_links",
)


# -------------------------
# COST REDUCTION DEFINITION
# -------------------------

COST_REDUCTION_KEYS = (
    "id",
    "description",
    "timestamp",
)

COST_REDUCTION_ID_REQUIRED = "CR-001"


# -------------------------
# IMPACT ASSESSMENT
# -------------------------

IMPACT_ASSESSMENT_KEYS = (
    "assessment_present",
    "service_impact_evaluated",
    "safety_impact_evaluated",
    "continuity_impact_evaluated",
)


# -------------------------
# DECISION RECORD
# -------------------------

DECISION_KEYS = (
    "action_taken",
    "basis",
    "timestamp",
)

DECISION_BASIS_REQUIRED = "incomplete_impact_evidence"


# -------------------------
# TRACEABILITY
# -------------------------

TRACEABILITY_KEYS = (
    "cost_reduction_to_impact_review",
    "impact_review_to_decision",
    "chain_complete",
)


# =========================
# INTEGRITY FLAGS
# =========================

INTEGRITY_FLAG_KEYS = (
    "evidence_incomplete",
    "impact_unknown",
    "decision_not_justified",
)


# =========================
# VALIDATION RULE IDS
# =========================

VALIDATION_RULES = (
    "V1_IDENTITY_LOCK",
    "V2_STRUCTURE_LOCK",
    "V3_PROCESS_SEQUENCE_LOCK",
    "V4_IMPACT_ASSESSMENT_INCOMPLETE_LOCK",
    "V5_TRACEABILITY_INCOMPLETE_LOCK",
    "V6_DECISION_BASIS_LOCK",
    "V7_INSUFFICIENT_EVIDENCE_LOCK",
    "V8_OUTPUT_LOCK",
)


# =========================
# FAIL-CLOSED DEFINITION
# =========================

FAIL_CLOSED_BEHAVIOR = "ANY_VIOLATION_RESULTS_IN_FAIL"
