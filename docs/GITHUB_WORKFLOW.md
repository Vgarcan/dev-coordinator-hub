# GitHub collaboration and communication

**Scope:** public project planning and code review in this repository. Real execution commands belong in a separate future **private** control channel.

## Table of contents

1. [Which GitHub feature to use](#which-github-feature-to-use)
2. [From an idea to an accepted change](#from-an-idea-to-an-accepted-change)
3. [Issue and PR conventions](#issue-and-pr-conventions)
4. [Decision and audit rules](#decision-and-audit-rules)
5. [Public/private boundaries](#publicprivate-boundaries)

## Which GitHub feature to use

| Need | Use | Rule |
| --- | --- | --- |
| Feature, bug, research, technical task | **Issue** | Outcome, scope, acceptance, dependencies, evidence |
| Architectural choice | **Decision Issue** + [decision register](DECISIONS.md) | Separate options, recommendation and owner approval |
| Actual code or documentation modification | **Branch + Pull Request** | Changes reviewed before merge to `main` |
| Review, feedback or correction | **PR review/comments** | Cite affected files, precise change and validation |
| Durable product understanding | **Markdown in `docs/`** | Updated by PR, not left buried in chat |
| Release or demonstration | **Tag/release** after validation | Not required before first MVP |
| Public design showcase | **GitHub Pages** | Fictional data only |
| Runtime job/approval and private audit events | **Private control repository / local store** | Never dispatch from public Issue comments |

GitHub Projects and Discussions may improve navigation as the backlog grows; they are **optional future conveniences**, not prerequisites and not currently assumed to be configured. GitHub Actions may eventually validate documentation/code, but the MVP must not depend on Actions billing or paid runners.

## From an idea to an accepted change

1. **Discuss:** owner and ChatGPT define what problem is being solved.
2. **Capture:** open a public-safe Issue using the right template, identifying objective, boundaries, requirement IDs and acceptance.
3. **Plan:** propose approach, dependencies, role and risk. Record unresolved decisions instead of guessing.
4. **Approve scope:** owner gives explicit approval for the work and any autonomy/spending limits.
5. **Implement:** create a branch and draft PR, with bounded changes, tests and evidence.
6. **Review:** use PR review comments or request changes; independent agent review is not equivalent to owner approval.
7. **Accept:** owner approves meaningful scope/design changes; merge only after requested checks pass.
8. **Record:** update docs/decision register, close or link Issues and preserve review history.

A plan being in an Issue or PR **does not automatically authorise agent execution**. The future private coordination protocol requires separate validated authorisation.

## Issue and PR conventions

- Issue titles start with `[Research]`, `[Task]`, `[Bug]` or `[Decision]` when helpful.
- Every task records an observable result and a definition of done.
- Requirements use stable IDs such as `FR-04` or `NFR-SEC-01`.
- Link related Issues and PRs in both directions; link commits and test evidence.
- PRs are narrowly scoped, reviewable and based on the current `main`.
- Do **not** paste large model conversations into Issues. Summarise decisions and link evidence.
- Use checklists for verifiable work, never as a substitute for actual test results.
- No silent force-push over reviewed commits; verify the head SHA when reviewing or merging.

## Decision and audit rules

Documents distinguish: **verified fact**, **proposal/assumption**, **open question**, **risk**, **approved decision** and **action**. Owner approval must be attributable and scoped; automated systems cannot self-approve.

For real runtime work, capture task ID, version/hash, actor, outcome, timestamp, reviewer and evidence references in the **private** channel, with protected local logs. Generic public Issues/PRs may link public-safe information only.

## Public/private boundaries

This public repository is readable by anyone. Do not publish credentials, private repositories, company-owned project details, session tokens, unredacted logs or task authorisation payloads. Public Issues are **never trusted command queues**. A GitHub App/token should have the minimum permissions needed for each environment.

Review [security rules](SECURITY.md) before proposing integrations.
