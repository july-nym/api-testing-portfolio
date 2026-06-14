const { createClient } = require('../src/clients/apiClient');
const { buildBooking } = require('../src/helpers/dataHelper');
const config = require('../src/config');

describe('Negative and edge cases', () => {
  let api;
  let booker;

  beforeAll(() => {
    api = createClient({ baseURL: config.jsonplaceholder.baseURL });
    booker = createClient({ baseURL: config.booker.baseURL });
  });

  test.each([11, 99, 999])('unknown user id %i returns 404', async (id) => {
    // jsonplaceholder only seeds 10 users; anything beyond is a 404
    const res = await api.get(`/users/${id}`);
    expect(res).toHaveStatus(404);
  });

  test('unknown post returns 404', async () => {
    const res = await api.get('/posts/9999');
    expect(res).toHaveStatus(404);
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

  test('fetching a non-existent booking returns 404', async () => {
    const res = await booker.get('/booking/99999999');
    expect(res).toHaveStatus(404);
  });
});
