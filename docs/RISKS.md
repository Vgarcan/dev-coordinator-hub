# Risk, assumption and dependency register

**State:** baseline risk assessment; no risk is considered closed without evidence.

## Table of contents

1. [Risks](#risks)
2. [Assumptions](#assumptions)
3. [Dependencies and open questions](#dependencies-and-open-questions)

## Risks

| ID | Risk | Impact | Planned mitigation | State |
| --- | --- | --- | --- | --- |
| R-01 | Enterprise Claude licence/terms do not permit proposed use | High | Verify with organisation and provider; disable adapter if not allowed | Open |
| R-02 | Leakage of secrets or private code into public GitHub/Pages | High | Public/private segregation, scoped credentials, secret-safe logging and review | Open |
| R-03 | Prompt injection through repos, Issues or model output | High | Treat external text as data; validate identity/approved spec; sandbox | Open |
| R-04 | Unbounded review loops or unexpected subscription exhaustion | Medium–high | Hard local time/attempt/concurrency limits; escalate; no invented 80% meter | Open |
| R-05 | GitHub outage, API rate limits or duplicate delivery | Medium | Conditional requests/backoff, durable state, idempotence and recovery tests | Open |
| R-06 | Destructive Git actions or simultaneous edits | High | Worktree-per-job, dirty-check, limited permissions, PR approvals | Open |
| R-07 | Overbuilding dashboard/forum before proving workflow | Medium | Phase gates, one-task PoC and measured value | Open |
| R-08 | Worker compromise affects other repos or host | High | Non-root identities, sandbox, restricted network/secrets, allowlists | Open |
| R-09 | Public demonstration mistaken for live secure controller | High | Clearly labelled mock data, no privileged frontend API keys | Open |

## Assumptions

- A permitted headless Linux host will be available; distro and hardware are not yet selected.
- GitHub identities can access a **separate private** repository with least-privilege permissions.
- Source repositories will be added deliberately and may have different confidentiality constraints.
- Official Claude/Codex subscription use and exact quotas are **not** assumed to work for unattended orchestration.

## Dependencies and open questions

- Which Linux server, service account, sandbox and backup design?
- What enterprise permission is required for Claude and for which repository data?
- How will authorised identities and immutable approval payloads be validated?
- What official signals reveal rate limits and capacity, if any?
- What information must remain only local rather than in private GitHub?
- Can GitHub Actions run in the account, and do we need them? **Not an MVP dependency.**

Track each answered question through a Decision Issue and PR; avoid replacing uncertainty with assumptions.
