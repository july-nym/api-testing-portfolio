# javascript-jest

API test suite built with **JavaScript + axios + Jest + jest-extended**.

## Highlights
- Axios instances with request/response **interceptors** (API-key + bearer injection, latency timing)
- Custom Jest matchers (`toHaveStatus`, `toRespondWithin`) plus jest-extended
- Schema validation with **Ajv** (+ ajv-formats for `email` etc.)
- `beforeAll` / `afterAll` for token setup and sandbox cleanup
- Negative and edge-case coverage (400 / 403 / 404, contract quirks)
- Selective runs via `jest --testPathPattern`

## Run it
```bash
npm install

npm test                              # full suite
npx jest --testPathPattern=auth       # just auth specs
npm run test:negative                 # negative.test.js only
npm run test:ci                       # serial, CI reporter
```

Defaults hit the public sandboxes; copy `.env.example` to `.env` to retarget.

## Layout
```
src/clients/apiClient.js     axios factory + interceptors
src/helpers/authHelper.js    booker token + cookie header, reqres login
src/helpers/dataHelper.js    realistic test-data builders
src/helpers/schemaValidator.js  Ajv validation + schemas
src/config.js                env-driven endpoints
tests/                       auth / users / bookings / negative
```
