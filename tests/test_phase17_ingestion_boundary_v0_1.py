"""
GUS v7 — Phase 17
Ingestion Boundary Tests (v0.1)

STRICT:
- Deterministic
- Fail-closed
- No coercion
- No inference
"""

from gus_v7.routing.ingestion_boundary_v0_1 import (
    ingest_case_payload_v0_1,
    ingest_case_batch_v0_1,
    ingest_or_fail_result_v0_1,
)
from gus_v7.routing.case_validator_router_v0_1 import FAIL


def _valid_case():
    return {
        "case_id": "BC-01",
        "any_field": "value"
    }


def test_phase17_accepts_valid_case_payload():
    case = _valid_case()
    result = ingest_case_payload_v0_1(case)

    assert result is case


def test_phase17_rejects_non_dict_payload():
    assert ingest_case_payload_v0_1("not_a_dict") is None
    assert ingest_case_payload_v0_1(123) is None
    assert ingest_case_payload_v0_1(None) is None


def test_phase17_rejects_empty_dict():
    assert ingest_case_payload_v0_1({}) is None


def test_phase17_rejects_missing_case_id():
    case = {"not_case_id": "x"}
    assert ingest_case_payload_v0_1(case) is None


def test_phase17_rejects_invalid_case_id():
    assert ingest_case_payload_v0_1({"case_id": ""}) is None
    assert ingest_case_payload_v0_1({"case_id": 123}) is None


def test_phase17_batch_accepts_valid_cases():
    batch = (_valid_case(), _valid_case())
    result = ingest_case_batch_v0_1(batch)

    assert isinstance(result, tuple)
    assert result == batch


def test_phase17_batch_rejects_invalid_container():
    assert ingest_case_batch_v0_1("not_a_batch") is None


def test_phase17_batch_rejects_invalid_member():
    batch = (_valid_case(), "bad_case")
    assert ingest_case_batch_v0_1(batch) is None


def test_phase17_ingest_or_fail_returns_fail_on_invalid():
    assert ingest_or_fail_result_v0_1("bad") == FAIL


def test_phase17_ingest_or_fail_returns_accepted_on_valid():
    assert ingest_or_fail_result_v0_1(_valid_case()) == "ACCEPTED"
