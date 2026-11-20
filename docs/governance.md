# Configure the GitHub controls

The files in this repository provide examples; a CODEOWNERS file and workflow
alone do not enforce approvals. Repository settings, access, and human
approvals must be managed in your own GitHub organization or account.

## 1. Choose real owners

[`.github/CODEOWNERS`](../.github/CODEOWNERS) assigns the original repository
owner as the default owner and includes commented team examples. For a fork or
team repository, replace or supplement that owner with appropriate real users
or teams. Protect the CODEOWNERS file itself as well as the specs, scenarios,
and workflow files.

Code owners must have write access. A team used as an owner must also be
visible and have write access to the repository. GitHub uses the CODEOWNERS
file from the pull request's base branch, so merge the configured file there.
The last matching pattern takes precedence; the more specific step-definition
example appears after the general `features/` pattern.

Requiring code-owner review does **not** require every owner listed on a line
to approve: an approval from any listed owner satisfies that requirement. If
each of several roles must approve, use appropriate additional review rules
and human process rather than assuming the list enforces all of them.
A pull request author cannot approve their own pull request, so a repository
with only one owner needs another eligible reviewer to satisfy this rule.

## 2. Protect the default branch

In your repository settings, create a branch ruleset for the default branch
(or configure equivalent branch protection). Depending on your GitHub plan
and permissions, select controls such as:

1. Require a pull request and approving reviews.
2. Require review from code owners and resolve review conversations.
3. Require the **OpenSpec validation** and **Tests and dependency audit**
   status checks. Run the workflow first so the checks are available to select.
4. Dismiss stale approvals when a new commit changes what was reviewed.
5. Restrict bypass permissions according to your organization's policy.

For stronger role-specific approval, GitHub rulesets can require particular
teams for matching paths where that feature is available. Verify the behavior
and availability for your account; a user-owned repository has no teams.

## 3. Add security checks appropriate to the repository

The included workflow runs `npm audit` against the installed dependency
graph. It does not configure CodeQL, GitHub dependency review, secret scanning,
push protection, threat modeling, or privacy review. Enable and require the
appropriate additional controls for your repository and GitHub plan.

An AI instruction, a passing example, and a CODEOWNERS file are not proof of
security or regulatory compliance. Human review and application-specific
testing remain necessary.

## 4. Use a simple readiness and completion check

Before implementation, confirm that the issue describes an outcome; the
affected contract and proposed scope are clear; scenarios and constraints
have been reviewed; and material questions are resolved.

Before merging, confirm that the approved behavior is traceable to code and
tests; the applicable checks and reviews pass; deviations are resolved; and
the plan to update the living spec and retain the change history is clear.

## Official documentation

- [Code owners and access requirements](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
- [Ruleset options and review requirements](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)
- [Configuring dependency review](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/manage-your-dependency-security/configure-dependency-review-action)
