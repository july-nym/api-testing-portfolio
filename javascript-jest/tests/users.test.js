const { createClient } = require('../src/clients/apiClient');
const { buildPost } = require('../src/helpers/dataHelper');
const {
  validate,
  singleUserSchema,
  postCreateSchema,
} = require('../src/helpers/schemaValidator');
const config = require('../src/config');

describe('Users + post CRUD (jsonplaceholder)', () => {
  let api;

  beforeAll(() => {
    api = createClient({ baseURL: config.jsonplaceholder.baseURL });
  });

  test('GET single user matches schema and SLA', async () => {
    const res = await api.get('/users/2');
    expect(res).toHaveStatus(200);
    expect(res).toRespondWithin(config.maxResponseMs);

    const { valid, errors } = validate(singleUserSchema, res.data);
    expect(valid).toBe(true);
    // errors is [] when valid; printing it makes a failure self-explanatory
    expect(errors).toBeArrayOfSize(0);
  });

  test('user directory has exactly 10 seeded users', async () => {
    const res = await api.get('/users');
    expect(res).toHaveStatus(200);
    expect(res.data).toBeArrayOfSize(10);
  });

  test.each([1, 2])('post page %i respects the page limit', async (page) => {
    const limit = 10;
    const res = await api.get('/posts', { params: { _page: page, _limit: limit } });
    expect(res).toHaveStatus(200);
    expect(res.data.length).toBeLessThanOrEqual(limit);
    // jsonplaceholder advertises the full count in a header, not the body
    expect(res.headers['x-total-count']).toBe('100');
  });

  test('POST create echoes the payload and adds an id', async () => {
    const draft = buildPost({ title: 'Release approved' });
    const res = await api.post('/posts', draft);

    expect(res).toHaveStatus(201);
    const { valid, errors } = validate(postCreateSchema, res.data);
    expect(valid).toBe(true);
    expect(errors).toBeArrayOfSize(0);

    expect(res.data.title).toBe('Release approved');
    expect(res.data.userId).toBe(draft.userId);
    expect(res.data.id).toBe(101); // jsonplaceholder always returns 101 for a new post
  });

  test('PUT replaces, PATCH partially updates', async () => {
    const put = await api.put('/posts/1', buildPost({ title: 'Full replace' }));
    expect(put).toHaveStatus(200);
    expect(put.data.title).toBe('Full replace');

    const patch = await api.patch('/posts/1', { title: 'Hotfix shipped' });
    expect(patch).toHaveStatus(200);
    expect(patch.data.title).toBe('Hotfix shipped');
    expect(patch.data.userId).toBe(1); // untouched field survives the partial update
  });

  test('DELETE returns 200', async () => {
    const res = await api.delete('/posts/1');
    expect(res).toHaveStatus(200);
  });
});
