"""
GUS v7 — Phase 21
Execution Contract Tests (v0.1)

STRICT:
- Deterministic
- Fail-closed
- No mutation
- Contract-only
"""

from __future__ import annotations

from gus_v7.routing.execution_contract_v0_1 import accept_execution_contract_v0_1


def _build_valid_case() -> dict:
    return {
        "case_id": "BC-01",
        "case_name": "Transparent Vendor Selection",
    }


def test_phase21_accepts_single_case_dict_unchanged() -> None:
    payload = _build_valid_case()
    accepted = accept_execution_contract_v0_1(payload)

    assert accepted is payload
    assert accepted == payload


def test_phase21_accepts_batch_tuple_unchanged() -> None:
    batch = (_build_valid_case(), _build_valid_case())
    accepted = accept_execution_contract_v0_1(batch)

    assert accepted is batch
    assert accepted == batch


def test_phase21_rejects_list_fail_closed() -> None:
    payload = [_build_valid_case()]

    assert accept_execution_contract_v0_1(payload) is None


def test_phase21_rejects_string_fail_closed() -> None:
    assert accept_execution_contract_v0_1("not_valid") is None


def test_phase21_rejects_none_fail_closed() -> None:
    assert accept_execution_contract_v0_1(None) is None
