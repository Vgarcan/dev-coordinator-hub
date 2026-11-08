# Dev Coordination Hub

An auditable, human-supervised development coordinator: plan work in ChatGPT, exchange authorised tasks through **private GitHub**, and run bounded Codex CLI / Claude Code jobs on a headless Linux server.

**Current status: documentation and public UI prototype only.** No coordinator backend, agent runtime or secure command channel is deployed.

> **Public-repository boundary:** this repository and its GitHub Pages demo are public. They must never be used for real agent instructions, confidential repo information, credentials, live audit logs, execution authorisations or operational payloads.

## Table of contents

1. [Try the public demo](#try-the-public-demo)
2. [Start with the documentation](#start-with-the-documentation)
3. [How we collaborate on GitHub](#how-we-collaborate-on-github)
4. [Product boundaries](#product-boundaries)
5. [Local preview](#local-preview)
6. [Design system](#design-system)

## Try the public demo

[Dev Coordination Hub — GitHub Pages](https://vgarcan.github.io/dev-coordinator-hub/)

The page is a **simulated, mobile-first mock-up** with fictional repositories, agents, task statuses and usage numbers. It makes no external write requests and does not execute work.

## Start with the documentation

- [Documentation index](docs/README.md) — recommended reading order.
- [Project Definition Document](docs/PDD.md) — objective, boundaries, MVP and approvals.
- [Architecture](docs/ARCHITECTURE.md) — public UI vs private control vs Linux worker.
- [Requirements](docs/REQUIREMENTS.md) — traceable functional and nonfunctional requirements.
- [Roadmap](docs/PROJECT_PLAN.md) — phased delivery and exit gates.
- [GitHub collaboration](docs/GITHUB_WORKFLOW.md) — issues, PRs, decisions and evidence.
- [Task protocol](docs/TASK_PROTOCOL.md) — proposed private task and review lifecycle.
- [ChatGPT–agent collaboration](docs/CHATGPT_AGENT_COLLABORATION.md) — how ChatGPT plans, recommends, delegates and supervises.
- [Model selection and budget policy](docs/MODEL_SELECTION_POLICY.md) — verified model choice, reasoning depth and efficiency.
- [Decision register](docs/DECISIONS.md) and [risk register](docs/RISKS.md).
- [Security](docs/SECURITY.md).
- [Codex project instructions](AGENTS.md) and [Claude Code project instructions](CLAUDE.md) — small agent briefs; they do **not** replace enforced runtime security.

## How we collaborate on GitHub

**Issues** hold proposals, defects, research and decisions (public-safe only). **Branches and pull requests** hold changes and their reviews. **Markdown documents** hold approved, durable architecture and product context. The **main branch** stays the reviewed source of truth. See [collaboration rules](docs/GITHUB_WORKFLOW.md) and the issue/PR templates.

The future *private control repository* is a separate, access-controlled resource, not this public repository.

## Product boundaries

- User and ChatGPT plan, review and approve; ChatGPT is **not** a continuously-running daemon.
- The server will eventually fetch approved work using outbound GitHub connections.
- Agent CLIs will run without VS Code and without root, after authentication/terms-of-use feasibility is established.
- No public API or open inbound port is required for the initial coordinator.
- No autonomous merge, deployment, destructive operation, or open-ended agent debate.
- The 80% subscription reserve is a **desired policy**, not an enforceable limit without official, reliable provider telemetry.

## Local preview

```bash
python3 -m http.server 8000
```

Open http://localhost:8000/ from this repository root. The demo references the original Glassmorphism Pro styling hosted in the [Bootstrap theme collection](https://github.com/Vgarcan/botstrap-css-styles).

## Design system

The public demo uses [Glassmorphism Pro](https://vgarcan.github.io/botstrap-css-styles/?theme=glassmorphism-pro), with the external original CSS/optional theme runtime and app-specific presentation. The theme repository remains independent; do not silently copy or relicense its files.

**Documentation status:** foundation draft for review; no automatic authorisation is implied by merging a documentation PR.
