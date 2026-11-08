# Requirements register

**Status:** initial traceable baseline, pending PDD review. FR-01 to FR-11 preserve the original scope; FR-12/13 capture the subsequent model-selection and coordination requirements. Implementation evidence is not yet available.

## Table of contents

1. [Functional requirements](#functional-requirements)
2. [Nonfunctional requirements](#nonfunctional-requirements)
3. [Traceability rules](#traceability-rules)

## Functional requirements

| ID | Priority | Expected capability / testable outcome |
| --- | --- | --- |
| FR-01 | Must | Register an **approved** source repo and select it per task; reject unlisted target repos |
| FR-02 | Must | Detect local checkout, safely clone if absent, and never overwrite dirty changes or auto-run repository scripts |
| FR-03 | Must | Check official CLI installation, viable authentication and availability/failure status before dispatch |
| FR-04 | Must | Run only valid, scoped, nonexpired, explicitly approved **task versions** from authorised actors |
| FR-05 | Must | Run isolated, bounded work with timeouts, attempt limits, error handling and cancellation |
| FR-06 | Must | Return structured result: status, summary, validation evidence, SHA/PR reference and blocking reason |
| FR-07 | Must | Support optional independent review without write access by default |
| FR-08 | Must | Preserve task state and deduplicate delivery across process restart and network failure |
| FR-09 | Should | Global pause/kill switch and limits for concurrency, retries, duration and available budget |
| FR-10 | Should | Record comparable duration, interventions, review loops, failures and reliable usage information |
| FR-11 | Later | Private authenticated Django audit viewer/foro, reading the same authoritative task state |
| FR-12 | Must | ChatGPT proposes NO_AI or a verified-eligible agent/model/effort tier, reviewer and coordination mode with rationale and obtains approval before dispatch |
| FR-13 | Must | Coordinator verifies model/effort support and enforces the approved fallback, tier, runtime and retry constraints; unknown quota telemetry must not be shown as measured |

## Nonfunctional requirements

| ID | Area | Constraint and verification |
| --- | --- | --- |
| NFR-SEC-01 | Privilege | Agents run non-root with distinct identities and least-privilege filesystem access |
| NFR-SEC-02 | Networking | MVP coordinator requires no publicly exposed inbound API/SSH route |
| NFR-SEC-03 | Secrets | No secrets in public Git, prompts, Issues, Pages, logs or artifacts |
| NFR-SEC-04 | Approval | Sensitive actions and changes of scope require explicit human approval, including immutable task version |
| NFR-REL-01 | Reliability | Restart/retry cannot execute an already-claimed task twice |
| NFR-REL-02 | Resilience | Handle GitHub unavailability, rate limits, worker crashes and cancellation safely |
| NFR-QA-01 | Quality | Readable maintainable Python, automated tests, structured logs and code review |
| NFR-UX-01 | Usability | Select repo → agree plan → authorise → inspect outcome, usable from mobile |
| NFR-PERF-01 | Efficiency | Deterministic checks do not invoke AI; bounded context and review loops |
| NFR-PERF-02 | Model economy | Use lowest suitable available capability, optional independent review, conservative time/attempt budgets and evidence-based escalation |
| NFR-UX-02 | Explainability | Before approval, the user can see proposed agents/models, effort, mode, estimated limitations, allowed fallback and reasons |
| NFR-PORT-01 | Portability | Headless Linux; no dependency on VS Code, web control panels or a specific distro |

## Traceability rules

- Each implementation Issue names its requirement IDs.
- Each PR names linked Issues, validation evidence and affected requirements.
- Unverified provider account limits and permitted enterprise Claude usage remain open feasibility checks, not hidden assumptions.
- A passed automated check supports an acceptance criterion; it is not evidence of complete security or user approval.
- The public demonstration is **not** evidence of FR-01 to FR-11 being implemented.
