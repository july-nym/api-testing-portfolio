/**
 * Factory for pre-configured axios instances.
 *
 * Interceptors do two jobs here:
 *   1. Request side  — inject the reqres API key and (optionally) a bearer token.
 *   2. Response side — stamp how long the round-trip took so the toRespondWithin
 *      matcher has something to read, and let non-2xx responses resolve instead
 *      of throwing. Tests want to assert on a 404, not catch it.
 */
const axios = require('axios');

function createClient({ baseURL, apiKey, timeout = 10000 } = {}) {
  const instance = axios.create({
    baseURL,
    timeout,
    headers: { Accept: 'application/json' },
    // Resolve every response < 500 so 4xx assertions read naturally; we still
    // want 5xx to surface loudly, so they keep rejecting.
    validateStatus: (status) => status < 500,
  });

  if (apiKey) {
    instance.defaults.headers.common['x-api-key'] = apiKey;
  }

  instance.interceptors.request.use((config) => {
    config.metadata = { startedAt: Date.now() };
    // bearer token, when one has been set via setAuthToken()
    if (instance.__bearer) {
      config.headers.Authorization = `Bearer ${instance.__bearer}`;
    }
    return config;
  });

  instance.interceptors.response.use(
    (response) => {
      response.config.metadata.durationMs =
        Date.now() - response.config.metadata.startedAt;
      return response;
    },
    (error) => {
      // attach timing to errors too, so 5xx timings aren't lost
      if (error.config && error.config.metadata) {
        error.config.metadata.durationMs =
          Date.now() - error.config.metadata.startedAt;
      }
      return Promise.reject(error);
    }
  );

  instance.setAuthToken = (token) => {
    instance.__bearer = token;
  };
  instance.clearAuthToken = () => {
    delete instance.__bearer;
  };

  return instance;
}

module.exports = { createClient };
