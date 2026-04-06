from __future__ import annotations

from typing import Any

from gus_v7.routing.ingestion_boundary_v0_1 import ingest_case_payload_v0_1


ALLOWED_CHANNELS_V0_1 = (
    "manual",
    "system",
)


def intake_channel_router_v0_1(envelope: dict[str, Any]) -> dict[str, Any]:
    """
    GUS v7 — Phase 18
    Controlled Ingestion Pipeline / Intake Routing (v0.1)

    STRICT:
    - envelope must be a dict
    - envelope must contain exactly:
        - channel
        - payload
    - channel must be explicitly allowed
    - payload must already be a dict
    - no parsing
    - no coercion
    - no repair
    - no fallback
    - no payload mutation

    Output:
    - returns accepted payload unchanged
    - raises ValueError on any rejection
    """
    if not isinstance(envelope, dict):
        raise ValueError("INVALID_ENVELOPE_TYPE")

    if tuple(envelope.keys()) != ("channel", "payload"):
        raise ValueError("INVALID_ENVELOPE_STRUCTURE")

    channel = envelope["channel"]
    payload = envelope["payload"]

    if not isinstance(channel, str) or not channel:
        raise ValueError("INVALID_CHANNEL_TYPE")

    if channel not in ALLOWED_CHANNELS_V0_1:
        raise ValueError("UNKNOWN_CHANNEL")

    if not isinstance(payload, dict):
        raise ValueError("INVALID_PAYLOAD_TYPE")

    accepted_payload = ingest_case_payload_v0_1(payload)
    if accepted_payload is None:
        raise ValueError("BOUNDARY_REJECTED_PAYLOAD")

    return accepted_payload
