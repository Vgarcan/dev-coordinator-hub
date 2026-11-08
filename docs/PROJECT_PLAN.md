# Delivery roadmap — Dev Coordination Hub

**Status:** proposed, incremental. No implementation dates or estimates have been committed.

## Table of contents

1. [Phases and exit gates](#phases-and-exit-gates)
2. [Immediate sequence](#immediate-sequence)
3. [Definition of done](#definition-of-done)
4. [How progress is measured](#how-progress-is-measured)

## Phases and exit gates

| Phase | Deliverable | Required evidence / exit gate |
| --- | --- | --- |
| Foundation (now) | PDD, architecture, requirements, security, Issues/PR workflow and public demo | Owner reviews the scope; no operational capability claimed |
| 0 — Feasibility | Headless CLI proof, eligible model and effort catalog, legal/auth check for Claude, secure GitHub private channel | Tool usage allowed, credentials protected, test writes/replies verified |
| 1 — Read-only proof | Poll private task, validate author/version, inspect allowlisted repo and post a report | Entire mobile → GitHub → Linux → GitHub → mobile loop completed without editing source |
| 2 — Controlled MVP | Worktrees, bounded agent edit, tests, independent review, durable events, cancellation | [PDD acceptance](PDD.md#11-mvp-acceptance) proven |
| 3 — Pilot | Multiple approved repos, recovery, resource limits, measured savings | Compare against manual workflow; no privilege boundary violation |
| 4 — Product evolution | Private Django audit viewer and optional richer communication | Demonstrated need and separately reviewed security design |

The existing static UI is a **demo**, not the read-only proof or a connected web control plane.

## Immediate sequence

1. Review and approve the foundation docs and terminology on a PR.
2. Create Issues for the **Phase 0** feasibility checks and their observable outputs.
3. Choose a Linux test host; establish non-root identities and an isolated test repository.
   - Run `python backend/scripts/preflight.py` on that host to inventory Python, Django and CLI availability **without executing an agent**; record authentication and subscription eligibility as unverified.
4. Verify official CLI use in headless mode, supported selectable model IDs / effort controls and quota visibility; explicitly check company-approved Claude use.
5. Decide and create the private control channel with scoped GitHub access.
6. Run one safe **read-only** task, then review findings before allowing edits.

Do not introduce GitHub Actions as a prerequisite, especially while runner/billing access is unresolved.

## Definition of done

A change is not done until its Issue outcome is met, a PR shows the actual diff and relevant tests, security/traceability concerns are resolved, owner approval is recorded when required, and documentation is updated.

The first meaningful MVP demonstration is a **controlled and auditable task lifecycle**, not autonomous conversation between LLMs.

## How progress is measured

Record selected model and requested/effective effort when available, total elapsed time, manual hand-offs, attempts, review rounds, defects discovered, failure reasons and reliable provider usage numbers when available. Show unknown or unverified utilisation as unknown, not a precise percentage.
