# Walkthrough: follow one change

This is a guided tour of the example, followed by the steps to try the same
workflow on GitHub. The files in this repository are an illustrative draft:
they are not evidence that an issue, approval, or pull request already exists.

## 1. Start with a problem

A team learns that coverage can be recorded after a service date even though
it was effective on that date. They want the answer to depend on the date of
service, not only on whether coverage is active today.

In a GitHub repository, open an issue using **Propose a change**. Describe the
problem and the desired result. For this synthetic example:

> When a requested service date falls inside the effective coverage period,
> return `Active`; otherwise return `Inactive`. Reject unauthenticated requests.

An issue is the conversation and work item. It does not by itself override an
approved requirement or security policy.

## 2. Compare the current promise with the proposed change

Read these files in order:

1. [Current contract](../openspec/specs/member-eligibility/spec.md): what the
   capability already promises.
2. [Proposal](../openspec/changes/add-retroactive-coverage/proposal.md): why
   the change is needed, its scope, and what is out of scope.
3. [Requirement delta](../openspec/changes/add-retroactive-coverage/specs/member-eligibility/spec.md):
   the proposed addition, rather than a replacement for the entire contract.
4. [Design](../openspec/changes/add-retroactive-coverage/design.md) and
   [tasks](../openspec/changes/add-retroactive-coverage/tasks.md): the intended
   approach and the work to review and perform.

## 3. Agree on examples

Read [the Gherkin scenarios](../features/member-eligibility.feature) with
product, quality, and engineering representatives:

- A service date inside the coverage period returns `Active`.
- A service date outside the coverage period returns `Inactive`.
- An unauthenticated request is rejected.

The words are intended to be understandable without knowing JavaScript.
`Given` sets up the example, `When` describes what happens, and `Then` states
the expected result. The start and end dates are inclusive; the unit tests
cover those boundaries.

People must approve the requirement and examples before implementation. If
the examples and OpenSpec disagree, resolve the disagreement explicitly.
Do not silently edit either one to make a test pass.

## 4. Ask Copilot for a plan

With the issue and files available in your Copilot context, start with a
planning request such as:

```text
Read the linked issue, current OpenSpec contract, proposed change, design,
tasks, and related Gherkin scenarios. Do not edit files yet.

Report conflicts or missing decisions. Map each scenario to the implementation
and automated tests, identify the files you would change, and propose small
implementation steps. Wait for human review before implementing.
```

Review the plan with the people responsible for the change. After approval,
ask Copilot to implement one bounded task at a time without changing the
approved specs or scenarios. If requirements need to change, treat that as a
separate reviewed decision.

The sample implementation is already included for inspection; there is no
claim that Copilot produced it or that a human has approved this draft.

## 5. Connect behavior to code and evidence

This map makes it possible to review the change in either direction: from a
requirement to evidence, or from a code change back to its reason.

| Example scenario | Requirement | Code and evidence |
| --- | --- | --- |
| Retroactive coverage includes the service date | Service-date evaluation | [`getEligibility`](../src/eligibility.js); [Cucumber steps](../features/step-definitions/eligibility.steps.js); inside and endpoint unit tests |
| Coverage does not include the service date | Service-date evaluation | The same function and steps; before- and after-period unit tests |
| Unauthenticated request | Authenticated eligibility lookup | The authentication guard and Cucumber rejection step; unit test for a generic error |

The current contract also requires protection of sensitive data. This sample
does not log input records and its rejection error is generic, but it does not
simulate a complete production logging, identity, or privacy system. Review
and test those controls separately in a real application.

## 6. Run the evidence

From the repository directory:

```sh
npm ci
npm run test:unit
npm run test:bdd
npm run validate:spec
npm audit --audit-level=high
```

The OpenSpec command checks both the current spec and the proposed change.
The audit checks known dependency advisories; it is not a substitute for
application security, privacy, or integration testing.

## 7. Open and review a pull request

In a GitHub repository with a change on a branch, open a pull request. Use the
provided template to link the issue, OpenSpec change, scenarios, code, and
results. Replace the example with the real issue number, for example
`Closes #123`. GitHub interprets closing keywords when the pull request targets
the repository's default branch.

GitHub Actions runs the checks defined in
[`validate.yml`](../.github/workflows/validate.yml). Set up reviewers and
required checks using the [governance guide](governance.md); a workflow file
alone does not protect a branch.

Ask reviewers:

- Is every requirement and scenario implemented and supported by evidence?
- Is any behavior or code outside the agreed scope?
- Did anyone weaken a requirement or scenario to make a check pass?
- Are security, privacy, and remaining risks addressed appropriately?

Copilot can help with that review, but it is not the final approval authority.

## 8. Merge and keep the contract current

After the work is finished, the tasks are complete, and the change is
approved, OpenSpec can apply the delta to the current spec and retain the
change as history:

```sh
npx openspec archive add-retroactive-coverage
npm run validate:spec
```

Run this on the change branch before its final review, or in a reviewed
follow-up pull request after merge, according to your team's policy. Inspect
the updated spec and `openspec/changes/archive/` in the diff. If archiving
changes the PR after review, obtain any renewed approvals your rules require.
Do not use `--yes` to bypass incomplete tasks or human review.

An issue linked with a closing keyword closes automatically when the linked
pull request is merged into the default branch. The current spec then describes
the accepted behavior, while the archived change preserves the history.

## Optional: regenerate the animation

The GIF is checked in, so readers do not need Python. To regenerate it after
editing [`scripts/create_workflow_gif.py`](../scripts/create_workflow_gif.py),
install Pillow 12.0.0 in a Python environment and run:

```sh
python -B -m scripts.create_workflow_gif
```
