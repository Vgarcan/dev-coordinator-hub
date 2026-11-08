# Model selection and usage-budget policy

**Status:** proposed policy for #8 and documentation PR #7. This is a **decision framework**, not a live inventory of subscription models, prices or CLI flags.

## Table of contents

1. [Objective](#1-objective)
2. [Dynamic model inventory](#2-dynamic-model-inventory)
3. [Recommendation ladder](#3-recommendation-ladder)
4. [Selection algorithm](#4-selection-algorithm)
5. [Effort, spending and quota guardrails](#5-effort-spending-and-quota-guardrails)
6. [Review, fallback and escalation](#6-review-fallback-and-escalation)
7. [Quality and audit metrics](#7-quality-and-audit-metrics)
8. [Examples](#8-examples)

## 1. Objective

Choose the **least resource-intensive verified model + reasoning configuration that can reliably satisfy the approved acceptance and risk level**. Spending less is a goal, but producing low-quality work or compromising security to save tokens is not acceptable.

This policy is intended for **Codex CLI** and **Claude Code CLI** in the future Dev Coordination Hub, not for AI Hub's general ModelConfig architecture.

## 2. Dynamic model inventory

The coordinator must discover/configure for each CLI adapter:

- Provider/CLI identity and current supported **model IDs** (not guesses from previous chats).
- Available model family/profile, supported reasoning/effort controls and exact implementation syntax.
- Authentication/licence/organisation permission, data classification and availability.
- Known output/context limits and usable telemetry (when officially exposed).
- Whether usage accounting reflects an **API-billed request**, a **subscription rate limit**, or **unknown**. Never conflate them.

**Historical planning labels** such as Codex `Luna`, `Terra` and `Sol` are *internal profile names*, not verified official Codex model IDs. Prior examples involving GPT-5.6, GPT-6.x and Claude Haiku/Sonnet/Opus describe a preferred **capability ladder** only. Actual choice must be validated against the current CLI/account; model versions, eligibility and effort controls may differ. No CLI flag is assumed to exist until tested.

## 3. Recommendation ladder

| Work class | Preferred capability / examples | Desired depth | Reviewer decision |
| --- | --- | --- | --- |
| **Deterministic**: known checks, format, Git metadata | **NO_AI**; ordinary code/tools | None | No LLM |
| **Low**: small text/isolated change | Lowest suitable **available** Codex profile or Claude Haiku-family | Low (where supported) | Usually none; deterministic checks |
| **Medium**: bounded feature, Django bug, tests | Mid capability Codex profile or Claude Sonnet-family | Medium (where supported) | Selectively; only if it improves confidence |
| **High**: difficult implementation, tricky RAG/concurrency | Strong Codex profile or Claude Sonnet/Opus-family as appropriate | High (where supported) | Independent review usually justified |
| **Critical**: security, data integrity, important architecture | Strongest **allowed and demonstrated-fit** available model | High; Extra High only if supported/justified | Independent review + explicit owner gate |

Model **family is guidance**, not a ranking guarantee. Compare results on representative project tasks before fixing defaults. A smaller model can be a better choice for narrow tasks even if an expensive model is available.

The earlier internal profile names can be mapped to real, verified CLI configs later:

| Planning alias | Relative tier | Meaning |
| --- | --- | --- |
| `Luna` | Low | Cheap/fast, routine |
| `Terra` | Medium | Daily development |
| `Sol` | High | Complex reasoning and review |

These names are **local labels only**. They do not imply Codex exposes named selectable modes with these identifiers.

## 4. Selection algorithm

1. **Scope**: identify desired outcome, acceptance, file boundaries, security impact and data exposure.
2. **No-AI check**: ask whether an existing deterministic command can fully solve/validate the task.
3. **Classify**: set task complexity, failure impact and uncertainty; never estimate only by lines of code.
4. **Filter**: remove unavailable, unauthorised, incompatible, high-risk or over-budget CLI/model options.
5. **Recommend**: use the least resource-intensive remaining choice with plausible quality. Propose a reviewer only where independent judgement matters.
6. **Approve**: show user model/effort, mode, limits, review policy and allowed fallback ceiling; bind the approved specification/version.
7. **Verify at runtime**: coordinator rechecks CLI/model IDs, supported effort settings and credentials. Unknown unsupported parameters are errors, not silently ignored.
8. **Execute and measure**: track actual result, attempts and evidence; improve future routing from outcomes and benchmarks.

If models differ in quality but no relevant comparison exists, mark the recommendation **inferred**, not proven.

## 5. Effort, spending and quota guardrails

- **Desired effort** (`Low`, `Medium`, `High`, `Extra High`) is an internal policy scale, **not a promise every provider exposes these exact labels**. The adapter translates only supported settings and records the effective configuration.
- Start with the **minimum suitable** effort. Increase only for an evidence-based problem: repeated failure, difficult dependencies, ambiguous requirements, genuine security review.
- Always apply enforceable local hard limits: max wall-clock duration, iterations, retries, concurrent jobs, correction cycles, output/context size where controlled, and cancellation.
- **Owner preference:** preserve approximately 20% of usable subscription allowance (avoid spending past 80%). This is **not a hard quota safeguard** unless the provider exposes reliable, plan-specific telemetry. Rate-limits, rolling windows, token counts and subscription allowances can be different measurements.
- Where usage/remaining budget is unknown, show `unknown` and use conservative local limits. Do not infer tokens used from elapsed time or claim a reliable percentage.
- Never assume that a ChatGPT Plus or company-provided Claude account automatically allows unattended CLI usage. Confirm each provider's current rules and the organisation's permission before integration.

## 6. Review, fallback and escalation

- **SINGLE** for self-contained changes with deterministic verification; **HANDOFF** implementer→independent reviewer for higher-risk work; **PARALLEL** only for truly independent scopes; **WAIT** for dependencies/approval/unavailability.
- A second agent is not an always-on conversational companion. Reviewers receive only the approved requirement, diff and relevant test evidence (read-only by default).
- Prefer one implementation attempt and a tightly limited number of corrections; ask owner to approve new scope or higher budget when needed.
- An unavailable model may be replaced **only** by a verified, permitted model within the user-approved capability/usage/data ceiling. Otherwise **BLOCKED/WAIT**, with explanation.
- No silent upgrade to a more expensive tier, no automatic switch across security/data jurisdictions, and no relaxed review because a model asks.
- Changes to the model/version or effort setting must be recorded. If the exact model is locked in the approval hash, changing it requires reapproval.

## 7. Quality and audit metrics

Track actual observed values when available: task type, repository category, selected provider/model ID (or `unknown`), requested/effective effort, duration, attempts, reviewer verdict, tests, manual intervention, observed token usage where exposed, and unresolved defects. Compare median effort and failure rate only once enough equivalent examples exist.

Do not build a complicated routing model before a small test set proves that it improves work.

## 8. Examples

**Low-risk documentation:** run a deterministic linter, optionally one low-cost agent for wording. No second model by default.

**Bounded Django validation fix:** propose a verified Medium-tier Codex/Claude worker, then use tests; add separate Claude/Codex review if the bug affects access or data correctness.

**Complex worker-cleanup defect:** justify a High-capability implementer plus independent reviewer in HANDOFF, isolate changes and cap review loops. Escalate on unresolved test, uncertain PostgreSQL behaviour or increasing scope.

**Security-critical migration:** request explicit owner approval, strong allowed model for analysis, independent review and deterministic database tests; do not auto-merge.

In all cases ChatGPT's proposal is **advice**; the future Linux coordinator validates and enforces permissions. This public repo does not operate the model router yet.
