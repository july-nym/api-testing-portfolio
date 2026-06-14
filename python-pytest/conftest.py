"""Shared fixtures and session setup.

Scope choices matter here: the API clients are session-scoped because building a
requests.Session per test is wasteful and the sandboxes are stateless enough to
share one. The booker auth token is also session-scoped — restful-booker tokens
are valid for the run, so re-authenticating per test would just hammer the
sandbox for no benefit.
"""
from __future__ import annotations

import pytest

from config.settings import get_settings
from utils.api_client import ApiClient


@pytest.fixture(scope="session")
def settings():
    return get_settings()


@pytest.fixture(scope="session")
def jsonplaceholder(settings):
    client = ApiClient(
        settings.jsonplaceholder_base_url, timeout=settings.request_timeout
    )
    yield client
    client.close()


@pytest.fixture(scope="session")
def booker(settings):
    client = ApiClient(settings.booker_base_url, timeout=settings.request_timeout)
    yield client
    client.close()


@pytest.fixture(scope="session")
def booker_token(booker, settings) -> str:
    """Authenticate once against restful-booker and reuse the token.

    The token goes in a Cookie header for write operations (booker's quirk),
    which the individual tests build themselves — here we just hand back the raw
    token string.
    """
    resp = booker.post(
        "/auth",
        json={"username": settings.booker_user, "password": settings.booker_password},
    )
    assert resp.status_code == 200, f"Auth setup failed: {resp.text}"
    token = resp.json().get("token")
    assert token, "Auth succeeded but no token came back"
    return token


@pytest.fixture
def new_booking_payload():
    """A fresh, realistic booking body for create tests.

    Returned from a fixture (not a module constant) so a test that mutates it
    can't bleed state into the next one.
    """
    return {
        "firstname": "Mariana",
        "lastname": "Okafor",
        "totalprice": 845,
        "depositpaid": True,
        "bookingdates": {"checkin": "2026-09-12", "checkout": "2026-09-19"},
        "additionalneeds": "Late checkout",
    }


@pytest.fixture
def new_post_payload():
    """A realistic jsonplaceholder post body for create/update tests."""
    return {
        "title": "Regression sign-off checklist",
        "body": "Smoke green, schema stable, no P1 regressions on the release branch.",
        "userId": 7,
    }
