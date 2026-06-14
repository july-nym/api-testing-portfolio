"""Full CRUD lifecycle against restful-booker.

This is the suite that proves we can drive a stateful API end to end: create a
booking, read it back, mutate it with auth, then delete it and confirm it's gone.
restful-booker wants the token in a Cookie header for write ops, which is why we
build `auth_cookie` rather than using the client's bearer helper.
"""
import pytest

from utils.assertions import (
    assert_status,
    assert_response_under,
    assert_matches_schema,
)
from utils.schemas import BOOKING_CREATE_SCHEMA


@pytest.fixture
def auth_cookie(booker_token):
    # booker is idiosyncratic: PUT/DELETE expect `Cookie: token=...`
    return {"Cookie": f"token={booker_token}"}


@pytest.mark.smoke
def test_create_booking_returns_id(booker, new_booking_payload, settings):
    resp = booker.post("/booking", json=new_booking_payload)
    assert_status(resp, 200)
    assert_response_under(resp, settings.max_response_ms)
    assert_matches_schema(resp.json(), BOOKING_CREATE_SCHEMA)
    assert resp.json()["booking"]["firstname"] == "Mariana"


@pytest.mark.regression
def test_full_booking_lifecycle(booker, auth_cookie, new_booking_payload):
    # --- create -------------------------------------------------------------
    created = booker.post("/booking", json=new_booking_payload)
    assert_status(created, 200)
    booking_id = created.json()["bookingid"]

    # --- read ---------------------------------------------------------------
    fetched = booker.get(f"/booking/{booking_id}")
    assert_status(fetched, 200)
    assert fetched.json()["lastname"] == "Okafor"

    # --- update (full replace) ---------------------------------------------
    updated_body = {**new_booking_payload, "totalprice": 1290, "depositpaid": False}
    updated = booker.put(
        f"/booking/{booking_id}", json=updated_body, headers=auth_cookie
    )
    assert_status(updated, 200)
    assert updated.json()["totalprice"] == 1290

    # --- delete + confirm gone ---------------------------------------------
    deleted = booker.delete(f"/booking/{booking_id}", headers=auth_cookie)
    assert_status(deleted, 201)  # booker returns 201 on a successful delete (quirk)

    gone = booker.get(f"/booking/{booking_id}")
    assert_status(gone, 404)


@pytest.mark.regression
def test_partial_update_changes_only_targeted_fields(
    booker, auth_cookie, new_booking_payload
):
    created = booker.post("/booking", json=new_booking_payload)
    booking_id = created.json()["bookingid"]

    patched = booker.patch(
        f"/booking/{booking_id}",
        json={"additionalneeds": "Airport transfer"},
        headers=auth_cookie,
    )
    assert_status(patched, 200)
    body = patched.json()
    assert body["additionalneeds"] == "Airport transfer"
    # untouched field should survive the partial update
    assert body["firstname"] == "Mariana"


@pytest.mark.regression
def test_filter_bookings_by_name(booker, new_booking_payload):
    # seed one we can find
    booker.post("/booking", json=new_booking_payload)
    resp = booker.get(
        "/booking", params={"firstname": "Mariana", "lastname": "Okafor"}
    )
    assert_status(resp, 200)
    # response is a list of {"bookingid": N}; at least our seed should be present
    assert isinstance(resp.json(), list)
    assert len(resp.json()) >= 1
