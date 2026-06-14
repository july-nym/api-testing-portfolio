/**
 * Test-data builders. Using factory functions (not shared constants) means each
 * test gets its own object and can't accidentally mutate a neighbour's fixture.
 * Names are realistic-but-fictional so a failing assertion reads like a real
 * record, not "test test test".
 */

let postCounter = 0;

function buildBooking(overrides = {}) {
  return {
    firstname: 'Priya',
    lastname: 'Ramanathan',
    totalprice: 1120,
    depositpaid: true,
    bookingdates: {
      checkin: '2026-07-03',
      checkout: '2026-07-10',
    },
    additionalneeds: 'Quiet room',
    ...overrides,
  };
}

function buildPost(overrides = {}) {
  postCounter += 1;
  return {
    title: 'Regression sign-off checklist',
    // the counter makes it easy to eyeball which post a given test created
    body: `Smoke green, schema stable, no P1 regressions (#${postCounter}).`,
    userId: 7,
    ...overrides,
  };
}

module.exports = { buildBooking, buildPost };
