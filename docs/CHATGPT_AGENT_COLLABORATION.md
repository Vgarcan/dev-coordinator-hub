# ChatGPT–agent collaboration policy

**Status:** design baseline proposed for owner review in #8 and draft PR #7. **No operational bridge or agent execution is implemented.**

## Table of contents

1. [Roles and authority](#1-roles-and-authority)
2. [Conversation-to-task workflow](#2-conversation-to-task-workflow)
3. [Assignment and coordination modes](#3-assignment-and-coordination-modes)
4. [What ChatGPT should present](#4-what-chatgpt-should-present)
5. [When to pause or escalate](#5-when-to-pause-or-escalate)
6. [Communication and evidence](#6-communication-and-evidence)
7. [Boundaries and examples](#7-boundaries-and-examples)

## 1. Roles and authority

| Actor | Responsibility | Not permitted |
| --- | --- | --- |
| **Owner** | Defines objective, selects/approves repo, accepts scope and budgets, reviews result | — |
| **ChatGPT** | Clarifies intent, proposes plan, agent/model/effort, coordination strategy and limits; explains outcomes | Pretending to be a permanent daemon, inferring approval from public comments |
| **Private GitHub bridge (future)** | Carries **authenticated, versioned, approved** messages and redacted status | Treating this public repository or Pages as an executable command queue |
| **Local coordinator (future)** | Validates actor, approval, scope, model availability, permissions, resource limits and task state; schedules jobs | Acting on unapproved model-proposed changes or expanding permissions |
| **Codex/Claude CLI workers (future)** | Implement or independently review within a sandbox; return actionable evidence | Granting their own permissions, accessing coordinator credentials, auto-merging/deploying |

**Important:** ChatGPT only reasons and proposes while invoked in conversation (or a separately authorised integration). It does not continuously supervise a Linux worker by itself. The Linux coordinator is the autonomous, **deterministic** scheduler.

## 2. Conversation-to-task workflow

1. **Understand** — Owner and ChatGPT agree goal, authorised repository, expected outcome, acceptance, dependencies, risk and exclusions.
2. **Classify** — ChatGPT identifies complexity and whether a deterministic script/test can do the job **without a model**.
3. **Recommend** — ChatGPT proposes agent(s), model family or validated model ID, abstract reasoning depth, mode (PARALLEL/HANDOFF/WAIT), budget and why. See [model selection policy](MODEL_SELECTION_POLICY.md).
4. **Approve** — Owner approves an immutable specification: selected repo/ref, objective, allowed models/agents or constrained tier, reviewer policy, risk scope, limits, expiry and conditions requiring reapproval.
5. **Dispatch** — The *future* private channel transmits the task. The coordinator independently checks who approved it, version/hash, expiry, policy, account status and precise CLI support before executing.
6. **Execute** — Prepare a clean isolated workspace; run permitted non-root processes with timeouts, retries and cancellation; gather deterministic check results.
7. **Review** — Use static checks first; send a compact, read-only diff-based brief to an independent reviewer only when requested/justified.
8. **Report** — Private task/status channel records concise outcomes, validation, SHA/PR and blockers, not full model transcripts by default.
9. **Decide** — Owner accepts, requests a constrained revision, pauses or cancels. A new scope/effort/privilege tier needs new authorisation.

**No GitHub comment, public Issue, model reply or PR merge is an execution approval.**

## 3. Assignment and coordination modes

| Mode | Use when | Risk/cost controls |
| --- | --- | --- |
| **NO_AI** | Mechanical validation, formatting/checks, Git bookkeeping, known deterministic operations | No model calls |
| **SINGLE** | Small bounded edit with objective checks, low risk | One agent, minimal appropriate model/effort |
| **HANDOFF** | Implementation and independent review benefit from different agents | Implementer writes; reviewer read-only by default; bounded correction loops |
| **PARALLEL** | Separate tasks can be done independently | Separate worktrees; no overlapping write ownership; explicit merge coordination |
| **WAIT** | Dependency, missing access, pending approval, unavailable CLI or insufficient budget | No pointless polling with models; pause and surface the blocker |

The proposed default for meaningful code changes is **one implementer plus independent review when risk justifies it**, not two permanently active model sessions. A plan may propose two agents; cost/quality analysis can recommend one or none.

## 4. What ChatGPT should present

A concise **work proposal** in ordinary language, with a structured record available to the coordinator:

| Field | Example for a hypothetical Django bug |
| --- | --- |
| Repository | Approved target, selected only for this job |
| Objective & acceptance | Repair a specific form validation error; prove with regression test |
| Risk / difficulty | Medium; small backend change |
| Implementation | Codex CLI, an available suitable model/profile, desired effort: Medium |
| Review | Claude Code, Sonnet-family model if available/allowed, desired effort: Medium, read-only; *skip if deterministic verification sufficiently covers risk* |
| Mode | HANDOFF |
| Budget | Time, attempts, correction loops and concurrency proposed; exact values approved by owner |
| Approval scope | Immutable spec hash, allowed model ceiling, expiry, disallowed operations |
| Escalation triggers | Credentials/limit failure, unexpected repo change, tests still failing, model tier/cost change |
| Evidence | Tests, diff, commit/PR, concise report and remaining unknowns |

ChatGPT must **label unverified** provider/model availability and subscription balance. A suggested model is not a proof of entitlement or an installed CLI feature.

The owner may approve a bounded **selection policy** (e.g. any verified Medium-tier model from an allowed provider), rather than a single hard-coded identifier; the coordinator may then pick an equivalent within the approved limits. Higher spending, new provider, different data exposure or reduced review requirements require new approval.

## 5. When to pause or escalate

Escalate to the owner instead of guessing or silently using a more expensive model when:

- No allowed model/CLI or legitimate credential is available.
- Model, reasoning level, token/time budget, repo or data classification exceeds the approved ceiling.
- Change impacts security, billing, production, permissions, secrets, schema migrations or destructive Git operations outside scope.
- The agent proposes unexpected dependencies, additional repositories or broader permissions.
- Review finds a critical defect, tests are inconclusive, or correction attempts are exhausted.
- Official usage telemetry is missing and resource limits cannot be safely honoured.

The coordinator should apply **policy checks in code**, not ask an LLM to decide if its own action is authorised.

## 6. Communication and evidence

Use compact, structured hand-offs: goal, allowed files/scope, acceptance, relevant diff, test failures, proposed next action. Avoid copying entire conversations into every prompt. Store run IDs, selected model and version if known, desired/actual effort settings if supported, elapsed time, attempts, outputs and policy decisions in the **private** audit channel; redact logs and secrets.

If a CLI hides the actual model, usage or quota, record **unknown**, not invented values. Audit evidence must not be hosted on the public GitHub Pages demo.

## 7. Boundaries and examples

- **Documentation typo:** deterministic spellcheck or SINGLE low-cost agent; no second reviewer by default.
- **Routine Django feature:** suitable mid-tier implementation; deterministic tests, optional second-agent diff review based on risk.
- **Concurrency, security or database integrity:** deeper analysis and typically independent review with explicit owner decision before privileged steps.
- **Agent temporarily unavailable:** WAIT, report reason; only switch to another authorised agent/model inside approved limits.

This document explains **how ChatGPT should collaborate**. Model capability and budget criteria are detailed in [Model Selection Policy](MODEL_SELECTION_POLICY.md), and security enforcement is defined in [Security](SECURITY.md).
