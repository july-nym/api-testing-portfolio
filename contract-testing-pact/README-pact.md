# Contract Testing with Pact

## Why contract testing matters

Integration tests against a live provider have two problems: they're slow and
flaky, and — worse — they only catch a breaking change **after** the provider
has already shipped it. By then the consumer is already broken in production.

Contract testing inverts the dependency. The **consumer** declares, up front,
exactly what it needs from the provider's response ("given user 2 exists, a GET
to `/users/2` returns an object with an integer `id`, an email, and a
`first_name`"). Pact captures that as a versioned JSON **contract**. The
**provider** then replays that contract in its own pipeline and fails if it can
no longer satisfy it.

The result: a provider learns it's about to break a consumer **before deploying**,
without the two services ever having to run together in a shared environment.
That's what makes it scale across teams and independently-deployed services.

Key principle: contracts assert on **type/shape**, not exact data. The consumer
doesn't care that the email is `janet.weaver@example.com` — only that it's a
string shaped like an email. This keeps contracts stable as data changes.

## The flow in this folder

```
consumer/javascript  ──(1) defines + generates pact──►  pacts/*.json
        │                                                    │
        │ (2) publish:pact                                   │
        ▼                                                    ▼
   broker/ (local Pact Broker, docker-compose)  ◄──(3) provider pulls + verifies──  provider/python
```

1. **Consumer** (`consumer/javascript`) — a Jest + Pact JS test runs the real
   `userClient` against a Pact **mock provider** and records expectations into
   `pacts/web-portfolio-app-user-service.json`.
2. **Broker** (`broker/`) — a local Pact Broker (via `docker compose up`)
   simulates the hand-off point. The consumer publishes contracts here; the
   provider pulls them down. Optional for a local run — you can verify straight
   from the file.
3. **Provider** (`provider/python`) — a pytest + pact-python test boots a tiny
   Flask stand-in for the user-service and verifies it satisfies the contract,
   using the provider-states hook to set up each precondition.

## Running it

### Consumer (generate the pact)
```bash
cd consumer/javascript
npm install
npm run test:pact          # writes pacts/web-portfolio-app-user-service.json
```

### Provider (verify against the pact)
```bash
cd provider/python
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest                     # boots provider_app.py and verifies the contract
```

### With the broker (full simulation)
```bash
cd broker && docker compose up -d        # http://localhost:9292

cd ../consumer/javascript
PACT_BROKER_BASE_URL=http://localhost:9292 npm run publish:pact

cd ../../provider/python
PACT_BROKER_BASE_URL=http://localhost:9292 pytest
```

## Why a JS consumer + Python provider?

Deliberate: it demonstrates that Pact is **language-agnostic**. A contract
authored by a Node app is verified by a Python service with no shared code —
exactly the cross-stack situation contract testing is built for.
