"""
GUS v7 — Phase 02
Benchmark Case 01 Schema (v0.1)

STRICT:
- No execution logic
- No inference
- Schema only (structure + validation rules as constants)
- Deterministic / fail-closed ready
"""

# =========================
# CASE IDENTITY (LOCKED)
# =========================

CASE_ID = "BC-01"
CASE_NAME = "Transparent Vendor Selection"
CASE_VERSION = "v0.1"
CASE_CLASS = "benchmark_pass"
EXPECTED_OUTPUT = "PASS"


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

CONTEXT_DOMAIN_REQUIRED = "vendor_selection"


# =========================
# AGENTS SCHEMA
# =========================

AGENTS_KEYS = (
    "selecting_authority",
    "candidate_vendors",
    "evaluation_mechanism",
)


# =========================
# PROCESS (STRICT ORDER LOCK)
# =========================

PROCESS_SEQUENCE = (
    "requirement_defined",
    "criteria_defined",
    "vendor_pool_fixed",
    "uniform_evaluation_executed",
    "evidence_recorded",
    "decision_logged",
)


# =========================
# EVIDENCE PACK SCHEMA
# =========================

EVIDENCE_PACK_KEYS = (
    "requirement_definition",
    "criteria_definition",
    "vendor_list",
    "evaluation_records",
    "decision_record",
    "traceability_links",
)


# -------------------------
# REQUIREMENT
# -------------------------

REQUIREMENT_KEYS = (
    "id",
    "description",
    "timestamp",
)

REQUIREMENT_ID_REQUIRED = "REQ-001"


# -------------------------
# CRITERIA
# -------------------------

CRITERIA_IDS_REQUIRED = ("C1", "C2", "C3")


# -------------------------
# EVALUATION RECORD
# -------------------------

EVALUATION_RECORD_KEYS = (
    "vendor_id",
    "criteria_results",
    "evidence_refs",
)

CRITERIA_RESULT_KEYS_REQUIRED = ("C1", "C2", "C3")


# -------------------------
# DECISION RECORD
# -------------------------

DECISION_KEYS = (
    "selected_vendor",
    "basis",
    "timestamp",
)

DECISION_BASIS_REQUIRED = "criteria_output_alignment"


# -------------------------
# TRACEABILITY
# -------------------------

TRACEABILITY_KEYS = (
    "requirement_to_criteria",
    "criteria_to_evaluations",
    "evaluations_to_decision",
    "chain_complete",
)


# =========================
# INTEGRITY FLAGS
# =========================

INTEGRITY_FLAG_KEYS = (
    "criteria_predefined",
    "uniform_evaluation",
    "evidence_present",
    "traceability_complete",
    "no_external_influence",
)


# =========================
# VALIDATION RULE IDS (NO LOGIC — DECLARATIVE ONLY)
# =========================

VALIDATION_RULES = (
    "V1_IDENTITY_LOCK",
    "V2_STRUCTURE_LOCK",
    "V3_PROCESS_SEQUENCE_LOCK",
    "V4_VENDOR_COMPLETENESS_LOCK",
    "V5_CRITERIA_UNIFORMITY_LOCK",
    "V6_EVIDENCE_PRESENCE_LOCK",
    "V7_TRACEABILITY_LOCK",
    "V8_DECISION_LEGITIMACY_LOCK",
    "V9_EXTERNAL_INFLUENCE_LOCK",
    "V10_OUTPUT_LOCK",
)


# =========================
# FAIL-CLOSED DEFINITION
# =========================

FAIL_CLOSED_BEHAVIOR = "ANY_VIOLATION_RESULTS_IN_FAIL"
