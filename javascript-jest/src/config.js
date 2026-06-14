/**
 * Centralised endpoints + tuneables, read from the environment with
 * public-sandbox fallbacks so `npm test` works on a fresh clone.
 */
module.exports = {
  reqres: {
    baseURL: process.env.REQRES_BASE_URL || 'https://reqres.in/api',
    apiKey: process.env.REQRES_API_KEY || 'reqres-free-v1',
  },
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
