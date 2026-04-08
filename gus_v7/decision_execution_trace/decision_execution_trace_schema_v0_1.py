"""
GUS v7 — Phase 49
Decision Execution Trace Schema (v0.1)

STRICT:
- Schema only
- Deterministic
- Fail-closed ready
- No inference
- No mutation
"""

# =========================
# TRACE OBJECT KEYS
# =========================

DECISION_EXECUTION_TRACE_KEYS = (
    "trace_id",
    "decision_id",
    "case_id",
    "evidence_binding_id",
    "integrity_envelope_id",
    "final_integrity_verdict",
    "execution_result",
    "trace_timestamp",
    "trace_sequence",
)


# =========================
# REQUIRED VALUE CONSTRAINTS
# =========================

VALID_EXECUTION_RESULTS = (
    "EXECUTE",
    "BLOCK",
)

VALID_FINAL_INTEGRITY_VERDICTS = (
    "INTEGRITY_CONFIRMED",
    "INTEGRITY_REJECTED",
)


# =========================
# FIELD RULES
# =========================

REQUIRED_NON_EMPTY_FIELDS = (
    "trace_id",
    "decision_id",
    "case_id",
    "evidence_binding_id",
    "integrity_envelope_id",
    "final_integrity_verdict",
    "execution_result",
    "trace_timestamp",
    "trace_sequence",
)


# =========================
# STRUCTURE LOCK
# =========================

NO_EXTRA_FIELDS_ALLOWED = True


# =========================
# MUTABILITY LOCK
# =========================

IMMUTABLE_AFTER_LOGGING = True


# =========================
# VALIDATION RULE IDS
# =========================

VALIDATION_RULES = (
    "T1_STRUCTURE_LOCK",
    "T2_REQUIRED_FIELDS_LOCK",
    "T3_EXECUTION_RESULT_LOCK",
    "T4_FINAL_INTEGRITY_VERDICT_LOCK",
    "T5_NO_EXTRA_FIELDS_LOCK",
    "T6_IMMUTABILITY_LOCK",
)


# =========================
# FAIL-CLOSED DEFINITION
# =========================

FAIL_CLOSED_BEHAVIOR = "ANY_VIOLATION_RESULTS_IN_INVALID_TRACE"
