"""Environment-driven configuration.

Everything that changes between local runs and CI lives here so the test code
never hard-codes a base URL or a credential. Defaults point at the public
sandboxes, which keeps the suite runnable out of the box without a .env file.

Targets:
  * jsonplaceholder — keyless, stable; used for user reads + post CRUD.
  * restful-booker  — real auth + stateful create/read/update/delete.
Both are public and need no API key, so a fresh clone runs green with no secrets.
"""
import os
from dataclasses import dataclass
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()  # no-op in CI where vars come from the environment directly


@dataclass(frozen=True)
class Settings:
    # jsonplaceholder backs the user/post CRUD + schema checks
    jsonplaceholder_base_url: str

    # restful-booker is where we exercise real create/update/delete + auth
    booker_base_url: str
    booker_user: str
    booker_password: str

    # global ceiling for response-time *assertions* (milliseconds) — a tight gate
    max_response_ms: int

    # hard network timeout (milliseconds). Deliberately decoupled from the SLA and
    # set generously: restful-booker runs on a free dyno that can take 10-30s to
    # cold-start, and a 6s timeout would fail the first call of a fresh CI run.
    request_timeout_ms: int

    @property
    def request_timeout(self) -> float:
        # requests wants seconds; we think in ms everywhere else
        return self.request_timeout_ms / 1000


@lru_cache
def get_settings() -> Settings:
    return Settings(
        jsonplaceholder_base_url=os.getenv(
            "JSONPLACEHOLDER_BASE_URL", "https://jsonplaceholder.typicode.com"
        ),
        booker_base_url=os.getenv(
            "BOOKER_BASE_URL", "https://restful-booker.herokuapp.com"
        ),
        booker_user=os.getenv("BOOKER_USER", "admin"),
        booker_password=os.getenv("BOOKER_PASSWORD", "password123"),
        max_response_ms=int(os.getenv("MAX_RESPONSE_MS", "2000")),
        request_timeout_ms=int(os.getenv("REQUEST_TIMEOUT_MS", "30000")),
    )
