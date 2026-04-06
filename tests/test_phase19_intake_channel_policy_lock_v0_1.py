import pytest

from gus_v7.intake.intake_channel_router_v0_1 import intake_channel_router_v0_1


def _valid_payload():
    return {
        "case_id": "BC-01",
        "case_name": "Transparent Vendor Selection",
    }


def test_phase19_manual_allowed():
    envelope = {
        "channel": "manual",
        "payload": _valid_payload(),
    }

    assert intake_channel_router_v0_1(envelope) == envelope["payload"]


def test_phase19_system_allowed():
    envelope = {
        "channel": "system",
        "payload": _valid_payload(),
    }

    assert intake_channel_router_v0_1(envelope) == envelope["payload"]


def test_phase19_unknown_channel_rejected():
    envelope = {
        "channel": "external",
        "payload": _valid_payload(),
    }

    with pytest.raises(ValueError, match="UNKNOWN_CHANNEL"):
        intake_channel_router_v0_1(envelope)


def test_phase19_channel_not_allowed():
    # simulate future restriction by temporarily altering policy
    from gus_v7.intake import intake_channel_router_v0_1 as module

    original = module.CHANNEL_POLICY_V0_1["manual"]["allowed"]
    module.CHANNEL_POLICY_V0_1["manual"]["allowed"] = False

    try:
        envelope = {
            "channel": "manual",
            "payload": _valid_payload(),
        }

        with pytest.raises(ValueError, match="CHANNEL_NOT_ALLOWED"):
            intake_channel_router_v0_1(envelope)
    finally:
        module.CHANNEL_POLICY_V0_1["manual"]["allowed"] = original
