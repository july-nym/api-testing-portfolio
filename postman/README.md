# postman

Postman collection for jsonplaceholder + restful-booker, runnable headless via
**Newman**.

## Contents
- `api-portfolio.postman_collection.json` — user reads, post create, schema
  checks, and a full booking auth → create → update → delete lifecycle. Tests are
  written in the request `test` scripts (status, schema, response-time, value
  assertions).
- `environments/dev.*` / `environments/staging.*` — per-env variables.
- `run-newman.sh` — CLI runner that emits a CLI summary + JUnit XML.

## Run it
```bash
npm install -g newman          # one-off
./run-newman.sh                # dev
./run-newman.sh staging        # staging

# or directly:
newman run api-portfolio.postman_collection.json \
  --environment environments/dev.postman_environment.json
```

State flows between requests via environment/collection variables — the booking
id captured on create is reused by the update and delete steps, so the suite
runs as a self-contained lifecycle. CI runs this on every push (see
`.github/workflows/newman-tests.yml`).
