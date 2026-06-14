"""Authentication flows against reqres and restful-booker.

reqres gives us register/login happy + sad paths; booker gives us a real token
issue that downstream write tests depend on.
"""
import pytest

from utils.assertions import assert_status, assert_response_under


@pytest.mark.smoke
def test_registered_user_can_login(reqres, settings):
    # reqres only accepts a known set of seeded accounts for login
    credentials = {"email": "eve.holt@reqres.in", "password": "cityslicka"}
    resp = reqres.post("/login", json=credentials)

    assert_status(resp, 200)
    assert_response_under(resp, settings.max_response_ms)
    assert resp.json().get("token"), "Expected a token in the login response"


@pytest.mark.smoke
def test_register_returns_id_and_token(reqres):
    resp = reqres.post(
        "/register",
        json={"email": "eve.holt@reqres.in", "password": "pistol"},
    )
    assert_status(resp, 200)
    body = resp.json()
    assert body["id"] == 4  # reqres returns a fixed id for this seeded account
    assert "token" in body


@pytest.mark.smoke
def test_booker_auth_issues_token(booker_token):
    # The fixture already asserted success; this documents the contract and gives
    # us a named smoke test in the report.
    assert isinstance(booker_token, str)
    assert len(booker_token) >= 10


@pytest.mark.negative
def test_login_without_password_is_rejected(reqres):
    resp = reqres.post("/login", json={"email": "peter.holt@reqres.in"})
    assert_status(resp, 400)
    assert resp.json().get("error") == "Missing password"


@pytest.mark.negative
def test_bearer_can_be_attached_and_cleared(reqres):
    # Not hitting a protected reqres endpoint (there isn't a good public one),
    # but we verify the client honours set/clear so other suites can trust it.
    reqres.set_bearer("dummy-token-for-header-check")
    assert reqres._session.headers["Authorization"] == "Bearer dummy-token-for-header-check"
    reqres.clear_bearer()
    assert "Authorization" not in reqres._session.headers
