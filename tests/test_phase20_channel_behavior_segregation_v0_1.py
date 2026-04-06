import pytest

from gus_v7.intake.intake_channel_router_v0_1 import intake_channel_router_v0_1


def _valid_payload(case_id: str = "BC-01"):
    return {
        "case_id": case_id,
        "case_name": "Transparent Vendor Selection",
    }


def test_phase20_manual_accepts_single_payload():
    envelope = {
        "channel": "manual",
        "payload": _valid_payload(),
    }

    assert intake_channel_router_v0_1(envelope) == envelope["payload"]


def test_phase20_manual_rejects_batch_payload():
    envelope = {
        "channel": "manual",
        "payload": [_valid_payload(), _valid_payload()],
    }

    with pytest.raises(ValueError, match="MANUAL_REQUIRES_SINGLE_PAYLOAD"):
        intake_channel_router_v0_1(envelope)


def test_phase20_system_accepts_single_payload():
    envelope = {
        "channel": "system",
        "payload": _valid_payload(),
    }

    assert intake_channel_router_v0_1(envelope) == envelope["payload"]


def test_phase20_system_accepts_batch_payload():
    envelope = {
        "channel": "system",
        "payload": [_valid_payload("BC-01"), _valid_payload("BC-02")],
    }

    accepted = intake_channel_router_v0_1(envelope)

    assert accepted == tuple(envelope["payload"])


def test_phase20_system_rejects_invalid_payload_type():
    envelope = {
        "channel": "system",
        "payload": "not_a_valid_payload",
    }

    with pytest.raises(ValueError, match="INVALID_PAYLOAD_TYPE"):
        intake_channel_router_v0_1(envelope)


def test_phase20_system_rejects_invalid_batch_member():
    envelope = {
        "channel": "system",
        "payload": [_valid_payload(), {}],
    }

    with pytest.raises(ValueError, match="BOUNDARY_REJECTED_BATCH"):
        intake_channel_router_v0_1(envelope)
