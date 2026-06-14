const { createClient } = require('../src/clients/apiClient');
const { getBookerToken } = require('../src/helpers/authHelper');
const config = require('../src/config');

describe('Authentication (restful-booker)', () => {
  let booker;

  beforeAll(() => {
    booker = createClient({ baseURL: config.booker.baseURL });
  });

  test('valid credentials issue a usable token', async () => {
    const token = await getBookerToken();
    expect(token).toBeString();
    expect(token.length).toBeGreaterThan(10);
  });

  test('bad credentials come back as a reason, not a 401', async () => {
    const res = await booker.post('/auth', {
      username: 'admin',
      password: 'definitely-wrong',
    });
    // booker answers 200 with a reason body — a quirk worth pinning
    expect(res).toHaveStatus(200);
    expect(res.data.reason).toBe('Bad credentials');
  });

  test('axios interceptor injects a bearer token once set', async () => {
    booker.setAuthToken('header-injection-check');
    // any GET works; we read the outgoing header back off the response config
    const res = await booker.get('/ping');
    expect(res.config.headers.Authorization).toBe('Bearer header-injection-check');
    booker.clearAuthToken();
  });
});
