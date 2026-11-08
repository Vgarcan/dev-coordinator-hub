# Decision register

**Source:** PDD v0.1 and subsequent planning. Only rows explicitly marked **Agreed** reflect existing owner decisions; proposed choices are **not** implementation authority.

## Table of contents

1. [Decision log](#decision-log)
2. [How to change a decision](#how-to-change-a-decision)

## Decision log

| ID | Decision / option | State | Reason or next validation |
| --- | --- | --- | --- |
| D-001 | Use private GitHub as initial ChatGPT ↔ server bridge; no public API | **Agreed** | Minimise exposed infrastructure; outbound connections |
| D-002 | Headless Linux, official Codex/Claude CLIs; VS Code optional | **Agreed** | Run without desktop dependence |
| D-003 | Repositories are chosen on demand; do not bulk-import all repos | **Agreed** | Simpler UX and narrower permissions |
| D-004 | No agent execution as root | **Agreed** | Basic host isolation and least privilege |
| D-005 | Public `dev-coordinator-hub` hosts code, docs and Pages UI only | **Agreed** | Distinct from operational control |
| D-006 | Python service, small persistent store / SQLite, outbound polling initially | **Proposed** | Validate reliability and operational simplicity |
| D-007 | Private GitHub control repository and identity/approval model | **Pending** | Create and verify rights, task authorisation, replay prevention |
| D-008 | Enterprise-provided Claude Code use on personal server/projects | **Pending** | Organisation and provider terms must explicitly permit it |
| D-009 | Reserve ~20% of account usage (stop near 80%) | **Preference, not guaranteed** | Need reliable provider telemetry; use bounded local limits first |
| D-010 | Private Django audit UI / foro after bridge feasibility | **Proposed** | Avoid building an unnecessary backend before value proof |
| D-011 | Server, sandbox technology, backup and retention | **Pending** | Must be tested in feasibility |
| D-012 | No automatic merges, deployment or destructive operation without owner approval | **Agreed** | Human authority over high-impact changes |
| D-013 | ChatGPT recommends task-specific agent/model/effort and coordination mode, including NO_AI, before owner approval | **Agreed in concept** | Economise token use without sacrificing validation; see #8 |
| D-014 | Dynamic eligible-model catalog, bounded fallback and routing telemetry in Linux | **Proposed** | Verify exact CLI support and subscriptions first; see #8 |

## How to change a decision

Open a **Decision Issue** with context, options, risks, recommendation and explicit owner approval. If accepted, update this table via PR with date and a link to the Issue. This register should never silently upgrade **Proposed** to **Agreed**.

Decisions may be revised when new evidence arises. A change to permissions, operating model, cloud access or scope must also update [security](SECURITY.md) and the [PDD](PDD.md).
