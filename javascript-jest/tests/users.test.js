const { createClient } = require('../src/clients/apiClient');
const { buildReqresUser } = require('../src/helpers/dataHelper');
const { validate, singleUserSchema } = require('../src/helpers/schemaValidator');
const config = require('../src/config');

describe('Users (reqres) + cross-host read (jsonplaceholder)', () => {
  let reqres;
  let placeholder;

  beforeAll(() => {
    reqres = createClient({
      baseURL: config.reqres.baseURL,
      apiKey: config.reqres.apiKey,
    });
    placeholder = createClient({ baseURL: config.jsonplaceholder.baseURL });
  });

  test('GET single user matches schema and SLA', async () => {
    const res = await reqres.get('/users/2');
    expect(res).toHaveStatus(200);
    expect(res).toRespondWithin(config.maxResponseMs);

    const { valid, errors } = validate(singleUserSchema, res.data);
    expect(valid).toBe(true);
    // errors is [] when valid; printing it makes a failure self-explanatory
    expect(errors).toBeArrayOfSize(0);
  });

  test.each([1, 2])('user list page %i is well-formed', async (page) => {
    const res = await reqres.get('/users', { params: { page } });
    expect(res).toHaveStatus(200);
    expect(res.data.page).toBe(page);
    expect(res.data.data.length).toBeLessThanOrEqual(res.data.per_page);
  });

  test('POST create echoes the payload and adds an id', async () => {
    const candidate = buildReqresUser({ job: 'QA Lead' });
    const res = await reqres.post('/users', candidate);

    expect(res).toHaveStatus(201);
    expect(res.data.name).toBe(candidate.name);
    expect(res.data.job).toBe('QA Lead');
    expect(res.data).toContainKeys(['id', 'createdAt']);
  });

  test('PUT replaces, PATCH partially updates', async () => {
    const put = await reqres.put('/users/2', buildReqresUser({ job: 'Principal QA' }));
    expect(put).toHaveStatus(200);
    expect(put.data.job).toBe('Principal QA');

    const patch = await reqres.patch('/users/2', { job: 'Engineering Manager' });
    expect(patch).toHaveStatus(200);
    expect(patch.data.job).toBe('Engineering Manager');
  });

  test('DELETE returns 204 with no body', async () => {
    const res = await reqres.delete('/users/2');
    expect(res).toHaveStatus(204);
    expect(res.data).toBeFalsy();
  });

  test('jsonplaceholder seeds exactly 10 users', async () => {
    const res = await placeholder.get('/users');
    expect(res).toHaveStatus(200);
    expect(res.data).toBeArrayOfSize(10);
  });
});
