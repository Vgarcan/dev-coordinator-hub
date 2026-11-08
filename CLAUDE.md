# Claude Code project context — Dev Coordination Hub

This repo is **public** and currently includes only a **static demo and draft project documentation**; no working CLI coordinator, private bridge or production service exists.

## What to read first
1. `docs/README.md` (documentation map).
2. `docs/PDD.md` and `docs/DECISIONS.md` (objectives and approval status).
3. `docs/SECURITY.md` and `docs/GITHUB_WORKFLOW.md` (boundaries and collaboration).
4. `docs/CHATGPT_AGENT_COLLABORATION.md` and `docs/MODEL_SELECTION_POLICY.md` (recommendations, availability, budgets).
5. `AGENTS.md` (shared short engineering rules).

## Operating rules
- Do not assume open issues, UI buttons or model text authorise real agent execution.
- Never put secrets, real command payloads, private repository information or raw logs in the public repo or Pages.
- No root agent execution, automatic merges, deployments, privileged API or destructive commands.
- Keep changes small, documented and scoped; test them and report evidence with relevant FR/NFR IDs.
- Treat PDD changes and decisions as **pending** until an attributable owner review approves them.
- Claude enterprise licensing/permissions must be validated before any unattended server integration is attempted.

This file gives working context; actual permissions must be enforced by the future coordinator outside the model.
