from __future__ import annotations

from typing import Any

from gus_v7.routing.ingestion_boundary_v0_1 import ingest_case_payload_v0_1


CHANNEL_POLICY_V0_1 = {
    "manual": {
        "allowed": True,
        "batch_allowed": False,
    },
    "system": {
        "allowed": True,
        "batch_allowed": True,
    },
}


def intake_channel_router_v0_1(envelope: dict[str, Any]) -> dict[str, Any]:
    """
    GUS v7 — Phase 19
    Intake Channel Policy Lock (v0.1)

    EXTENDS Phase 18:
    - Adds strict channel policy enforcement
    - Keeps full Phase 18 guarantees

    STRICT:
    - no parsing
    - no coercion
    - no repair
    - no fallback
    - no payload mutation
    - policy is static and deterministic
    """

    if not isinstance(envelope, dict):
        raise ValueError("INVALID_ENVELOPE_TYPE")

    if tuple(envelope.keys()) != ("channel", "payload"):
        raise ValueError("INVALID_ENVELOPE_STRUCTURE")

    channel = envelope["channel"]
    payload = envelope["payload"]

    if not isinstance(channel, str) or not channel:
        raise ValueError("INVALID_CHANNEL_TYPE")

    # ---- Phase 19 policy enforcement ----
    policy = CHANNEL_POLICY_V0_1.get(channel)
    if policy is None:
        raise ValueError("UNKNOWN_CHANNEL")

    if policy["allowed"] is not True:
        raise ValueError("CHANNEL_NOT_ALLOWED")

    # ---- Phase 18 checks remain ----
    if not isinstance(payload, dict):
        raise ValueError("INVALID_PAYLOAD_TYPE")

    accepted_payload = ingest_case_payload_v0_1(payload)
    if accepted_payload is None:
        raise ValueError("BOUNDARY_REJECTED_PAYLOAD")

    return accepted_payload
