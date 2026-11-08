# Private task and agent hand-off protocol

**Status:** proposed protocol; **not implemented**, and never to be executed through this public repository.

## Table of contents

1. [Purpose](#purpose)
2. [Task record](#task-record)
3. [States and transitions](#states-and-transitions)
4. [Approval and trust](#approval-and-trust)
5. [Agent-to-agent hand-off](#agent-to-agent-hand-off)
6. [Failure and evidence](#failure-and-evidence)

## Purpose

Replace free-form, continuous model conversations with small structured, auditable events. ChatGPT helps the owner prepare a plan; the local coordinator determines when work may start, within the approved policy.

## Task record

The private control plane should eventually represent:

| Field | Purpose |
| --- | --- |
| `task_id`, `schema_version` | Stable ID and versioned parser |
| `repo_id`, `target_ref` | Allowlisted repository and immutable target |
| `intent`, `scope` | Requested outcome and explicit exclusions |
| `acceptance` | Verifiable tests/evidence required |
| `agent_policy` | Allowed CLI agents, role and review requirements |
| `limits` | Maximum duration, attempts, context/session budget, concurrency |
| `requested_by`, `approved_by` | Auditable actor identities |
| `spec_hash`, `approval_expires_at` | Approval pinned to a specific task version |
| `status`, `revision` | Optimistic concurrency / lifecycle |
| `evidence_refs` | Commits, PR, checks and protected log references |

This is a design contract, **not** an executable YAML or a stable API schema yet.

## States and transitions

```mermaid
stateDiagram-v2
    [*] --> DRAFT
    DRAFT --> READY: validated owner approval
    READY --> PREPARING
    PREPARING --> RUNNING: safe checkout and CLI available
    RUNNING --> REVIEW: implementation completed
    REVIEW --> WAITING_APPROVAL: review passed or escalated
    WAITING_APPROVAL --> DONE: owner accepts
    REVIEW --> RUNNING: bounded authorised correction
    DRAFT --> CANCELLED
    READY --> CANCELLED
    PREPARING --> BLOCKED
    RUNNING --> FAILED
    RUNNING --> BLOCKED
    REVIEW --> BLOCKED
    WAITING_APPROVAL --> CANCELLED
```

The transition map is indicative; cancellation, recovery and retry semantics must be tested. Every state change is persisted with the actor and timestamp. `FAILED` and `BLOCKED` are not auto-retry permissions.

## Approval and trust

- A text comment or label does not grant operating-system execution authority.
- Authorisation must come from an explicitly approved identity through a separately validated protocol.
- Approval binds repo, command scope, agent policy, limits, expiry and content hash.
- Any material mutation requires a new approval; repeated delivery with the same ID/revision is idempotent.
- The worker must refuse unexpected repos, dangerous commands, untrusted attachments and missing permits.
- Review and owner acceptance are distinct actions; no agent may grant itself additional permission.

## Agent-to-agent hand-off

Agents exchange compact evidence, not multi-thousand-token transcripts:

1. Implementation agent returns summary, changed files, SHA/PR and test results.
2. Coordinator records that output and checks deterministic requirements first.
3. Reviewer receives approved specification, relevant diff and tests, normally read-only.
4. Reviewer reports `APPROVE`, `REQUEST_CHANGES` or `BLOCKED` with actionable findings.
5. Coordinator can permit only a small preapproved number of correction loops before escalating.

No agent continuously polls another agent or expands the approved scope.

## Failure and evidence

Persist timeouts, cancellations, authentication failures, token-limit errors and audit events without copying secrets. Recover after crashes without duplicate execution. Usage percentages must be labelled **unverified** when providers do not expose accurate subscription telemetry.

Result is not `DONE` simply because a CLI produced text. It must meet acceptance, have validation evidence and obtain the required human decision.
