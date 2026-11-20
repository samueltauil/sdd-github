# Proposal: Add retroactive coverage evaluation

## Why
Coverage may be activated after a service date. Eligibility evaluation must use the effective coverage period rather than only the current status.

## What Changes
- Evaluate a requested service date against coverage start and end dates.
- Preserve authentication and sensitive-data protections.
- Return only `Active` or `Inactive` in this sample.

## Out of scope
- Claims adjudication
- Real payer integrations
- Production member data
- Changes to identity or authorization architecture

## Success criteria
All approved Gherkin scenarios pass, unit tests pass, and the pull request contains no unapproved specification changes.
