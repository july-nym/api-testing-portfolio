"""Provider-side verification.

This replays the consumer's pact against our running provider. If the provider
ever stops returning a field the consumer reads — or changes its type — this test
goes red, on the provider's pipeline, before the change is ever deployed. That's
the payoff of contract testing: breaking changes surface at the source.

Run order:
  1. fixture boots provider_app.py on :5001
  2. Verifier POSTs each provider-state to /_pact/provider_states
  3. Verifier replays the recorded request and checks the response shape
"""
import os
import socket
import subprocess
import sys
import time
from pathlib import Path

import pytest
from pact import Verifier

PROVIDER_PORT = 5001
PROVIDER_BASE_URL = f"http://localhost:{PROVIDER_PORT}"

# Default to the checked-in pact file; a broker URL can override in CI.
PACT_FILE = (
    Path(__file__).resolve().parents[3]
    / "consumer"
    / "javascript"
    / "pacts"
    / "web-portfolio-app-user-service.json"
)


def _wait_for_port(port: int, timeout: float = 10.0) -> None:
    """Block until the provider is accepting connections (or give up)."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(("127.0.0.1", port)) == 0:
                return
        time.sleep(0.2)
    raise RuntimeError(f"Provider did not come up on port {port} within {timeout}s")


@pytest.fixture(scope="module")
def provider_process():
    app_path = Path(__file__).resolve().parents[1] / "provider_app.py"
    proc = subprocess.Popen(
        [sys.executable, str(app_path)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        _wait_for_port(PROVIDER_PORT)
        yield
    finally:
        proc.terminate()
        proc.wait(timeout=5)


def test_provider_honours_user_service_contract(provider_process):
    verifier = Verifier(
        provider="user-service",
        provider_base_url=PROVIDER_BASE_URL,
    )

    # If a broker is configured, prefer pacts from there; else use the local file.
    broker_url = os.getenv("PACT_BROKER_BASE_URL")
    if broker_url:
        success, _ = verifier.verify_with_broker(
            broker_url=broker_url,
            provider_states_setup_url=f"{PROVIDER_BASE_URL}/_pact/provider_states",
        )
    else:
        assert PACT_FILE.exists(), f"Pact file not found: {PACT_FILE}"
        success, _ = verifier.verify_pacts(
            str(PACT_FILE),
            provider_states_setup_url=f"{PROVIDER_BASE_URL}/_pact/provider_states",
        )

    assert success == 0, "Provider failed to satisfy the consumer contract"
