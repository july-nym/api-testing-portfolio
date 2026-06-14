const { createClient } = require('../src/clients/apiClient');
const { buildBooking } = require('../src/helpers/dataHelper');
const config = require('../src/config');

describe('Negative and edge cases', () => {
  let reqres;
  let booker;
  let placeholder;

  beforeAll(() => {
    reqres = createClient({
      baseURL: config.reqres.baseURL,
      apiKey: config.reqres.apiKey,
    });
    booker = createClient({ baseURL: config.booker.baseURL });
    placeholder = createClient({ baseURL: config.jsonplaceholder.baseURL });
  });

  test('login without password is a 400 with a clear reason', async () => {
    const res = await reqres.post('/login', { email: 'peter.holt@reqres.in' });
    expect(res).toHaveStatus(400);
    expect(res.data.error).toBe('Missing password');
  });

  test('registering an unseeded email is rejected', async () => {
    const res = await reqres.post('/register', {
      email: 'stranger@example.com',
      password: 'x',
    });
    expect(res).toHaveStatus(400);
  });

  test.each([0, 23, 999])('unknown reqres user id %i returns 404', async (id) => {
    const res = await reqres.get(`/users/${id}`);
    expect(res).toHaveStatus(404);
    expect(res.data).toEqual({});
  });

  test('booker rejects a write with no auth cookie (403)', async () => {
    const created = await booker.post('/booking', buildBooking());
    const id = created.data.bookingid;

    const res = await booker.put(`/booking/${id}`, buildBooking());
    expect(res).toHaveStatus(403);
  });

  test('booker bad credentials come back as a reason, not a 401', async () => {
    const res = await booker.post('/auth', {
      username: 'admin',
      password: 'definitely-wrong',
    });
    expect(res).toHaveStatus(200);
    expect(res.data.reason).toBe('Bad credentials');
  });

  test('unknown jsonplaceholder resource returns 404', async () => {
    const res = await placeholder.get('/posts/9999');
    expect(res).toHaveStatus(404);
  });
});
