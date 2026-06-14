/**
 * Centralised endpoints + tuneables, read from the environment with
 * public-sandbox fallbacks so `npm test` works on a fresh clone.
 *
 * Both targets are keyless: jsonplaceholder for user reads + post CRUD, and
 * restful-booker for real auth + a stateful booking lifecycle.
 */
module.exports = {
  jsonplaceholder: {
    baseURL:
      process.env.JSONPLACEHOLDER_BASE_URL || 'https://jsonplaceholder.typicode.com',
  },
  booker: {
    baseURL: process.env.BOOKER_BASE_URL || 'https://restful-booker.herokuapp.com',
    username: process.env.BOOKER_USER || 'admin',
    password: process.env.BOOKER_PASSWORD || 'password123',
  },
  // SLA used by the toRespondWithin matcher (ms)
  maxResponseMs: Number(process.env.MAX_RESPONSE_MS || 2000),
};
