# Delta: Retroactive coverage

## ADDED requirements

### Requirement: Service-date evaluation
The service MUST evaluate the requested service date against inclusive coverage effective and termination dates.

#### Scenario: Date within coverage period
- GIVEN an authenticated caller and a coverage period
- WHEN the requested date falls within the period
- THEN the status is `Active`

#### Scenario: Date outside coverage period
- GIVEN an authenticated caller and a coverage period
- WHEN the requested date falls outside the period
- THEN the status is `Inactive`
