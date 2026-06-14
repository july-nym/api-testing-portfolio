"""Custom assertion helpers.

These exist to turn repetitive checks into one-liners that produce a useful
failure message. A bare `assert resp.status_code == 200` tells you almost
nothing when it fails at 2am in CI; these dump the body so you can triage from
the log alone.
"""
from __future__ import annotations

from typing import Any

import jsonschema
from requests import Response


def assert_status(response: Response, expected: int) -> None:
    if response.status_code != expected:
        raise AssertionError(
            f"Expected HTTP {expected} but got {response.status_code} "
            f"for {response.request.method} {response.url}\n"
            f"Body: {_safe_body(response)}"
        )


def assert_response_under(response: Response, max_ms: int) -> None:
    measured = getattr(response, "elapsed_ms", None)
    if measured is None:
        # fall back to requests' own timer if the client wrapper wasn't used
        measured = response.elapsed.total_seconds() * 1000
    if measured > max_ms:
        raise AssertionError(
            f"{response.request.method} {response.url} took {measured:.0f}ms, "
            f"SLA is {max_ms}ms"
        )


def assert_matches_schema(payload: Any, schema: dict) -> None:
    try:
        jsonschema.validate(instance=payload, schema=schema)
    except jsonschema.ValidationError as exc:
        # re-raise as AssertionError so pytest treats it as a failure, not an error
        raise AssertionError(
            f"Schema validation failed at {list(exc.absolute_path)}: {exc.message}"
        ) from exc


def assert_has_keys(payload: dict, *keys: str) -> None:
    missing = [k for k in keys if k not in payload]
    if missing:
        raise AssertionError(f"Response is missing expected keys: {missing}")


def _safe_body(response: Response) -> str:
    text = response.text or "<empty>"
    return text if len(text) <= 500 else text[:500] + "…(truncated)"
