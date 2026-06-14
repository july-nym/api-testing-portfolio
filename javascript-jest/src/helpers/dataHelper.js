/**
 * Test-data builders. Using factory functions (not shared constants) means each
 * test gets its own object and can't accidentally mutate a neighbour's fixture.
 * Names are realistic-but-fictional so a failing assertion reads like a real
 * record, not "test test test".
 */

let bookingCounter = 0;

function buildBooking(overrides = {}) {
  bookingCounter += 1;
  return {
    firstname: 'Priya',
    lastname: 'Ramanathan',
    totalprice: 1120,
    depositpaid: true,
    bookingdates: {
      checkin: '2026-07-03',
      checkout: '2026-07-10',
    },
    // makes it easy to eyeball which booking a given test created
    additionalneeds: `Quiet room (#${bookingCounter})`,
    ...overrides,
  };
}

function buildReqresUser(overrides = {}) {
  return {
    name: 'Lars Petersen',
    job: 'Senior QA Engineer',
    ...overrides,
  };
}

module.exports = { buildBooking, buildReqresUser };
