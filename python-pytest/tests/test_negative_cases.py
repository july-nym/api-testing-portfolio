"""Negative and edge-case coverage.

A suite is only as trustworthy as its failure handling. These cover the status
codes recruiters and auditors actually ask about — 401/403/404 — plus a couple of
contract quirks worth pinning so a future change is caught.
"""
import pytest

from utils.assertions import assert_status


@pytest.mark.negative
@pytest.mark.parametrize("missing_id", [11, 99, 999])
def test_unknown_user_returns_404(jsonplaceholder, missing_id):
    # jsonplaceholder only seeds 10 users; anything past that is a 404
    resp = jsonplaceholder.get(f"/users/{missing_id}")
    assert_status(resp, 404)


@pytest.mark.negative
def test_unknown_post_returns_404(jsonplaceholder):
    resp = jsonplaceholder.get("/posts/9999")
    assert_status(resp, 404)


@pytest.mark.negative
def test_malformed_path_returns_404(jsonplaceholder):
    resp = jsonplaceholder.get("/this-route-does-not-exist")
    assert_status(resp, 404)


@pytest.mark.negative
def test_booker_write_without_token_is_forbidden(booker, new_booking_payload):
    created = booker.post("/booking", json=new_booking_payload)
    booking_id = created.json()["bookingid"]

    # no Cookie header -> booker rejects the mutation
    resp = booker.put(f"/booking/{booking_id}", json=new_booking_payload)
    assert_status(resp, 403)


@pytest.mark.negative
def test_booker_bad_credentials_yield_reason(booker):
    resp = booker.post(
        "/auth", json={"username": "admin", "password": "wrong-password"}
    )
    # booker returns 200 with a "reason" body rather than a 401 — worth pinning
    # so a future contract change is caught.
    assert_status(resp, 200)
    assert resp.json().get("reason") == "Bad credentials"


@pytest.mark.negative
def test_fetch_missing_booking_returns_404(booker):
    # An id well beyond anything the sandbox is likely to hold
    resp = booker.get("/booking/99999999")
    assert_status(resp, 404)
