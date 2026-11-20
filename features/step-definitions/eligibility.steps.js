import assert from 'node:assert/strict';
import { Given, When, Then } from '@cucumber/cucumber';
import { getEligibility } from '../../src/eligibility.js';

Given('an authenticated eligibility request', function () { this.authenticated = true; });
Given('an unauthenticated eligibility request', function () { this.authenticated = false; });
Given('coverage is active from {string} through {string}', function (start, end) {
  this.coverageStart = start;
  this.coverageEnd = end;
});
When('eligibility is requested for {string}', function (serviceDate) {
  try {
    this.status = getEligibility({
      authenticated: this.authenticated,
      serviceDate,
      coverageStart: this.coverageStart,
      coverageEnd: this.coverageEnd
    });
  } catch (error) {
    this.error = error;
  }
});
Then('the eligibility status is {string}', function (expected) {
  if (this.error) throw this.error;
  assert.equal(this.status, expected);
});
Then('the request is rejected', function () {
  assert.equal(this.error?.message, 'Unauthorized');
});
