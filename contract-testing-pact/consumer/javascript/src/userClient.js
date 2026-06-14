/**
 * The consumer's view of the user service.
 *
 * This is the real client code our app would ship — the Pact test points it at
 * a mock provider instead of the live host. Whatever shape this client depends
 * on becomes the contract, which is the whole idea: the consumer declares what
 * it actually needs, nothing more.
 */
const axios = require('axios');

function createUserClient(baseURL) {
  const http = axios.create({ baseURL, headers: { Accept: 'application/json' } });

  return {
    async getUserById(id) {
      const res = await http.get(`/users/${id}`);
      // We only consume these three fields — so these are all we'll contract for.
      const { id: userId, email, first_name: firstName } = res.data.data;
      return { id: userId, email, firstName };
    },
  };
}

module.exports = { createUserClient };
