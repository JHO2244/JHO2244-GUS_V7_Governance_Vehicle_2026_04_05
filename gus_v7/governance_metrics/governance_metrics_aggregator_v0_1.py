"""
GUS v7 — Phase 57
Governance Metrics Aggregator (v0.1)

STRICT:
- Deterministic
- Fail-closed
- No inference
- No mutation
- No external calls
"""

from gus_v7.governance_metrics.governance_metrics_schema_v0_1 import (
    GOVERNANCE_METRICS_KEYS,
)


REQUIRED_INPUT_KEYS = (
    "decision_id",
    "execution_result",
    "final_integrity_verdict",
    "governance_result",
)

VALID_EXECUTION_RESULTS = ("EXECUTE", "BLOCK")
VALID_INTEGRITY_VERDICTS = ("INTEGRITY_CONFIRMED", "INTEGRITY_REJECTED")
VALID_GOVERNANCE_RESULTS = ("GOVERNANCE_PASS", "GOVERNANCE_FAIL")


def aggregate_governance_metrics_v0_1(entries: list) -> dict:
    """
    Returns:
        governance metrics dict

    Fail-closed behavior:
    - empty input -> ValueError
    - malformed entry -> ValueError
    """

    if not isinstance(entries, list) or len(entries) == 0:
        raise ValueError("INVALID_INPUT")

    total = 0
    execute_count = 0
    block_count = 0
    integrity_confirmed_count = 0
    integrity_rejected_count = 0
    governance_pass_count = 0
    governance_fail_count = 0

    for entry in entries:
        # -------------------------
        # STRUCTURE VALIDATION
        # -------------------------
        if set(entry.keys()) != set(REQUIRED_INPUT_KEYS):
            raise ValueError("INVALID_ENTRY")

        for field in REQUIRED_INPUT_KEYS:
            if entry[field] in (None, "", []):
                raise ValueError("INVALID_ENTRY")

        # -------------------------
        # VALUE VALIDATION
        # -------------------------
        execution_result = entry["execution_result"]
        integrity_verdict = entry["final_integrity_verdict"]
        governance_result = entry["governance_result"]

        if execution_result not in VALID_EXECUTION_RESULTS:
            raise ValueError("INVALID_ENTRY")

        if integrity_verdict not in VALID_INTEGRITY_VERDICTS:
            raise ValueError("INVALID_ENTRY")

        if governance_result not in VALID_GOVERNANCE_RESULTS:
            raise ValueError("INVALID_ENTRY")

        # -------------------------
        # COUNTING
        # -------------------------
        total += 1

        if execution_result == "EXECUTE":
            execute_count += 1
        else:
            block_count += 1

        if integrity_verdict == "INTEGRITY_CONFIRMED":
            integrity_confirmed_count += 1
        else:
            integrity_rejected_count += 1

        if governance_result == "GOVERNANCE_PASS":
            governance_pass_count += 1
        else:
            governance_fail_count += 1

    return {
        "total_decisions": total,
        "execute_count": execute_count,
        "block_count": block_count,
        "integrity_confirmed_count": integrity_confirmed_count,
        "integrity_rejected_count": integrity_rejected_count,
        "governance_pass_count": governance_pass_count,
        "governance_fail_count": governance_fail_count,
    }
