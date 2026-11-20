Feature: Member eligibility lookup
  Eligibility is evaluated using synthetic coverage dates and an authenticated caller.

  Scenario: Retroactive coverage includes the service date
    Given an authenticated eligibility request
    And coverage is active from "2026-01-01" through "2026-12-31"
    When eligibility is requested for "2026-03-15"
    Then the eligibility status is "Active"

  Scenario: Coverage does not include the service date
    Given an authenticated eligibility request
    And coverage is active from "2026-04-01" through "2026-12-31"
    When eligibility is requested for "2026-03-15"
    Then the eligibility status is "Inactive"

  Scenario: Unauthenticated request
    Given an unauthenticated eligibility request
    And coverage is active from "2026-01-01" through "2026-12-31"
    When eligibility is requested for "2026-03-15"
    Then the request is rejected
