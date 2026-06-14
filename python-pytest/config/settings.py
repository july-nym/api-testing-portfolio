"""Environment-driven configuration.

Everything that changes between local runs and CI lives here so the test code
never hard-codes a base URL or a credential. Defaults point at the public
sandboxes, which keeps the suite runnable out of the box without a .env file.
"""
import os
from dataclasses import dataclass
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()  # no-op in CI where vars come from the environment directly


@dataclass(frozen=True)
class Settings:
    # reqres is our primary target for auth + user CRUD
    reqres_base_url: str
    # reqres started gating writes behind a free key in 2024 — keep it configurable
    reqres_api_key: str

    # jsonplaceholder is read-mostly, handy for schema + pagination checks
    jsonplaceholder_base_url: str

    # restful-booker is where we exercise real create/update/delete flows
    booker_base_url: str
    booker_user: str
    booker_password: str

    # global ceiling for response-time assertions (milliseconds)
    max_response_ms: int

    @property
    def request_timeout(self) -> float:
        # requests wants seconds; we think in ms everywhere else
        return self.max_response_ms / 1000 * 3  # allow 3x the SLA before we hard-fail


@lru_cache
def get_settings() -> Settings:
    return Settings(
        reqres_base_url=os.getenv("REQRES_BASE_URL", "https://reqres.in/api"),
        reqres_api_key=os.getenv("REQRES_API_KEY", "reqres-free-v1"),
        jsonplaceholder_base_url=os.getenv(
            "JSONPLACEHOLDER_BASE_URL", "https://jsonplaceholder.typicode.com"
        ),
        booker_base_url=os.getenv(
            "BOOKER_BASE_URL", "https://restful-booker.herokuapp.com"
        ),
        booker_user=os.getenv("BOOKER_USER", "admin"),
        booker_password=os.getenv("BOOKER_PASSWORD", "password123"),
        max_response_ms=int(os.getenv("MAX_RESPONSE_MS", "2000")),
    )
