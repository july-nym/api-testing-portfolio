const { createClient } = require('../src/clients/apiClient');
const { getBookerToken, loginToReqres } = require('../src/helpers/authHelper');
const config = require('../src/config');

describe('Authentication', () => {
  let reqres;

  beforeAll(() => {
    reqres = createClient({
      baseURL: config.reqres.baseURL,
      apiKey: config.reqres.apiKey,
    });
  });

  test('seeded reqres user receives a token on login', async () => {
    const token = await loginToReqres(reqres, 'eve.holt@reqres.in', 'cityslicka');
    expect(token).toBeString();
    expect(token.length).toBeGreaterThan(10);
  });

  test('register returns a fixed id and a token', async () => {
    const res = await reqres.post('/register', {
      email: 'eve.holt@reqres.in',
      password: 'pistol',
    });
    expect(res).toHaveStatus(200);
    expect(res.data).toContainKeys(['id', 'token']);
    expect(res.data.id).toBe(4);
  });

  test('booker issues a usable token', async () => {
    const token = await getBookerToken();
    expect(token).toBeString();
  });

  test('axios interceptor injects a bearer token once set', async () => {
    reqres.setAuthToken('header-injection-check');
    // /users/2 doesn't require auth, but we can read the outgoing header back
    // off the response config to prove the interceptor fired.
    const res = await reqres.get('/users/2');
    expect(res.config.headers.Authorization).toBe('Bearer header-injection-check');
    reqres.clearAuthToken();
  });
});
