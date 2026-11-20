import test from 'node:test';
import assert from 'node:assert/strict';
import { getEligibility } from '../src/eligibility.js';

const base = { authenticated: true, coverageStart: '2026-01-01', coverageEnd: '2026-12-31' };

test('date inside coverage is active', () => assert.equal(getEligibility({ ...base, serviceDate: '2026-03-15' }), 'Active'));
test('coverage start is inclusive', () => assert.equal(getEligibility({ ...base, serviceDate: '2026-01-01' }), 'Active'));
test('coverage end is inclusive', () => assert.equal(getEligibility({ ...base, serviceDate: '2026-12-31' }), 'Active'));
test('date before coverage is inactive', () => assert.equal(getEligibility({ ...base, serviceDate: '2025-12-31' }), 'Inactive'));
test('date after coverage is inactive', () => assert.equal(getEligibility({ ...base, serviceDate: '2027-01-01' }), 'Inactive'));
test('unauthenticated request is rejected without exposing input', () => {
  assert.throws(
    () => getEligibility({ ...base, authenticated: false, serviceDate: 'synthetic-sensitive-input' }),
    { name: 'Error', message: 'Unauthorized' }
  );
});
