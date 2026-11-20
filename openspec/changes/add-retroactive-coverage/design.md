# Design

The eligibility function receives an authenticated flag, requested date, and synthetic coverage periods. It returns `Active` when the requested date falls within an inclusive coverage period; otherwise it returns `Inactive`.

## Security and privacy
- Reject unauthenticated requests before evaluating coverage.
- Keep test fixtures synthetic.
- Do not log input records.

## Traceability
- `features/member-eligibility.feature` defines observable acceptance behavior.
- `tests/eligibility.test.js` covers boundary behavior.
