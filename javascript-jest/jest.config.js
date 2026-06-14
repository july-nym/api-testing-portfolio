/**
 * Jest config.
 *
 * setupFilesAfterEnv wires in jest-extended's matchers (toBeOneOf, toContainKey,
 * …) and our own custom matchers so every spec gets them without an import.
 * testTimeout is generous because we're hitting live public sandboxes that
 * occasionally cold-start (restful-booker runs on a free Heroku dyno).
 */
module.exports = {
  testEnvironment: 'node',
  setupFilesAfterEnv: ['jest-extended/all', '<rootDir>/jest.setup.js'],
  testMatch: ['**/tests/**/*.test.js'],
  testTimeout: 15000,
  verbose: true,
  // Don't stop the world on the first failure — we want the full picture in CI
  bail: false,
};
