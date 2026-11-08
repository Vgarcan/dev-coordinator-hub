# ChatGPT review role and possible MCP integration

**Status: design exploration only.** No endpoint, server listener, public
API, remote tool or agent execution is implemented by this document.

## Table of contents

1. [Roles and limitations](#roles-and-limitations)
2. [Review workflow](#review-workflow)
3. [Connectivity options](#connectivity-options)
4. [Future tool contract](#future-tool-contract)
5. [Security and decisions](#security-and-decisions)

## Roles and limitations

Dev Coordination Hub may use three reasoning participants, but **not three
equivalent always-on workers**:

- **ChatGPT:** interactive objective clarification, planning, evidence
  interpretation and additional audit when invoked by the user. It is not a
  constantly running background service or an independent approval authority.
- **Codex CLI:** potential scoped implementation or independent review worker,
  subject to verified local CLI support, permissions and owner approval.
- **Claude Code:** potential scoped implementation or independent reviewer,
  subject to the same checks and explicit permitted usage.

For meaningful independent review, a reviewer should ideally inspect the
changed diff and test evidence without simply trusting the implementer's
summary. A second ChatGPT pass can offer another perspective, but should not
be mistaken for deterministic validation or a review that authorises itself.

## Review workflow

1. Owner defines and approves an immutable, versioned task through the future
   private control channel.
2. A local coordinator validates policy and delegates approved work in a
   non-root, isolated environment.
3. The implementer produces a diff, checks, commit reference and a concise
   redacted evidence report.
4. Deterministic checks execute; an optional independent model reviewer
   evaluates the scoped output.
5. ChatGPT may retrieve approved *read-only* evidence and perform an
   additional audit when invoked, presenting findings for owner review.
6. The owner accepts, requests corrections, or rejects. No model may use its
   own recommendations as permission to merge, deploy, or widen scope.

## Connectivity options

**Phase 1 preference: private GitHub channel.** ChatGPT already has
authorised GitHub connector access when the user has connected it. A private
repository could hold restricted, redacted reports and task status, with
strict identity/scope checks on the Linux worker. Merely writing a GitHub
comment is not execution approval.

**Future option: a custom remote MCP integration.** ChatGPT could use named,
limited tools for safe task inspection and evidence retrieval instead of
receiving unrestricted shell access. This requires plan/workspace permission,
an authenticated and reachable remote MCP endpoint (or supported secure
tunnel for private networks), audited tool permissions, explicit owner
approval of sensitive writes and a threat-model review. Whether custom MCP
actions can be connected depends on the current ChatGPT plan and product
permissions; this is not assumed available.

There is **no requirement to publish Django or the host to the internet now**.
The public GitHub Pages demonstration must never become an operational API.

## Future tool contract

The following are *examples*, not registered endpoints or active actions:

| Proposed tool | Classification | Return or constraint |
| --- | --- | --- |
| `list_tasks` | Read | Only authorised task IDs and redacted state |
| `get_task_evidence` | Read | Versioned diff references, checks and safe audit summary |
| `review_result` | Read/analysis | Human-readable findings without mutating task state |
| `propose_task` | Write, future | Draft only, not approval or execution |
| `request_dispatch` | High-risk, future | Must pass independent identity and immutable-version approval gates |

Do not expose arbitrary shell execution, credentials, raw terminal logs,
filesystem browsing, direct Git pushes, or unrestricted local network access.

## Security and decisions

Before any MCP implementation: confirm plan support; compare private GitHub
against MCP for actual value; choose network accessibility and authenticated
transport; enforce per-tool allowlists and read-only defaults; assess prompt
injection, evidence redaction, replay protection, quota and audit retention.
Do not put real tokens in `.env.example`, public docs or GitHub Issues.

See [security](SECURITY.md), [architecture](ARCHITECTURE.md), and
[task protocol](TASK_PROTOCOL.md). This proposal does not change the
approved public/private separation, require deployment or authorise agents.
