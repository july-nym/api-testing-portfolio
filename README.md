# API Testing Portfolio

A multi-stack API test automation portfolio: the same set of REST APIs exercised
across **four languages/frameworks** plus **consumer-driven contract testing**,
each wired into CI. It's built to show how I'd approach test architecture, not
just that I can write an assertion — fixtures and clients are shared, config is
environment-driven, and every suite runs headless on push.

[![python-tests](https://github.com/july-nym/api-testing-portfolio/actions/workflows/python-tests.yml/badge.svg)](https://github.com/july-nym/api-testing-portfolio/actions/workflows/python-tests.yml)
[![javascript-tests](https://github.com/july-nym/api-testing-portfolio/actions/workflows/javascript-tests.yml/badge.svg)](https://github.com/july-nym/api-testing-portfolio/actions/workflows/javascript-tests.yml)
[![java-tests](https://github.com/july-nym/api-testing-portfolio/actions/workflows/java-tests.yml/badge.svg)](https://github.com/july-nym/api-testing-portfolio/actions/workflows/java-tests.yml)
[![newman-tests](https://github.com/july-nym/api-testing-portfolio/actions/workflows/newman-tests.yml/badge.svg)](https://github.com/july-nym/api-testing-portfolio/actions/workflows/newman-tests.yml)
[![pact-tests](https://github.com/july-nym/api-testing-portfolio/actions/workflows/pact-tests.yml/badge.svg)](https://github.com/july-nym/api-testing-portfolio/actions/workflows/pact-tests.yml)

## Targets under test

All public, no signup required — the suites run on a fresh clone:

| API | Used for |
| --- | --- |
| [reqres.in](https://reqres.in) | Auth + user CRUD (primary) |
| [jsonplaceholder.typicode.com](https://jsonplaceholder.typicode.com) | Read-mostly cross-host checks (secondary) |
| [restful-booker](https://restful-booker.herokuapp.com) | Stateful create/read/update/delete lifecycle |

## Tech stack

| Folder | Stack | Demonstrates |
| --- | --- | --- |
| [`python-pytest/`](python-pytest) | Python · requests · pytest · jsonschema | Fixtures, parametrize, custom markers, response-time SLAs |
| [`javascript-jest/`](javascript-jest) | JavaScript · axios · Jest · jest-extended · Ajv | Interceptors, custom matchers, schema validation, setup/teardown |
| [`java-rest-assured/`](java-rest-assured) | Java 17 · REST Assured · TestNG · Maven · Lombok · Allure | Given/When/Then, POJO (de)serialization, groups, Maven profiles |
| [`contract-testing-pact/`](contract-testing-pact) | Pact JS (consumer) · pact-python (provider) | Consumer-driven contracts across two languages + a local broker |
| [`postman/`](postman) | Postman · Newman | Collection-based tests, env files, headless CI runs |

## Quick start

Each folder is self-contained and ships sensible public-sandbox defaults, so no
`.env` is required to get a green run. Override via the `.env.example` in each
folder when pointing at a different environment.

```bash
# Python
cd python-pytest && pip install -r requirements.txt && pytest

# JavaScript
cd javascript-jest && npm install && npm test

# Java
cd java-rest-assured && mvn test

# Postman / Newman
cd postman && ./run-newman.sh dev

# Contract testing (consumer generates, provider verifies)
cd contract-testing-pact/consumer/javascript && npm install && npm run test:pact
cd ../../provider/python && pip install -r requirements.txt && pytest
```

Or drive everything from the repo root via the `Makefile`:

```bash
make install     # deps for every stack
make smoke       # fast smoke subset across stacks
make test        # full suite, every stack
make py-test     # or a single stack: py-/js-/java-test, newman, pact
```

## Why contract testing?

End-to-end integration tests between services are slow, flaky, and — the real
problem — they only fail **after** a breaking change has shipped. Contract
testing moves that signal earlier and to the right place.

The **consumer** declares exactly what it needs from a provider's response (an
integer `id`, an email-shaped string, a `first_name`). [Pact](https://docs.pact.io)
records that as a versioned contract. The **provider** then replays it in its own
pipeline and fails if it can no longer satisfy it — so a team learns it's about
to break a downstream consumer **before deploying**, without the two services
ever sharing a test environment.

In this repo a **JavaScript** consumer contract is verified by a **Python**
provider on purpose: it shows Pact is language-agnostic, which is the whole point
when independently-deployed services are owned by different teams. Full
walkthrough in [`contract-testing-pact/README-pact.md`](contract-testing-pact/README-pact.md).

## CI/CD

Every stack has its own GitHub Actions workflow under
[`.github/workflows/`](.github/workflows), triggered on push to `main` and on
pull requests, and path-filtered so a change to the Java suite doesn't rerun the
Python one. Highlights:

- **Python** runs against a 3.11 / 3.12 matrix; smoke gate before the full suite.
- **Java** runs the smoke profile first, then the full TestNG suite, archiving Surefire reports.
- **Pact** runs the consumer and provider as **separate sequential jobs**, passing the generated pact as an artifact — mirroring two real, independent pipelines.
- **Newman** uploads a JUnit report so per-request results show up in the run.

## Skills demonstrated

For recruiters and hiring managers — what this portfolio is evidence of:

- **Test architecture across stacks** — reusable HTTP clients, shared fixtures, environment-driven config, and a clean separation of test data from test logic, repeated idiomatically in four ecosystems.
- **API testing depth** — full CRUD lifecycles, auth/token handling, JSON schema validation, response-time SLAs, and deliberate negative coverage (400/401/403/404/500) including pinning a provider's known quirks so a future regression is caught.
- **Modern contract testing** — consumer-driven contracts with Pact across two languages and a broker, the approach used to keep microservices safe to deploy independently.
- **CI/CD ownership** — per-stack pipelines, build matrices, smoke-then-full gating, artifact retention, and path filtering — i.e. test suites that earn their place in a delivery pipeline, not just on a laptop.
- **Engineering judgement** — realistic test data, meaningful assertion messages, and comments that explain the *why* behind non-obvious choices (provider quirks, header conventions, fixture scope).

## Repository layout

```
.
├── python-pytest/          requests + pytest
├── javascript-jest/        axios + Jest
├── java-rest-assured/      REST Assured + TestNG + Maven
├── contract-testing-pact/  Pact consumer (JS) + provider (Python) + broker
├── postman/                collection, environments, Newman runner
└── .github/workflows/      one CI pipeline per stack
```

---

> Targets are public sandboxes; credentials shown are their documented public
> test credentials, not secrets. All test data is fictional.
