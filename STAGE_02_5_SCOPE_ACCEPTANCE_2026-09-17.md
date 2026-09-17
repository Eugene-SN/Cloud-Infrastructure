# Stage 02.5 — Remaining Functional Scope Reconciliation & Research — Scope Acceptance

Date: 2026-09-17

Status: **ACCEPTED / ACTIVE**

## Purpose

Stage 02.5 is a research-only checkpoint between accepted Stage 2 and the next production deployment stage. It reconciles the complete remaining Cloud Infrastructure roadmap and defines a dependency-aware deployment order before any further production branch is opened.

No production deployment or configuration mutation is part of Stage 02.5.

## Accepted scope

Stage 02.5 must:

1. Analyze all remaining previously listed implementation stages together, not only historical Stage 3.
2. Reassess the current remaining tasks, dependencies and execution order.
3. Remove work already satisfied by Stage 1/2 and identify duplicate, misplaced, premature or dependency-inverted tasks.
4. Research every still-required infrastructure capability that lacks a selected concrete product/package/mechanism.
5. Determine where no new service is required because an already accepted component such as n8n, Stalwart/mail, nginx, Authelia, CloudCLI, Codex CLI or Antigravity CLI can satisfy the requirement adequately.
6. Preserve already accepted product anchors and avoid replacement research without a concrete incompatibility or changed requirement.
7. Produce a revised remaining roadmap before any next deployment branch is opened.
8. Separate infrastructure/service construction from later user-specific n8n/agent workflows so continually evolving application workflows do not block infrastructure completion.

## Accepted dependency-aware roadmap direction

The old thematic Stage 3–7 grouping is no longer authoritative. Future deployment must follow dependency direction:

1. **Remaining Standalone Core Services** — deploy any still-required full services that can operate independently on `edge` without future Home/PAI connectivity or late lifecycle tooling.
2. **Cross-site Connectivity Foundation** — establish the required `edge ↔ ai-node ↔ PVE/Home` transport/reachability before deploying services whose correctness depends on that connectivity.
3. **Cross-site Data & Knowledge Services** — only after connectivity, deploy selected working-file access, web file management, selected-directory synchronization, Obsidian synchronization/relay/mirror and other data services that depend on Home/PAI reachability.
4. **Remaining Infrastructure Services** — finish other selected infrastructure components once their dependencies are satisfied, producing a substantially stable final service inventory.
5. **Backrest & Recovery** — deploy/configure Backrest + Restic against the substantially complete system and prove a usable backup/restore path.
6. **Semaphore & Maintenance / Update** — deploy Semaphore and the maintenance/update workflow only after Backrest restore capability exists. `update.escloud.us` is a dedicated custom maintenance/update page, separate from `app.escloud.us`, and will be implemented in its own Codex substage after the real Semaphore/update backend contract is known.
7. **Monitoring, Heartbeats & Alerts** — deploy production monitoring only after the main service inventory, cross-site connectivity, Backrest and update subsystem substantially exist, so the monitoring layer can be built once against the finished infrastructure.
8. **`app.escloud.us` Portal** — build the final Cloud Infrastructure navigation/status dashboard after monitoring/status sources are accepted. This is a separate Codex substage. Detailed update controls remain on `update.escloud.us`.
9. **Final Integrated Infrastructure Acceptance** — execute only after all selected infrastructure services, connectivity/integration, backup/restore, update/maintenance, monitoring, portal and cleanup are accepted.
10. **Automation & User Workflows** — develop Capture Inbox, approval flows, mail-triggered automation, continuous information intake, bounded AI research, durable application-level task handoff, messaging commands and other user-specific n8n/agent workflows after the infrastructure framework is accepted. These workflows evolve continuously and are not infrastructure-completion blockers.

## Minimum research inventory

Research must still cover all unresolved infrastructure/service domains, including at minimum:

- remaining standalone full services that provide durable independent value on `edge`;
- `edge ↔ ai-node ↔ PVE/Home` connectivity and the real flows it must support;
- VPS working-file access and web file management;
- MacBook/iPhone/iPad/`ai-node` access mechanisms;
- selected-directory synchronization;
- free/self-hosted Obsidian synchronization and the useful `edge` role while the canonical vault stays on `ai-node`;
- remaining off-site/recovery topology details around the accepted Backrest/Restic direction;
- external uptime/availability monitoring;
- dead-man / heartbeat monitoring;
- alert and notification delivery mechanisms;
- optional messaging/control frontend where it represents an infrastructure service rather than merely a workflow interface;
- optional password/2FA vault;
- limited failover/secondary-endpoint role;
- Hermes only if it closes a concrete persistent-agent/runtime gap not covered by n8n + CloudCLI + Codex CLI + Antigravity CLI;
- any other accepted-scaffold capability that still lacks a concrete implementation decision.

Application/workflow capabilities such as Universal Capture Inbox, human-in-the-loop approvals, mail-triggered workflows, continuous information intake, bounded AI research and durable task store-and-forward remain part of the research matrix, but their actual implementation is normally deferred to the post-infrastructure workflow layer unless a dedicated infrastructure service proves necessary.

## Research outcome classes

Each capability must end Stage 02.5 with one of these outcomes:

- `SELECTED` — concrete product/mechanism accepted for later implementation;
- `REUSE EXISTING` — no new package/service is needed;
- `DEFERRED` — useful, but decision or implementation must wait for a concrete dependency;
- `REJECTED` — insufficient value or unnecessary duplication/complexity;
- `RESEARCH STILL REQUIRED` — only when available evidence is genuinely insufficient.

## Selection priorities

1. correctness / fit to the actual requirement;
2. simplicity;
3. minimum number of components and manual operations;
4. reliability and maintainability;
5. compatibility with accepted `edge`, Home Infrastructure and PAI architecture.

Do not import enterprise observability, IAM, security or orchestration complexity without a demonstrated need.

## Accepted lifecycle constraints

1. `app.escloud.us` is near-final and is built only after the service inventory and monitoring/status sources are substantially stable.
2. Backrest is deployed/configured before Semaphore update testing.
3. Semaphore and maintenance/update workflow are developed/tested together.
4. `update.escloud.us` is the dedicated custom maintenance/update page and is implemented in a separate Codex substage; do not fold detailed maintenance controls into `app.escloud.us`.
5. The existing PVE/Home update tooling is an engineering reference to audit/adapt, not a template to copy blindly.
6. Production monitoring is deployed after the main infrastructure, connectivity, Backrest and update subsystem exist.
7. `app.escloud.us` is implemented in a separate Codex substage after monitoring is accepted.
8. Final server-wide acceptance follows all above layers and final cleanup.
9. Ongoing user-specific automation/workflow development follows infrastructure acceptance rather than blocking it.

## Required deliverables

Stage 02.5 cannot close until the user explicitly accepts:

1. reconciled remaining capability inventory;
2. research matrix for every unresolved capability;
3. normalized remaining service/product inventory;
4. revised dependency graph and execution order;
5. final stage names/numbers/scopes;
6. explicit placement of Backrest, Semaphore + `update.escloud.us`, monitoring, `app.escloud.us` and final acceptance;
7. explicit list of intentionally unresolved decisions and the dependency blocking each;
8. canonical GitHub updates and read-back.

Only then may the next production deployment branch begin.

## Immediate next research block

`Remaining Standalone Core Services`

The next task is to determine which additional full, independently deployable services are genuinely required on `edge`, what functional gaps they close, and which concrete maintained packages should be selected. User-specific n8n/agent workflows are not part of this first service-selection block.
