/**
 * Global test setup. Loads env vars and registers a couple of project-specific
 * matchers that read better than chaining generic assertions.
 */
require('dotenv').config();

expect.extend({
  // expect(response).toHaveStatus(200) — one matcher, a body dump on failure
  toHaveStatus(received, expected) {
    const pass = received && received.status === expected;
    return {
      pass,
      message: () =>
        pass
          ? `expected status not to be ${expected}`
          : `expected status ${expected} but got ${received && received.status}\n` +
            `body: ${JSON.stringify(received && received.data)}`,
    };
  },

  // expect(response).toRespondWithin(2000)
  toRespondWithin(received, maxMs) {
    const elapsed = received && received.config && received.config.metadata
      ? received.config.metadata.durationMs
      : undefined;
    const pass = typeof elapsed === 'number' && elapsed <= maxMs;
    return {
      pass,
      message: () =>
        pass
          ? `expected request to exceed ${maxMs}ms`
          : `expected response within ${maxMs}ms but took ${elapsed}ms`,
    };
  },
});
