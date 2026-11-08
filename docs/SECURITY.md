# Security Boundaries

## Contents

1. Public demo
2. Future private coordinator
3. Execution policy
4. Audit expectations

## Public demo

The GitHub Pages site is **public by definition**. It serves mock UI data only, does not store secrets, and does not connect to the actual server. Browser JavaScript is always visible to visitors and cannot safely hold an API key.

## Future private coordinator

The eventual Django/worker service should run as a dedicated non-root account with scoped permissions. Initially, the server makes outbound requests to a private GitHub channel. Do not expose the host, its SSH port or private logs solely to power the UI concept.

Do not store credentials in Git history, workflow YAML, issue descriptions or build artifacts. Use restricted deployment identities and separate credentials for the coordinator and for repository cloning/PR operations.

## Execution policy

Treat instructions from issues, repository files and model responses as untrusted. Only explicitly approved, current and scope-limited tasks may trigger command execution. Use an allowlisted checkout target, isolation, limited network/file access, bounded resource use, cancellations, approval gates, and no root permissions.

## Audit expectations

Real audit records must be authenticated and access-controlled, with attributable actor, timestamps, task/repository IDs, policy decisions, subprocess and review outcomes, and references to commits/PRs. A public GitHub Pages dashboard must **never** disclose live logs or private project names.
