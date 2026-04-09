"""
GUS v7 — Phase 58
Policy Compliance Report Schema (v0.1)

STRICT:
- Schema only
- Deterministic
- Fail-closed ready
- No inference
- No mutation
"""

# =========================
# REPORT OBJECT KEYS
# =========================

POLICY_COMPLIANCE_REPORT_KEYS = (
    "total_decisions",
    "governance_pass_count",
    "governance_fail_count",
    "compliance_result",
)


# =========================
# REQUIRED FIELDS
# =========================

REQUIRED_FIELDS = POLICY_COMPLIANCE_REPORT_KEYS


# =========================
# VALUE CONSTRAINTS
# =========================

INTEGER_FIELDS = (
    "total_decisions",
    "governance_pass_count",
    "governance_fail_count",
)

VALID_COMPLIANCE_RESULTS = (
    "COMPLIANT",
    "NON_COMPLIANT",
)

NO_NEGATIVE_VALUES = True


# =========================
# STRUCTURE LOCK
# =========================

NO_EXTRA_FIELDS_ALLOWED = True


# =========================
# VALIDATION RULE IDS
# =========================

VALIDATION_RULES = (
    "R1_STRUCTURE_LOCK",
    "R2_REQUIRED_FIELDS_LOCK",
    "R3_INTEGER_FIELDS_LOCK",
    "R4_COMPLIANCE_RESULT_LOCK",
    "R5_NON_NEGATIVE_LOCK",
    "R6_NO_EXTRA_FIELDS_LOCK",
)


# =========================
# FAIL-CLOSED DEFINITION
# =========================

FAIL_CLOSED_BEHAVIOR = "ANY_VIOLATION_RESULTS_IN_INVALID_REPORT"
