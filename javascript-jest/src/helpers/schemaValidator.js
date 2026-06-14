/**
 * Ajv-backed schema validation. A single compiled Ajv instance is reused across
 * specs — compiling per assertion is wasteful and ajv caches by reference.
 * Schemas live alongside the validator since they're small and tightly coupled
 * to the responses they describe.
 */
const Ajv = require('ajv');
const addFormats = require('ajv-formats');

const ajv = new Ajv({ allErrors: true });
addFormats(ajv); // enables "format": "email" etc.

// jsonplaceholder user — only the fields we assert on are required; the nested
// address/company objects carry more, but we don't over-specify the contract.
const singleUserSchema = {
  type: 'object',
  required: ['id', 'name', 'username', 'email', 'address', 'phone', 'company'],
  properties: {
    id: { type: 'integer' },
    name: { type: 'string' },
    username: { type: 'string' },
    email: { type: 'string', format: 'email' },
    phone: { type: 'string' },
    website: { type: 'string' },
    address: {
      type: 'object',
      required: ['street', 'suite', 'city', 'zipcode'],
    },
    company: {
      type: 'object',
      required: ['name'],
    },
  },
};

// jsonplaceholder POST /posts -> 201
const postCreateSchema = {
  type: 'object',
  required: ['id', 'title', 'body', 'userId'],
  properties: {
    id: { type: 'integer' },
    title: { type: 'string' },
    body: { type: 'string' },
    userId: { type: 'integer' },
  },
};

const bookingCreateSchema = {
  type: 'object',
  required: ['bookingid', 'booking'],
  properties: {
    bookingid: { type: 'integer' },
    booking: {
      type: 'object',
      required: ['firstname', 'lastname', 'totalprice', 'depositpaid', 'bookingdates'],
      properties: {
        firstname: { type: 'string' },
        lastname: { type: 'string' },
        totalprice: { type: 'integer' },
        depositpaid: { type: 'boolean' },
        bookingdates: {
          type: 'object',
          required: ['checkin', 'checkout'],
          properties: {
            checkin: { type: 'string' },
            checkout: { type: 'string' },
          },
        },
      },
    },
  },
};

/**
 * Validate `payload` against `schema`. Returns { valid, errors } so the caller
 * can assert and also print a readable diff on failure.
 */
function validate(schema, payload) {
  const check = ajv.compile(schema);
  const valid = check(payload);
  return { valid, errors: check.errors || [] };
}

module.exports = { validate, singleUserSchema, postCreateSchema, bookingCreateSchema };
