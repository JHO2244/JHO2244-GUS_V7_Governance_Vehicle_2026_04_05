"""
GUS v7 — Phase 63
Governance Notifications and Hooks Schema (v0.1)

STRICT:
- Schema only
- Deterministic
- Fail-closed ready
- No inference
- No mutation
"""

# =========================
# OUTPUT KEYS
# =========================

GOVERNANCE_NOTIFICATIONS_HOOKS_KEYS = (
    "notification_required",
    "hook_required",
    "notification_reason",
    "hook_reason",
)


# =========================
# REQUIRED FIELDS
# =========================

REQUIRED_FIELDS = GOVERNANCE_NOTIFICATIONS_HOOKS_KEYS


# =========================
# VALUE CONSTRAINTS
# =========================

BOOLEAN_FIELDS = (
    "notification_required",
    "hook_required",
)

VALID_NOTIFICATION_REASONS = (
    "NONE",
    "HIGH_RISK",
    "ALERT_RAISED",
)

VALID_HOOK_REASONS = (
    "NONE",
    "HIGH_RISK",
    "EXCEPTION_OPEN",
)


# =========================
# STRUCTURE LOCK
# =========================

NO_EXTRA_FIELDS_ALLOWED = True


# =========================
# VALIDATION RULE IDS
# =========================

VALIDATION_RULES = (
    "N1_STRUCTURE_LOCK",
    "N2_REQUIRED_FIELDS_LOCK",
    "N3_BOOLEAN_FIELDS_LOCK",
    "N4_NOTIFICATION_REASON_LOCK",
    "N5_HOOK_REASON_LOCK",
    "N6_NO_EXTRA_FIELDS_LOCK",
)


# =========================
# FAIL-CLOSED DEFINITION
# =========================

FAIL_CLOSED_BEHAVIOR = "ANY_VIOLATION_RESULTS_IN_INVALID_NOTIFICATION_HOOK_OUTPUT"
