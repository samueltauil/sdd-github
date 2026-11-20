# ADR 0001: Separate requirement and behavioral authority

## Status
Proposed

## Decision
Use OpenSpec as the authority for requirements, constraints, design, and change scope. Use Gherkin as the authority for observable acceptance behavior. Use automated tests and pull-request checks as evidence of conformance.

## Consequences
This improves traceability and business readability, but requires disciplined ownership and conflict handling. It does not replace architecture review, threat modeling, privacy review, or human approval.
