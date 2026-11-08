# Documentation map

## Table of contents

1. [Recommended reading](#recommended-reading)
2. [Where decisions and work live](#where-decisions-and-work-live)
3. [Document lifecycle](#document-lifecycle)

## Recommended reading

| Document | Purpose | Status |
| --- | --- | --- |
| [PDD](PDD.md) | Why the product exists, MVP scope, objectives and acceptance | Draft v0.1 for approval |
| [Architecture](ARCHITECTURE.md) | Logical boundaries, components, trust and deployment | Proposed design |
| [Requirements](REQUIREMENTS.md) | Testable FR/NFR identifiers and traceability | Initial baseline |
| [Task protocol](TASK_PROTOCOL.md) | Data, states, approval and review hand-offs | Proposed design |
| [Security](SECURITY.md) | Public/private data, access, execution policy | Mandatory constraints |
| [Project plan](PROJECT_PLAN.md) | Delivery phases and exit criteria | Proposed plan |
| [GitHub workflow](GITHUB_WORKFLOW.md) | How to communicate, review and preserve evidence | Working agreement |
| [Decisions](DECISIONS.md) | Approved, proposed and unresolved architecture decisions | Living register |
| [Risks](RISKS.md) | Risks, assumptions, dependencies and mitigations | Living register |

## Where decisions and work live

- **Public repository:** product code, public-safe documentation, architectural decisions, generic backlog, PR reviews.
- **Future private control repository:** real dispatch messages, authorised job requests, scoped execution results and identifiers that must not be disclosed.
- **Future local coordinator:** runtime state, protected audit events, credentials and isolated agent workspaces.
- **GitHub Pages:** visual demonstration only, never an authenticated operational control plane.

See [GitHub workflow](GITHUB_WORKFLOW.md) for message ownership and approval rules.

## Document lifecycle

1. Propose a change in an Issue or a PR, with reason and affected requirements.
2. Edit on a branch; link the corresponding Issue/decision where applicable.
3. Review correctness, security impact and traceability.
4. Obtain the owner's approval where scope, risk, spending or autonomy changes.
5. Merge approved changes to `main`; update [decision register](DECISIONS.md) and related work items.

The Markdown PDD is a repository working copy **derived from the earlier PDD v0.1 draft**. It does not silently claim that the original draft was approved or that design proposals are already implemented.
