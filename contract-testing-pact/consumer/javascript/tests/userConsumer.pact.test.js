/**
 * Consumer contract test.
 *
 * WHY this exists: integration tests against a live provider are slow and flaky,
 * and they only fail *after* a breaking change ships. A contract test flips that
 * around — the consumer states, up front, exactly what it needs from the
 * provider ("given user 2 exists, GET /users/2 returns an object with id, email,
 * first_name"). Pact records that expectation as a JSON pact file. The provider
 * then replays it in its own pipeline, so a breaking change is caught on the
 * provider side *before* it reaches us.
 *
 * Note we match on TYPE (like('...')), not exact values. The contract is about
 * shape, not data — the provider is free to return any string email.
 */
const path = require('path');
const { PactV3, MatchersV3 } = require('@pact-foundation/pact');
const { createUserClient } = require('../src/userClient');

const { like, integer, email } = MatchersV3;

const provider = new PactV3({
  consumer: 'web-portfolio-app',
  provider: 'user-service',
  // pacts land here; the provider verification step reads them back
  dir: path.resolve(__dirname, '..', 'pacts'),
  logLevel: 'warn',
});

describe('User service contract', () => {
  it('returns the fields the consumer reads for an existing user', async () => {
    provider
      .given('user 2 exists') // provider state — the provider sets this up on its side
      .uponReceiving('a request for user 2')
      .withRequest({
        method: 'GET',
        path: '/users/2',
      })
      .willRespondWith({
        status: 200,
        headers: { 'Content-Type': 'application/json' },
        body: {
          data: {
            id: integer(2),
            email: email('janet.weaver@reqres.in'),
            first_name: like('Janet'),
          },
        },
      });

    await provider.executeTest(async (mockServer) => {
      const client = createUserClient(mockServer.url);
      const user = await client.getUserById(2);

      // Assert our client maps the response the way the app depends on
      expect(user.id).toBe(2);
      expect(user.email).toContain('@');
      expect(user.firstName).toBe('Janet');
    });
  });
});
