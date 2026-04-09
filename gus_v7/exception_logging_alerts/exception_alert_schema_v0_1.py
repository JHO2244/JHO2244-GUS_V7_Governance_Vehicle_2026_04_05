"""
GUS v7 — Phase 59
Exception Logging & Alerts Schema (v0.1)

STRICT:
- Schema only
- Deterministic
- Fail-closed ready
- No inference
- No mutation
"""

# =========================
# ALERT OBJECT KEYS
# =========================

EXCEPTION_ALERT_KEYS = (
    "total_decisions",
    "governance_fail_count",
    "compliance_result",
    "exception_status",
    "alert_status",
)


# =========================
# REQUIRED FIELDS
# =========================

REQUIRED_FIELDS = EXCEPTION_ALERT_KEYS


# =========================
# VALUE CONSTRAINTS
# =========================

INTEGER_FIELDS = (
    "total_decisions",
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
    "E1_STRUCTURE_LOCK",
    "E2_REQUIRED_FIELDS_LOCK",
    "E3_INTEGER_FIELDS_LOCK",
    "E4_COMPLIANCE_RESULT_LOCK",
    "E5_EXCEPTION_STATUS_LOCK",
    "E6_ALERT_STATUS_LOCK",
    "E7_NON_NEGATIVE_LOCK",
    "E8_NO_EXTRA_FIELDS_LOCK",
)


# =========================
# FAIL-CLOSED DEFINITION
# =========================

FAIL_CLOSED_BEHAVIOR = "ANY_VIOLATION_RESULTS_IN_INVALID_ALERT"
