"""
GUS v7 — Phase 57
Governance Metrics Aggregation Schema (v0.1)

STRICT:
- Schema only
- Deterministic
- Fail-closed ready
- No inference
- No mutation
"""

# =========================
# METRICS OBJECT KEYS
# =========================

GOVERNANCE_METRICS_KEYS = (
    "total_decisions",
    "execute_count",
    "block_count",
    "integrity_confirmed_count",
    "integrity_rejected_count",
    "governance_pass_count",
    "governance_fail_count",
)


# =========================
# REQUIRED FIELDS
# =========================

REQUIRED_FIELDS = GOVERNANCE_METRICS_KEYS


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
    "M1_STRUCTURE_LOCK",
    "M2_REQUIRED_FIELDS_LOCK",
    "M3_INTEGER_ONLY_LOCK",
    "M4_NON_NEGATIVE_LOCK",
    "M5_NO_EXTRA_FIELDS_LOCK",
)


# =========================
# FAIL-CLOSED DEFINITION
# =========================

FAIL_CLOSED_BEHAVIOR = "ANY_VIOLATION_RESULTS_IN_INVALID_METRICS"
