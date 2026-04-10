"""
GUS v7 — Phase 61
Historical Decision Analytics Schema (v0.1)

STRICT:
- Schema only
- Deterministic
- Fail-closed ready
- No inference
- No mutation
"""

# =========================
# HISTORY ANALYTICS KEYS
# =========================

HISTORICAL_DECISION_ANALYTICS_KEYS = (
    "snapshot_count",
    "total_decisions_sum",
    "governance_pass_sum",
    "governance_fail_sum",
    "compliant_snapshot_count",
    "non_compliant_snapshot_count",
    "exception_open_snapshot_count",
    "alert_raised_snapshot_count",
)


# =========================
# REQUIRED FIELDS
# =========================

REQUIRED_FIELDS = HISTORICAL_DECISION_ANALYTICS_KEYS


# =========================
# VALUE CONSTRAINTS
# =========================

ALL_FIELDS_INTEGER = True
NO_NEGATIVE_VALUES = True


# =========================
# STRUCTURE LOCK
# =========================

NO_EXTRA_FIELDS_ALLOWED = True


# =========================
# VALIDATION RULE IDS
# =========================

VALIDATION_RULES = (
    "H1_STRUCTURE_LOCK",
    "H2_REQUIRED_FIELDS_LOCK",
    "H3_INTEGER_ONLY_LOCK",
    "H4_NON_NEGATIVE_LOCK",
    "H5_NO_EXTRA_FIELDS_LOCK",
)


# =========================
# FAIL-CLOSED DEFINITION
# =========================

FAIL_CLOSED_BEHAVIOR = "ANY_VIOLATION_RESULTS_IN_INVALID_HISTORY_ANALYTICS"
