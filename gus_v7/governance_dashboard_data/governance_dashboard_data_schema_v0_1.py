"""
GUS v7 — Phase 60
Governance Dashboard Data Schema (v0.1)

STRICT:
- Schema only
- Deterministic
- Fail-closed ready
- No inference
- No mutation
"""

# =========================
# DASHBOARD DATA KEYS
# =========================

GOVERNANCE_DASHBOARD_DATA_KEYS = (
    "total_decisions",
    "governance_pass_count",
    "governance_fail_count",
    "compliance_result",
    "exception_status",
    "alert_status",
)


# =========================
# REQUIRED FIELDS
# =========================

REQUIRED_FIELDS = GOVERNANCE_DASHBOARD_DATA_KEYS


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

VALID_EXCEPTION_STATUS = (
    "NO_EXCEPTION",
    "EXCEPTION_OPEN",
)

VALID_ALERT_STATUS = (
    "NO_ALERT",
    "ALERT_RAISED",
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
    "D1_STRUCTURE_LOCK",
    "D2_REQUIRED_FIELDS_LOCK",
    "D3_INTEGER_FIELDS_LOCK",
    "D4_COMPLIANCE_RESULT_LOCK",
    "D5_EXCEPTION_STATUS_LOCK",
    "D6_ALERT_STATUS_LOCK",
    "D7_NON_NEGATIVE_LOCK",
    "D8_NO_EXTRA_FIELDS_LOCK",
)


# =========================
# FAIL-CLOSED DEFINITION
# =========================

FAIL_CLOSED_BEHAVIOR = "ANY_VIOLATION_RESULTS_IN_INVALID_DASHBOARD_DATA"
