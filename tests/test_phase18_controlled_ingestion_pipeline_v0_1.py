import pytest

from gus_v7.intake.intake_channel_router_v0_1 import intake_channel_router_v0_1


def _build_valid_payload():
    return {
        "case_id": "BC-01",
        "case_name": "Transparent Vendor Selection",
    }


def test_phase18_manual_channel_accepts_canonical_payload():
    envelope = {
        "channel": "manual",
        "payload": _build_valid_payload(),
    }

    accepted = intake_channel_router_v0_1(envelope)

    assert accepted == envelope["payload"]


def test_phase18_system_channel_accepts_canonical_payload():
    envelope = {
        "channel": "system",
        "payload": _build_valid_payload(),
    }

    accepted = intake_channel_router_v0_1(envelope)

    assert accepted == envelope["payload"]


def test_phase18_rejects_non_dict_envelope():
    with pytest.raises(ValueError, match="INVALID_ENVELOPE_TYPE"):
        intake_channel_router_v0_1("not_a_dict")


def test_phase18_rejects_invalid_envelope_structure():
    envelope = {
        "payload": _build_valid_payload(),
        "channel": "manual",
        "extra": True,
    }

    with pytest.raises(ValueError, match="INVALID_ENVELOPE_STRUCTURE"):
        intake_channel_router_v0_1(envelope)


def test_phase18_rejects_empty_channel():
    envelope = {
        "channel": "",
        "payload": _build_valid_payload(),
    }

    with pytest.raises(ValueError, match="INVALID_CHANNEL_TYPE"):
        intake_channel_router_v0_1(envelope)


def test_phase18_rejects_unknown_channel():
    envelope = {
        "channel": "external",
        "payload": _build_valid_payload(),
    }

    with pytest.raises(ValueError, match="UNKNOWN_CHANNEL"):
        intake_channel_router_v0_1(envelope)


def test_phase18_rejects_non_dict_payload():
    envelope = {
        "channel": "manual",
        "payload": "not_a_dict",
    }

    with pytest.raises(ValueError, match="INVALID_PAYLOAD_TYPE"):
        intake_channel_router_v0_1(envelope)


def test_phase18_rejects_boundary_invalid_payload():
    envelope = {
        "channel": "manual",
        "payload": {},
    }

    with pytest.raises(ValueError, match="BOUNDARY_REJECTED_PAYLOAD"):
        intake_channel_router_v0_1(envelope)
