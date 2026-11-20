# From an issue to a trusted change

This repository is a small, runnable example of **specification-driven
development**: agree on what software should do before asking a person or an
AI assistant to change it. The same examples used to explain the behavior can
then be run as tests.

![Animated workflow: an issue leads to an OpenSpec change and Gherkin examples, people approve them, Copilot helps implement, and a pull request runs checks and receives human review before the change is merged, archived, and reflected in the living specification.](docs/assets/sdd-workflow.gif)

In short: **describe the problem → agree on the behavior → build → check →
review → merge and update the contract**.

## What do these words mean?

| Term | Plain-language meaning |
| --- | --- |
| **GitHub issue** | A place to describe a problem, desired outcome, and discussion. |
| **Specification** (or **spec**) | A written promise about what the software must do. |
| **OpenSpec** | A tool and file structure for keeping the current spec separate from a proposed change. |
| **Gherkin** | A way to describe examples with `Given`, `When`, and `Then`. |
| **Cucumber** | A test runner that connects those examples to code and executes them. |
| **GitHub Copilot** | An AI assistant that can help plan, implement, and review against the agreed files. |
| **Pull request** (PR) | A proposed set of changes that people can review before it is merged. |
| **GitHub Actions** | Automated jobs that run checks when a PR is opened or updated. |
| **CODEOWNERS / ruleset** | GitHub mechanisms for identifying reviewers and requiring checks or approvals. |
| **Living specification** | The current, maintained description of what the system promises. |

These are complementary: an issue explains **why**, OpenSpec defines **what
must change**, Gherkin illustrates **observable behavior**, and code and tests
show **how it was implemented and checked**. If they disagree, stop and resolve
the disagreement rather than changing a test to make the code pass.

## The example

Imagine a coverage record that becomes effective on an earlier date. The sample
checks the requested service date against a synthetic coverage period:

- A date inside the period, including either endpoint, returns `Active`.
- A date outside the period returns `Inactive`.
- An unauthenticated request is rejected.

For example, the [feature file](features/member-eligibility.feature) says:

```gherkin
Given an authenticated eligibility request
And coverage is active from "2026-01-01" through "2026-12-31"
When eligibility is requested for "2026-03-15"
Then the eligibility status is "Active"
```

The code is intentionally small: it models date evaluation using synthetic
inputs. It does not record when coverage was entered, connect to a real
eligibility system, or implement actual identity verification. The
`authenticated` flag is a teaching stand-in, not a production security control.

## Try it locally

Install Node.js **22.12 or later within the 22.x line**, Node.js 24, or Node.js
26 or later. Then, from the repository directory:

```sh
npm ci
npm test
npm run validate:spec
```

`npm test` runs both the JavaScript unit tests and the three Gherkin scenarios.
`npm run validate:spec` runs the pinned OpenSpec CLI against **both** the
current spec and proposed change.

To run just one layer:

```sh
npm run test:unit
npm run test:bdd
npm audit --audit-level=high
```

## Follow the whole story

The [step-by-step walkthrough](docs/walkthrough.md) shows how the example moves
from an issue to reviewed requirements, a Copilot plan, tests, a pull request,
and an updated living spec. It includes prompts and a scenario-to-code map.

The example's files are already present so you can explore and run them without
a GitHub account or Copilot subscription. The example issue, PR, and human
approvals are **not** pre-created or pre-approved. Repository owners can
configure reviewers and branch rules as described in the governance guide.

## Where to look

| Location | What you will find |
| --- | --- |
| [`openspec/specs/`](openspec/specs/member-eligibility/spec.md) | The existing system contract. |
| [`openspec/changes/`](openspec/changes/add-retroactive-coverage/) | The proposed change, design, tasks, and requirement delta. |
| [`features/`](features/member-eligibility.feature) | Business-readable examples that Cucumber can run. |
| [`src/`](src/eligibility.js) and [`tests/`](tests/eligibility.test.js) | The sample implementation and focused technical tests. |
| [`.github/copilot-instructions.md`](.github/copilot-instructions.md) | Instructions to plan against the contracts and stop on conflicts. |
| [`.github/workflows/`](.github/workflows/validate.yml) | OpenSpec, test, and dependency-audit jobs. |
| [`docs/governance.md`](docs/governance.md) | How to configure real reviewers and required checks on GitHub. |
| [`docs/adr/`](docs/adr/0001-openspec-gherkin-authority.md) | The proposed decision about which artifact has which authority. |

Use synthetic examples only. Do not put protected health information,
credentials, production identifiers, or customer data in issues, prompts,
specifications, examples, tests, or logs. The local `context/` directory is
ignored by Git so that source material is not accidentally included in the
repository.

## Official references

- [OpenSpec CLI reference](https://github.com/Fission-AI/OpenSpec/blob/main/docs/cli.md)
- [Gherkin reference](https://cucumber.io/docs/gherkin/reference/)
- [GitHub Copilot custom instructions](https://docs.github.com/en/copilot/concepts/prompting-and-context/custom-instructions)
- [Linking a pull request to an issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue)
- [About code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
- [Available rules for rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)
