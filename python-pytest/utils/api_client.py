"""Thin wrapper around requests.Session.

The point of this class is to centralise three things that otherwise get
copy-pasted into every test: the base URL, the default headers, and a single
place to capture how long the call took. Tests stay readable because they only
deal in paths and payloads. An optional API key is still supported for any host
that needs one, even though the current targets are keyless.
"""
from __future__ import annotations

import time
from typing import Any, Mapping, Optional

import requests


class ApiClient:
    def __init__(
        self,
        base_url: str,
        *,
        api_key: Optional[str] = None,
        timeout: float = 10.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._session = requests.Session()
        # An x-api-key rides on every request when one is supplied — kept generic
        # so the client works against a key-gated host without code changes.
        if api_key:
            self._session.headers["x-api-key"] = api_key
        self._session.headers["Accept"] = "application/json"

    def _url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    def set_bearer(self, token: str) -> None:
        """Attach a bearer token for the rest of the session."""
        self._session.headers["Authorization"] = f"Bearer {token}"

    def clear_bearer(self) -> None:
        self._session.headers.pop("Authorization", None)

    def request(
        self,
        method: str,
        path: str,
        *,
        json: Any = None,
        params: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> requests.Response:
        start = time.perf_counter()
        response = self._session.request(
            method.upper(),
            self._url(path),
            json=json,
            params=params,
            headers=headers,
            timeout=self.timeout,
        )
        # stash the measured latency on the response object itself so assertion
        # helpers can read it without us inventing a parallel return type.
        elapsed_ms = (time.perf_counter() - start) * 1000
        response.elapsed_ms = elapsed_ms  # type: ignore[attr-defined]
        return response

    def get(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("PUT", path, **kwargs)

    def patch(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("DELETE", path, **kwargs)

    def close(self) -> None:
        self._session.close()
