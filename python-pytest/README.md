# python-pytest

API test suite built with **Python + requests + pytest**.

## What it covers
- Full CRUD against restful-booker (create → read → update → delete → confirm gone)
- Auth flows on reqres and a reusable booker token fixture
- JSON schema validation (`jsonschema`)
- Parameterised tests (`pytest.mark.parametrize`)
- Negative paths: 400 / 401 / 403 / 404 and contract-quirk pinning
- Response-time assertions against a configurable SLA
- Custom markers: `smoke`, `regression`, `negative`

## Run it
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

pytest                       # everything
pytest -m smoke              # quick health check
pytest -m "regression and not negative"
pytest -n auto               # parallel (pytest-xdist)
```

Defaults target the public sandboxes, so no `.env` is required. Copy
`.env.example` to `.env` to point at a different environment.

## Layout
```
config/settings.py   env-driven configuration
utils/api_client.py  requests.Session wrapper with latency capture
utils/assertions.py  assertion helpers with useful failure messages
utils/schemas.py     JSON schemas for response validation
conftest.py          session-scoped clients + booker token fixture
tests/               test_auth / test_users / test_bookings / test_negative_cases
```
