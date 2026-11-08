# Project Plan — Dev Coordination Hub

## Contents

1. Product objective
2. MVP boundary
3. Implementation stages
4. Acceptance criteria
5. Open decisions

## Product objective

Make an AI-assisted development workflow auditable and manageable from a phone. The user approves goals and important changes; a local coordinator dispatches bounded work to available CLI agents. GitHub provides versioned code and initially a private coordination channel.

## MVP boundary

- One server; a small number of approved source repositories.
- Codex CLI and Claude Code availability checks (subject to official product terms and organisation policy).
- Task registration, authorisation state, assignments, review status, and audit events.
- Git worktrees or equivalent isolated checkouts for parallel writes.
- No automated merges to protected branches; no administrative execution by agents.
- No public administrative API.
- Explicit maximum task duration, retries and concurrency.

Out of scope for the first version: continuously running model coordinator, a large multi-agent chat/forum, a public live dashboard and unrestricted autonomous discovery of new repositories.

## Implementation stages

| Stage | Deliverable | Evidence |
| --- | --- | --- |
| UI | Public prototype | Responsive browser review and owner approval |
| Feasibility | Headless CLI check | Official authentication, usage-policy and noninteractive execution verified |
| Bridge | Private GitHub task exchange | Least-privilege worker and message handling validated on test tasks |
| Worker | Local execution | Isolated repo checkout, bounded subprocesses, safe cancellation |
| Audit | Private Django viewer | Authenticated event history and decisions traceable to commits/PRs |

## Acceptance criteria

- A user can select an authorised repository and register an approved task.
- A worker completes one bounded CLI operation without a desktop environment.
- Tasks with expired, duplicate or revoked authorisation do not execute.
- Every state change has an attributable, timestamped audit record.
- Reviewer results and evidence are accessible without copying chat transcripts.
- The public UI contains no production data or credentials.

## Open decisions

- Confirm whether enterprise-provided Claude Code access may be used with a personal/server workflow.
- Verify available subscription usage/limit telemetry; the proposed 80% allowance is a policy target, not a guaranteed hard stop.
- Select authoritative storage for audit records and approvals; do not use public issues for sensitive data.
- Select server OS, deployment mechanism, backups and test strategy.
