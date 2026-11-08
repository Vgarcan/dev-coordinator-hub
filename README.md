# Dev Coordination Hub

**Public, interactive user-interface prototype** for a proposed local, GitHub-bridged AI software-development coordinator. Designed mobile-first with [Glassmorphism Pro](https://github.com/Vgarcan/botstrap-css-styles).

> **Demo only.** This site does not connect to a Linux server, GitHub API, Codex or Claude. All repositories, activities, quotas and approvals shown inside the interface are fictional examples. Buttons change state inside the current browser tab only.

## Table of contents

1. [Live demo](#live-demo)
2. [Product idea](#product-idea)
3. [Repository structure](#repository-structure)
4. [Local preview](#local-preview)
5. [Roadmap](#roadmap)
6. [Security](#security)
7. [Design system](#design-system)

## Live demo

After enabling GitHub Pages from the `main` branch and the repository root, the intended URL is:

https://vgarcan.github.io/dev-coordinator-hub/

The address is **not verified as published** until GitHub Pages has deployed.

## Product idea

The planned product lets a user choose a code repository, authorize a task and assign it to Codex CLI and/or Claude Code running on a headless Linux server. A coordinator manages task status, approvals, reviews, and audit events. Initially, a private GitHub repository (or other access-controlled GitHub project channel) carries commands and results between ChatGPT and the server. The public demo is **not** that private channel.

## Repository structure

- `index.html` — standalone frontend concept, simulated in-memory data.
- `.nojekyll` — serves static files directly on GitHub Pages.
- `README.md` — purpose and setup.
- `docs/PROJECT_PLAN.md` — first-stage implementation plan.
- `docs/SECURITY.md` — separation of public and private surfaces.

## Local preview

From the repository root:

```bash
python3 -m http.server 8000
```

Open `http://localhost:8000/` in a modern browser. The interface currently references the original Glassmorphism Pro stylesheet and optional theme runtime hosted on another public GitHub Pages site; an application-specific CSS fallback is embedded in `index.html`.

## Roadmap

1. Public frontend concept and visual review.
2. Private Linux coordinator proof of concept: install official CLI tools and verify authorized authentication.
3. GitHub bridge: structured tasks, state transitions, idempotence and event records.
4. Isolated workers, repository checkout, automated validation and safe approval gates.
5. Authenticated private audit viewer integrated with the coordinator.

## Security

This is an intentionally non-operational static demo. **Never place tokens, credentials, private task descriptions, audit events, raw logs or any server secrets in this public repository or in GitHub Pages JavaScript.** The future Django coordinator and sensitive audit data belong on a private, authenticated service. See [Security boundaries](docs/SECURITY.md).

## Design system

UI styling is adapted from the owner's [Glassmorphism Pro](https://github.com/Vgarcan/botstrap-css-styles) theme. This demo loads the published theme CSS and optional JavaScript runtime from that separate repository. Its upstream files are not copied or relicensed here.

**Status:** early UI design concept; not production software.