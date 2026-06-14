/**
 * Auth helpers. restful-booker hands back a token that write operations expect
 * as a `Cookie: token=...` header — not a bearer — so we expose a helper that
 * builds that header rather than leaking booker's quirk into every spec.
 */
const { createClient } = require('../clients/apiClient');
const config = require('../config');

const bookerClient = createClient({ baseURL: config.booker.baseURL });

async function getBookerToken() {
  const res = await bookerClient.post('/auth', {
    username: config.booker.username,
    password: config.booker.password,
  });
  if (res.status !== 200 || !res.data.token) {
    throw new Error(`Booker auth failed: ${res.status} ${JSON.stringify(res.data)}`);
  }
  return res.data.token;
}

function bookerAuthHeader(token) {
  return { Cookie: `token=${token}` };
}

module.exports = { getBookerToken, bookerAuthHeader };
