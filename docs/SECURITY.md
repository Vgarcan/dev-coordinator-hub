# Security boundaries and operating rules

**Public repository; proposed future coordinator.** This file describes mandatory design constraints, not evidence that a secure system has been deployed.

## Table of contents

1. [Exposure and data classification](#exposure-and-data-classification)
2. [Authentication and authorisation](#authentication-and-authorisation)
3. [Host and agent isolation](#host-and-agent-isolation)
4. [GitHub and prompt injection](#github-and-prompt-injection)
5. [Audit, recovery and incidents](#audit-recovery-and-incidents)
6. [Preimplementation security gates](#preimplementation-security-gates)

## Exposure and data classification

| Surface | Allowed | Never allowed |
| --- | --- | --- |
| **Public** repo, Pages and Issues | Generic product/architecture, fictional demo tasks, scrubbed examples | Real command payloads, API keys, private code/logs, identifiable company data |
| **Private** control GitHub (future) | Authenticated task metadata, approved instructions, redacted summaries and evidence links | Raw host secrets, unnecessary sensitive data, secret-bearing terminal transcripts |
| **Local** Linux store (future) | Durable task state, protected audit logs and scoped credentials | Secrets accessible to all model workers or served via a public web endpoint |

GitHub Pages is static and public; a client-side 'password' or hidden button is **not** sufficient protection. A public Issue/PR may describe generic proposed work but must never act as the command queue.

## Authentication and authorisation

- Use narrowly scoped GitHub App or equivalent token, rotated and revocable; distinguish read-only repository access from control/status writes.
- Use strong, explicit allowlists for owners, worker identities, target repos and operations.
- A private GitHub comment alone is **not** an authorisation decision. Authorise the exact immutable task version (hash, repo, scope, limits, expiry) through validated identity checks.
- Reject replayed, altered, expired and unauthorised tasks; record why a command was blocked.
- No automatic release of new capabilities or unrestricted agent-tool permissions after model suggestion.

## Host and agent isolation

- Admin may use root/sudo for setup; the coordinator and agent execution accounts must not.
- Separate coordinator credentials from model execution environments. Agents must not be able to read the coordinator's GitHub control token.
- Clone only approved repository origins, verify expected refs, and never execute unchecked installation hooks on import.
- Use separate worktrees/sandboxes, bounded CPU/memory/time, limited disk access and restricted network egress appropriate to the task.
- No automatic destructive commands, pushing to protected branches, merge to main, production deploy or privileged package install.

## GitHub and prompt injection

Task text, Issues, PR comments, repository source and model responses are untrusted inputs. The model's instruction to 'approve' or 'ignore rules' is never an authority to change system policy. Approvals are validated in code against explicit policy, not inferred from prose.

Treat output artifacts as potentially sensitive. Do not paste full transcripts into public Issues. Redact credentials, private paths, account names and identifying data before publication. Review third-party dependencies and repository scripts before running them.

## Audit, recovery and incidents

Persist task ID, version, actor, permission checks, immutable approval reference, attempted transition, timestamps, job result and evidence location. Support suspension, cancellation and credential revocation. Protect audit records from casual model editing; define retention and backups before handling actual sensitive work.

The usage reserve target (e.g. 80%) is an **operational preference**. If no official reliable signal exists, never claim a quota has been measured or enforce a false threshold; use local execution budgets instead.

## Preimplementation security gates

1. Verify allowed use of enterprise Claude credentials and the data category of target repos.
2. Verify least-privilege private GitHub channel, rotation and incident recovery.
3. Demonstrate non-root execution, sandbox limitations and absence of token leakage.
4. Demonstrate duplicate/altered task rejection and clean restart behaviour.
5. Obtain explicit owner approval before moving from read-only proof to code-writing execution.
