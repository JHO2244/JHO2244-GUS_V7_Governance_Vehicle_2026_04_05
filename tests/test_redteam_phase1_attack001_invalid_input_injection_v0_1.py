import pytest

from gus_v7.intake.intake_channel_router_v0_1 import intake_channel_router_v0_1


def _valid_payload():
    return {
        "case_id": "BC-01",
        "case_name": "Transparent Vendor Selection",
    }


def test_attack001_rejects_non_dict_envelope():
    with pytest.raises(ValueError, match="INVALID_ENVELOPE_TYPE"):
        intake_channel_router_v0_1("not_a_dict")


def test_attack001_rejects_missing_payload_key():
    envelope = {
        "channel": "manual",
    }

    with pytest.raises(ValueError, match="INVALID_ENVELOPE_STRUCTURE"):
        intake_channel_router_v0_1(envelope)


def test_attack001_rejects_extra_envelope_key():
    envelope = {
        "channel": "manual",
        "payload": _valid_payload(),
        "extra": "unexpected",
    }

    with pytest.raises(ValueError, match="INVALID_ENVELOPE_STRUCTURE"):
        intake_channel_router_v0_1(envelope)


def test_attack001_rejects_wrong_key_order():
    envelope = {
        "payload": _valid_payload(),
        "channel": "manual",
    }

    with pytest.raises(ValueError, match="INVALID_ENVELOPE_STRUCTURE"):
        intake_channel_router_v0_1(envelope)


def test_attack001_rejects_non_string_channel():
    envelope = {
        "channel": 123,
        "payload": _valid_payload(),
    }

    with pytest.raises(ValueError, match="INVALID_CHANNEL_TYPE"):
        intake_channel_router_v0_1(envelope)


def test_attack001_rejects_empty_channel():
    envelope = {
        "channel": "",
        "payload": _valid_payload(),
    }

    with pytest.raises(ValueError, match="INVALID_CHANNEL_TYPE"):
        intake_channel_router_v0_1(envelope)


def test_attack001_manual_rejects_scalar_payload():
    envelope = {
        "channel": "manual",
        "payload": 42,
    }

    with pytest.raises(ValueError, match="INVALID_PAYLOAD_TYPE"):
        intake_channel_router_v0_1(envelope)
