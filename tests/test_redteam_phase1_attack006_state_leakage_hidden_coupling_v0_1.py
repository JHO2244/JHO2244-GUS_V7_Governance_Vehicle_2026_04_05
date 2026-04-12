from gus_v7.routing.ingestion_boundary_v0_1 import (
    ingest_case_batch_v0_1,
    ingest_case_payload_v0_1,
)


def _case(case_id: str, note: str) -> dict[str, str]:
    return {
        "case_id": case_id,
        "note": note,
    }


def test_attack006_single_payload_acceptance_reuses_original_reference():
    payload = _case("BC-01", "original")

    accepted = ingest_case_payload_v0_1(payload)

    assert accepted is payload


def test_attack006_batch_acceptance_reuses_original_member_references():
    case_a = _case("BC-01", "A")
    case_b = _case("BC-02", "B")

    accepted = ingest_case_batch_v0_1((case_a, case_b))

    assert accepted is not None
    assert accepted[0] is case_a
    assert accepted[1] is case_b


def test_attack006_mutating_original_after_acceptance_changes_accepted_view():
    payload = _case("BC-01", "before")

    accepted = ingest_case_payload_v0_1(payload)
    payload["note"] = "after"

    assert accepted is not None
    assert accepted["note"] == "after"


def test_attack006_batch_member_mutation_after_acceptance_leaks_into_accepted_batch():
    case_a = _case("BC-01", "before-a")
    case_b = _case("BC-02", "before-b")

    accepted = ingest_case_batch_v0_1((case_a, case_b))
    case_a["note"] = "after-a"

    assert accepted is not None
    assert accepted[0]["note"] == "after-a"
    assert accepted[1]["note"] == "before-b"


def test_attack006_shared_input_reference_contaminates_multiple_acceptances():
    shared = _case("BC-01", "start")

    accepted_one = ingest_case_payload_v0_1(shared)
    accepted_two = ingest_case_payload_v0_1(shared)

    shared["note"] = "contaminated"

    assert accepted_one is not None
    assert accepted_two is not None
    assert accepted_one["note"] == "contaminated"
    assert accepted_two["note"] == "contaminated"
