"""
GUS v7 — Phase 48
Decision Execution Gate (v0.1)

STRICT:
- Deterministic
- Fail-closed
- No inference
- No external calls
"""


def apply_decision_execution_gate_v0_1(envelope: dict) -> str:
    """
    Returns:
        "EXECUTE" or "BLOCK"
    """

    final_integrity_verdict = envelope.get("final_integrity_verdict")

    if final_integrity_verdict == "INTEGRITY_CONFIRMED":
        return "EXECUTE"

    return "BLOCK"
