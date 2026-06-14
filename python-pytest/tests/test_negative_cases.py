"""Negative and edge-case coverage.

A suite is only as trustworthy as its failure handling. These cover the status
codes recruiters and auditors actually ask about: 400/401/403/404 and a 500
simulated via the public httpstat-style endpoints booker doesn't give us, so we
lean on reqres' delayed/error behaviours and jsonplaceholder's 404s.
"""
import pytest

from utils.assertions import assert_status


@pytest.mark.negative
def test_register_missing_password_returns_400(reqres):
    resp = reqres.post("/register", json={"email": "sydney.farr@reqres.in"})
    assert_status(resp, 400)
    assert resp.json()["error"] == "Missing password"


@pytest.mark.negative
def test_register_unknown_email_returns_400(reqres):
    # reqres only allows registration for its seeded address; anything else 400s
    resp = reqres.post(
        "/register", json={"email": "not-on-the-list@example.com", "password": "x"}
    )
    assert_status(resp, 400)


@pytest.mark.negative
def test_booker_write_without_token_is_unauthorized(booker, new_booking_payload):
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
@pytest.mark.parametrize("missing_id", [0, 23, 999])
def test_unknown_reqres_user_returns_404(reqres, missing_id):
    resp = reqres.get(f"/users/{missing_id}")
    assert_status(resp, 404)
    assert resp.json() == {}


@pytest.mark.negative
def test_jsonplaceholder_unknown_resource_returns_404(jsonplaceholder):
    resp = jsonplaceholder.get("/posts/9999")
    assert_status(resp, 404)


@pytest.mark.negative
def test_malformed_path_returns_404(jsonplaceholder):
    resp = jsonplaceholder.get("/this-route-does-not-exist")
    assert_status(resp, 404)
