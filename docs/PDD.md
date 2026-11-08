# Project Definition Document — Dev Coordination Hub

**Document ID:** DCH-PDD-001  
**Version:** 0.1 (repository working draft)  
**Date:** 2026-11-08  
**Status:** **Pending owner review and scope approval**  
**Source:** Project Definition Document v0.1 prepared during concept definition; this Markdown version is adapted for traceable GitHub collaboration.

## Table of contents

1. [Executive summary](#1-executive-summary)
2. [Problem, vision and measurable objectives](#2-problem-vision-and-measurable-objectives)
3. [Scope and exclusions](#3-scope-and-exclusions)
4. [Operating model](#4-operating-model)
5. [Logical architecture](#5-logical-architecture)
6. [End-to-end process](#6-end-to-end-process)
7. [Requirements and quality](#7-requirements-and-quality)
8. [Security and usage policy](#8-security-and-usage-policy)
9. [Delivery plan](#9-delivery-plan)
10. [Risks, dependencies and decisions](#10-risks-dependencies-and-decisions)
11. [MVP acceptance](#11-mvp-acceptance)

## 1. Executive summary

Dev Coordination Hub (DCH) is a **project-agnostic**, personal software-development coordination system. A user and ChatGPT discuss an objective from a phone or desktop; after explicit approval, a headless Linux server receives bounded tasks through a **private GitHub coordination channel**, prepares an approved source repository and delegates work to authenticated Codex CLI and/or Claude Code sessions.

The system handles deterministic operations in code rather than spending model tokens: state tracking, task delivery, dependency checks, retries, limits, evidence collection and hand-off to human review. GitHub hosts versioned discussions and code changes; an eventual private Django viewer provides audit-oriented navigation.

The existing **public** `Vgarcan/dev-coordinator-hub` repo hosts this documentation and a static UI demo. **It is not the operational control channel.**

## 2. Problem, vision and measurable objectives

**Current problem:** manual copy/paste of plans and results among ChatGPT, Codex and Claude adds coordination time, duplicated context and weak traceability.

**Vision:** run a small, supervised development team by objectives and verifiable deliverables, without needing VS Code or an always-open model conversation.

| Objective | Evidence of value |
| --- | --- |
| O1 — Remove manual hand-offs | Complete a pilot without manually passing prompts/results among three chat surfaces |
| O2 — Trace every change | Every task links to its repository, approval, actor, execution and verifiable evidence |
| O3 — Reuse selected repositories | Discover or clone an *approved* repo only when needed |
| O4 — Preserve control | No agent runs as root; no unapproved merge, deployment or scope change |
| O5 — Reduce waste | Compare elapsed time, reviews, retries, interventions and reliable usage telemetry against manual work |

No numerical savings target is claimed before a measured baseline exists.

## 3. Scope and exclusions

**MVP in scope:** one headless Linux host; a *separate private* GitHub control channel; approved repository registration and safe checkout; availability checks for CLI agents; structured tasks and approval gates; one bounded execution plus optional independent review; durable state and an audit trail; a human-readable result.

**Not in MVP:** public operational API, mandatory CWP or domain, full forum, public live audit viewer, indefinite autonomous work, production deployment, root agent access, mandatory integration with AI Hub, or a guaranteed 80% quota stop.

The public visual prototype is an **already-created design exploration**, not evidence that any operational capability exists.

## 4. Operating model

| Actor | Responsibility and constraint |
| --- | --- |
| Owner | Selects repo and goals, approves scope and sensitive actions, accepts outcomes |
| ChatGPT | Assists planning, recommends suitable agent/model/effort and coordination mode, review and status queries; not a 24/7 process |
| Local coordinator | Validates identity, approval, task version, dependencies and runtime policy; dispatches and logs |
| Codex CLI / Claude Code | Execute scoped work in isolated environments and return evidence, not final product authority |
| GitHub | Versioned source, Issues, PRs and private task hand-offs where authorised |

Codex/Claude roles are **per task**, not permanently fixed; a reviewer should not modify the implementation by default.

## 5. Logical architecture

- **Public layer:** this repo, issue backlog, documentation, code and static UI demo.
- **Private coordination layer:** dedicated private GitHub repository or an equivalent authorised private channel, with task commands and outcomes.
- **Runtime layer:** Linux coordinator, local durable store, Git workspace manager and isolated CLI runners.
- **Review layer:** commits, tests, PRs, audited states and owner decision. A private Django interface is an **optional later phase**.

The server uses outbound GitHub access first; it does not require inbound Internet access. See [architecture](ARCHITECTURE.md).

## 6. End-to-end process

1. **Define:** owner and ChatGPT agree objective, repo, acceptance, allowed agents and limits.
2. **Register:** create versioned structured draft with a unique task ID.
3. **Recommend:** ChatGPT proposes whether an AI model is needed, available agent/model family and desired reasoning effort, execution mode, independent review and bounded budget. Its recommendation is subject to current CLI/account verification.
4. **Authorise:** authorised human approves the *specific immutable task version*, including allowed model/effort tier and limits; issue comments alone are not approval.
5. **Prepare:** coordinator validates permissions, available models and supported effort controls, budget and clean/isolated checkout.
6. **Execute:** agent works within an explicit sandbox, timeout and attempt budget.
7. **Review:** deterministic checks run first; a second agent reviews when authorised and justified.
8. **Publish:** concise status, selected model/effort when known, tests, commit/PR and redacted evidence reach the private coordination channel.
9. **Decide:** owner accepts, requests a scoped revision or cancels.

Suggested states: `DRAFT → READY → PREPARING → RUNNING → REVIEW → WAITING_APPROVAL → DONE`. `BLOCKED`, `FAILED` and `CANCELLED` are explicit alternatives. All transitions are recorded and idempotent.

## 7. Requirements and quality

The traceable [requirements register](REQUIREMENTS.md) defines FR-01 to FR-13 and NFR constraints. [ChatGPT–agent collaboration](CHATGPT_AGENT_COLLABORATION.md) and [model selection](MODEL_SELECTION_POLICY.md) describe the recommended assignment, model/effort, review and budget policy; exact provider capability and compliance are pending feasibility verification. Every implementation Issue should reference one or more IDs; tests and PR evidence should be mapped back to them.

Important: GitHub’s own comments, repository files and model outputs are **untrusted input** until the coordinator validates them.

## 8. Security and usage policy

- Separate Linux administrator, coordinator service identity and limited worker identities.
- Never run model agents as root or grant unrestricted access to other projects.
- Keep secrets out of code, chat, prompts, issues, logs and static Pages.
- Require explicit approval for destructive operations, production changes, merges, new access or expanded scope.
- Prefer per-job workspace isolation, restricted I/O and deterministic checks.
- ChatGPT recommends the smallest viable agent/model and reasoning effort, explicitly including **no AI** for deterministic operations. The owner approves the permitted model tier and budget, and the coordinator verifies CLI support and enforces these constraints without asking a model to self-authorise.
- Confirm provider terms and the organisation's permission for Claude Code before using its enterprise-provided access in this environment.

The desired **80% usage ceiling / 20% manual reserve** is only approximate until reliable official quota telemetry is available; instead enforce conservative budgets for time, attempts, concurrency and sessions.

## 9. Delivery plan

| Phase | Outcome | Exit gate |
| --- | --- | --- |
| 0 — Feasibility | Permitted headless CLI auth, server permissions, private GitHub read/write test | Allowed, reproducible test with no credential leakage |
| 1 — Read-only PoC | Approved task received; repo inspected; report returned | ChatGPT → private GitHub → Linux → private GitHub → ChatGPT |
| 2 — Safe MVP | Isolated checkout, bounded edit, review, evidence, approvals | All MVP criteria below pass |
| 3 — Pilot | Second repo, recovery, measured savings, limits | Verified reliability and value |
| 4 — UX evolution | Private Django audit/forum and optional direct API | Explicitly justified by usage |

The public UI demo is an earlier visual artefact and does **not** replace these delivery gates. No dates or effort estimates have been approved.

## 10. Risks, dependencies and decisions

See [risks](RISKS.md) and [decisions](DECISIONS.md). Top open dependencies: server choice; creation and access control of the private coordination channel; permitted enterprise Claude use; authentication lifecycle; actual provider quota telemetry.

## 11. MVP acceptance

A demonstration in an authorised test repository must show:

1. An owner-approved task created and delivered via private GitHub.
2. Valid author and approved task version checked; duplicate deliveries do not execute twice.
3. A repository cloned or selected under a non-root identity, with an isolated workspace.
4. At least one bounded CLI agent execution plus optional independent second-agent review.
5. Reliable timeout, cancellation, failure and resume handling, including durable audit state.
6. Verifiable result evidence (tests, diff, SHA/PR or justified failure), with protected data redacted.
7. No merge to `main`, production deployment, secret disclosure or destructive action without explicit approval.
8. Owner can retrieve and understand the result without copying agent transcripts manually.

**Approval required:** adoption of this PDD as the project baseline is a separate human decision, not implied by publication or automated tests.
