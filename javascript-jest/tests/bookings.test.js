const { createClient } = require('../src/clients/apiClient');
const { getBookerToken, bookerAuthHeader } = require('../src/helpers/authHelper');
const { buildBooking } = require('../src/helpers/dataHelper');
const { validate, bookingCreateSchema } = require('../src/helpers/schemaValidator');
const config = require('../src/config');

describe('Booking lifecycle (restful-booker)', () => {
  let booker;
  let authHeader;
  // ids we create so afterAll can tidy up after itself
  const createdIds = [];

  beforeAll(async () => {
    booker = createClient({ baseURL: config.booker.baseURL });
    const token = await getBookerToken();
    authHeader = bookerAuthHeader(token);
  });

  afterAll(async () => {
    // Be a good sandbox citizen: remove anything the suite left behind.
    await Promise.all(
      createdIds.map((id) =>
        booker.delete(`/booking/${id}`, { headers: authHeader }).catch(() => {})
      )
    );
  });

  test('create returns an id and a schema-valid body', async () => {
    const res = await booker.post('/booking', buildBooking());
    expect(res).toHaveStatus(200);

    const { valid, errors } = validate(bookingCreateSchema, res.data);
    expect(valid).toBe(true);
    expect(errors).toBeArrayOfSize(0);

    createdIds.push(res.data.bookingid);
  });

  test('create → read → update → delete → 404', async () => {
    const created = await booker.post('/booking', buildBooking({ lastname: 'Nakamura' }));
    const id = created.data.bookingid;

    const read = await booker.get(`/booking/${id}`);
    expect(read).toHaveStatus(200);
    expect(read.data.lastname).toBe('Nakamura');

    const replacement = buildBooking({ lastname: 'Nakamura', totalprice: 1999 });
    const updated = await booker.put(`/booking/${id}`, replacement, {
      headers: authHeader,
    });
    expect(updated).toHaveStatus(200);
    expect(updated.data.totalprice).toBe(1999);

    const deleted = await booker.delete(`/booking/${id}`, { headers: authHeader });
    expect(deleted).toHaveStatus(201); // booker's odd-but-real delete status

    const gone = await booker.get(`/booking/${id}`);
    expect(gone).toHaveStatus(404);
  });

  test('PATCH updates only the targeted field', async () => {
    const created = await booker.post('/booking', buildBooking());
    const id = created.data.bookingid;
    createdIds.push(id);

    const patched = await booker.patch(
      `/booking/${id}`,
      { additionalneeds: 'Airport transfer' },
      { headers: authHeader }
    );
    expect(patched).toHaveStatus(200);
    expect(patched.data.additionalneeds).toBe('Airport transfer');
    expect(patched.data.firstname).toBe('Priya'); // untouched field survives
  });
});
