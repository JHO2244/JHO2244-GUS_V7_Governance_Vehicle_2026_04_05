from __future__ import annotations

from typing import Any

from gus_v7.routing.ingestion_boundary_v0_1 import (
    ingest_case_batch_v0_1,
    ingest_case_payload_v0_1,
)


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


def intake_channel_router_v0_1(
    envelope: dict[str, Any],
) -> dict[str, Any] | tuple[dict[str, Any], ...]:
    """
    GUS v7 — Phase 20
    Channel Behavior Segregation (v0.1)

    EXTENDS Phase 19:
    - keeps strict channel permission policy
    - adds deterministic behavior segregation by channel

    STRICT:
    - no parsing
    - no coercion
    - no repair
    - no fallback
    - no payload mutation
    - policy is static and deterministic

    Behavior:
    - manual channel accepts single payload only
    - system channel accepts single payload or batch payload
    """

    if not isinstance(envelope, dict):
        raise ValueError("INVALID_ENVELOPE_TYPE")

    if tuple(envelope.keys()) != ("channel", "payload"):
        raise ValueError("INVALID_ENVELOPE_STRUCTURE")

    channel = envelope["channel"]
    payload = envelope["payload"]

    if not isinstance(channel, str) or not channel:
        raise ValueError("INVALID_CHANNEL_TYPE")

    policy = CHANNEL_POLICY_V0_1.get(channel)
    if policy is None:
        raise ValueError("UNKNOWN_CHANNEL")

    if policy["allowed"] is not True:
        raise ValueError("CHANNEL_NOT_ALLOWED")

    if channel == "manual":
        if isinstance(payload, dict):
            accepted_payload = ingest_case_payload_v0_1(payload)
            if accepted_payload is None:
                raise ValueError("BOUNDARY_REJECTED_PAYLOAD")
            return accepted_payload

        if isinstance(payload, (tuple, list)):
            raise ValueError("MANUAL_REQUIRES_SINGLE_PAYLOAD")

        raise ValueError("INVALID_PAYLOAD_TYPE")

    if channel == "system":
        if isinstance(payload, dict):
            accepted_payload = ingest_case_payload_v0_1(payload)
            if accepted_payload is None:
                raise ValueError("BOUNDARY_REJECTED_PAYLOAD")
            return accepted_payload

        if isinstance(payload, (tuple, list)):
            accepted_batch = ingest_case_batch_v0_1(payload)
            if accepted_batch is None:
                raise ValueError("BOUNDARY_REJECTED_BATCH")
            return accepted_batch

        raise ValueError("INVALID_PAYLOAD_TYPE")

    raise ValueError("UNREACHABLE_CHANNEL_STATE")
