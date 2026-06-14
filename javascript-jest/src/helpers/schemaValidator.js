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

const singleUserSchema = {
  type: 'object',
  required: ['data', 'support'],
  properties: {
    data: {
      type: 'object',
      required: ['id', 'email', 'first_name', 'last_name', 'avatar'],
      properties: {
        id: { type: 'integer' },
        email: { type: 'string', format: 'email' },
        first_name: { type: 'string' },
        last_name: { type: 'string' },
        avatar: { type: 'string' },
      },
    },
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

module.exports = { validate, singleUserSchema, bookingCreateSchema };
