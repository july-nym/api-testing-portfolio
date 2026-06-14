/**
 * Publishes generated pacts to a broker.
 *
 * In a real setup this points at a hosted Pact Broker (or PactFlow). For this
 * portfolio we run the broker locally via docker-compose (see broker/), so the
 * default URL is localhost. The broker is the hand-off point: consumers publish
 * their expectations here, providers pull them down to verify. It's what makes
 * contract testing work across separately-deployed services and teams.
 */
const path = require('path');
const { Publisher } = require('@pact-foundation/pact');

const brokerBaseUrl = process.env.PACT_BROKER_BASE_URL || 'http://localhost:9292';

const opts = {
  pactFilesOrDirs: [path.resolve(__dirname, '..', 'pacts')],
  pactBroker: brokerBaseUrl,
  // tag with the branch/commit so the provider can verify the right version
  consumerVersion: process.env.GIT_SHA || '0.0.0-local',
  tags: [process.env.GIT_BRANCH || 'local'],
};

new Publisher(opts)
  .publishPacts()
  .then(() => console.log(`Published pacts to ${brokerBaseUrl}`))
  .catch((err) => {
    console.error('Pact publish failed:', err.message);
    process.exit(1);
  });
