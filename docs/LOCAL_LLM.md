# Dev Coordinator Hub — local Ollama smoke pilot

**Status:** implemented *optional read-only prototype*. Runtime validation
against the user's Ollama server and GPU is **not yet performed**.

## Table of contents

1. [What is integrated](#what-is-integrated)
2. [Configuration](#configuration)
3. [Manual smoke test](#manual-smoke-test)
4. [Trust boundaries](#trust-boundaries)
5. [Acceptance and next phase](#acceptance-and-next-phase)

## What is integrated

The standard-library adapter at `backend/local_llm/ollama.py` can:

- Read the installed model inventory using Ollama's `GET /api/tags`.
- Classify one short, **non-sensitive** diagnostic with `POST /api/generate`.
- Reject uninstalled models, malformed responses and anything except one of
  four labels: `configuration`, `dependency`, `test_failure`, `unknown`.
- Limit request duration (1–60 seconds), context (2,048 tokens), generation
  (24 tokens), prompt length (1,200 characters), response (256 KiB) and
  unload the model after each call (`keep_alive=0`).

`backend/scripts/ollama_pilot.py` deliberately requires either
`--inventory` or `--benchmark`. The latter runs **six synthetic examples**,
sequentially (one call at a time), and counts correct classifications.
There are no file edits, git writes, subprocess agent executions, job
permissions, scheduler or automatic paid-model fallback.

## Configuration

Install the normal Django development dependencies first, for example via
`python3 backend/scripts/setup_local.py` (or your existing venv). Ollama is
installed and managed separately. The adapter never downloads or starts a
model for you. For first tests, prefer a *small model you already have
installed*, around 3B–4B, and inspect actual VRAM use on your 12 GB RTX 3060.

Manually create `backend/.env` from `backend/.env.example` and set:

```dotenv
# These are examples, not real credentials or a required model tag.
DCH_OLLAMA_ENABLED=1
DCH_OLLAMA_URL=http://127.0.0.1:11434
DCH_OLLAMA_MODEL=<name-returned-by-inventory>
DCH_OLLAMA_TIMEOUT_SECONDS=30
DCH_OLLAMA_ALLOWED_LAN_IP=
```

The selected model **must** already be installed in Ollama. Use the exact
tag shown by `--inventory`; there is no hard-coded default model. To reach
Ollama on another machine in your own LAN, use an RFC1918 IPv4 address
(e.g. `http://192.168.1.50:11434`) and set
`DCH_OLLAMA_ALLOWED_LAN_IP=192.168.1.50` to the **same** address. This is
an exact allowlist, not a LAN scan. Never port-forward an unauthenticated
Ollama service or publish its URL publicly.

Local `.env` is ignored by Git, and OS environment variables take
precedence. The public `.env.example` contains no secrets.

## Manual smoke test

From the repository root with dependencies installed:

```bash
# Read-only model list; loads no model into GPU.
python backend/scripts/ollama_pilot.py --inventory

# Exactly six invented classification inputs; opt-in inference.
python backend/scripts/ollama_pilot.py --benchmark

# Unit tests: no Ollama service or GPU is required.
cd backend
python -m unittest discover -s scripts -p 'test_local_llm.py' -v
```

A benchmark success only means the six examples matched; it is **not**
permission to delegate real code or report reliable accuracy. Errors or
mismatches cause a nonzero exit. Record wall time and local VRAM
measurements separately; neither savings nor memory utilisation is known
until measured.

## Trust boundaries

- Disabled unless `DCH_OLLAMA_ENABLED=1` is set explicitly.
- HTTP restricted to loopback or a single explicitly allowlisted private IPv4
  address. No proxy or HTTP redirects, no cloud endpoint or cloud model tags.
- No private logs, credentials, unreviewed repo content or user data should be
  submitted. Strict output validation does **not** establish model truth.
- No shell, GitHub control, repository write, approval, MCP endpoint or remote
  agent capability. This does not integrate with AI Hub.
- Local LLM errors **fail closed**, with no automatic retry or paid escalation.

## Acceptance and next phase

Run the offline tests, confirm that the installed small model can be listed,
then run the six-case pilot on the actual Ollama host. Measure results,
time, and VRAM usage. Only after reviewing those measurements should the
owner consider allowing narrowly scoped local tasks with deterministic
validation, persistent audit logs, bounded concurrency and an approved
escalation policy. The private coordinator is not implemented yet.
