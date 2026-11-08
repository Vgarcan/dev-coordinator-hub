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
| `model_policy` | Approved provider/model ID or bounded eligible tier; desired/effective effort, allowed fallback and data restrictions |
| `routing_rationale` | ChatGPT's explained recommendation, risk class and NO_AI/SINGLE/HANDOFF/PARALLEL/WAIT choice |
| `limits` | Maximum duration, attempts, context/session budget, concurrency |
| `requested_by`, `approved_by` | Auditable actor identities |
| `spec_hash`, `approval_expires_at` | Approval pinned to a specific task version |
| `status`, `revision` | Optimistic concurrency / lifecycle |
| `auth_provider`, `auth_resume_from` (when relevant) | Allowlisted CLI provider (Codex or Claude) and prior lifecycle checkpoint; never secrets, login URLs or device codes |
| `evidence_refs` | Commits, PR, checks and protected log references |

This is a design contract, **not** an executable YAML or a stable API schema yet.

## States and transitions

```mermaid
stateDiagram-v2
    [*] --> DRAFT
    DRAFT --> READY: validated owner approval
    READY --> PREPARING
    PREPARING --> RUNNING: safe checkout and CLI available
    PREPARING --> AUTH_REQUIRED: CLI session missing or expired
    RUNNING --> AUTH_REQUIRED: auth lost; stop and reconcile partial work
    AUTH_REQUIRED --> PREPARING: human re-login + independent verification
    AUTH_REQUIRED --> BLOCKED: verification or policy fails
    AUTH_REQUIRED --> CANCELLED: owner cancels
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

### Human-in-the-loop authentication pause (proposed)

`AUTH_REQUIRED` is **a hold on the affected task**, not permission to start a new login, execute arbitrary shell commands, retry a partially completed job, or dispatch a different agent. It records only a task ID, an allowlisted provider (`codex` or `claude`), the previous checkpoint and a redacted reason. This public repository has no real task state machine or CLI connections.

- When a CLI reports missing/expired authentication, a **future private coordinator** stops dispatch and records the pause. Never capture terminal transcripts, bearer tokens, passwords, verification codes, or generated login URLs in task records or UI.
- The owner uses their own trusted SSH/terminal session under the **same non-root OS account** that owns the CLI session, and follows the provider's official login instructions. The Django interface cannot collect credentials or initiate terminal commands.
- After manual sign-in, the future coordinator must separately verify the provider CLI session using its supported, read-only status mechanism. It must also revalidate the original immutable approval, scope, account, and time limits. A browser acknowledgement is never evidence of successful authentication.
- If a job had already started, **reconcile its actual process and side effects before any retry**. Resume from a known safe checkpoint only with valid owner-approved authority; otherwise remain blocked or ask for a fresh approval. Authentication alone does not automatically run or merge work.

Do not store CLI-managed sessions in `.env`: the development `.env` can hold application configuration, but provider credential storage belongs to the CLI's secure per-user mechanism. The exact production status-check integration and permissions remain pending the CLI feasibility assessment.

## Approval and trust

- A text comment or label does not grant operating-system execution authority.
- Authorisation must come from an explicitly approved identity through a separately validated protocol.
- Approval binds repo, command scope, agent/model/effort or allowed tier, fallback constraints, limits, expiry and content hash. Material model-tier upgrades require reapproval.
- Any material mutation requires a new approval; repeated delivery with the same ID/revision is idempotent.
- The worker must refuse unexpected repos, dangerous commands, untrusted attachments and missing permits.
- Review and owner acceptance are distinct actions; no agent may grant itself additional permission.

## Agent-to-agent hand-off

Agents exchange compact evidence, not multi-thousand-token transcripts:

1. ChatGPT's proposed assignment is recorded with selected provider/model (if verified), desired effort, budget and whether independent review is warranted; owner approves permitted limits. See [collaboration policy](CHATGPT_AGENT_COLLABORATION.md) and [model selection](MODEL_SELECTION_POLICY.md).
2. Implementation agent returns summary, changed files, SHA/PR, tested outcomes and usage data only when actually available.
3. Coordinator records that output and checks deterministic requirements first.
4. Reviewer receives approved specification, relevant diff and tests, normally read-only.
5. Reviewer reports `APPROVE`, `REQUEST_CHANGES` or `BLOCKED` with actionable findings.
6. Coordinator can permit only a small preapproved number of correction loops before escalating.

No agent continuously polls another agent or expands the approved scope.

## Failure and evidence

Persist timeouts, cancellations, authentication failures, token-limit errors and audit events without copying secrets. Recover after crashes without duplicate execution. Usage percentages must be labelled **unverified** when providers do not expose accurate subscription telemetry. A failed CLI model lookup or unsupported effort setting must block or invoke only an explicitly approved equivalent fallback.

Result is not `DONE` simply because a CLI produced text. It must meet acceptance, have validation evidence and obtain the required human decision.
