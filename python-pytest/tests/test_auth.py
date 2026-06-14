"""Authentication flows against restful-booker.

booker is the one public sandbox here that issues a real session token, so it
carries the auth coverage: a happy-path token issue that the write tests depend
on, plus the negative paths around bad/again-missing credentials.
"""
import pytest

from utils.assertions import assert_status


@pytest.mark.smoke
def test_auth_issues_token(booker, settings):
    resp = booker.post(
        "/auth",
        json={"username": settings.booker_user, "password": settings.booker_password},
    )
    assert_status(resp, 200)
    # No response-time SLA here on purpose: restful-booker runs on a free dyno
    # that cold-starts, so a tight latency gate on auth would just flake. The SLA
    # is asserted against the fast jsonplaceholder reads instead.
    assert resp.json().get("token"), "Expected a token in the auth response"


@pytest.mark.smoke
def test_token_fixture_is_reusable(booker_token):
    # The fixture already asserted success; this documents the contract and gives
    # us a named smoke test in the report.
    assert isinstance(booker_token, str)
    assert len(booker_token) >= 10


@pytest.mark.negative
def test_bad_credentials_return_reason(booker):
    resp = booker.post(
        "/auth", json={"username": "admin", "password": "wrong-password"}
    )
    # booker answers 200 with a "reason" body rather than a 401 — pin it so a
    # future contract change is caught.
    assert_status(resp, 200)
    assert resp.json().get("reason") == "Bad credentials"


@pytest.mark.negative
def test_missing_password_is_rejected(booker):
    resp = booker.post("/auth", json={"username": "admin"})
    assert_status(resp, 200)
    assert resp.json().get("reason") == "Bad credentials"


@pytest.mark.negative
def test_bearer_can_be_attached_and_cleared(booker):
    # Verify the client honours set/clear so other suites can trust it.
    booker.set_bearer("dummy-token-for-header-check")
    assert booker._session.headers["Authorization"] == "Bearer dummy-token-for-header-check"
    booker.clear_bearer()
    assert "Authorization" not in booker._session.headers
