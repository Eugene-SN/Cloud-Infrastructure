# Stage 02.5 — Remaining Functional Scope Reconciliation & Research — Scope Acceptance

Date: 2026-09-17

Status: **ACCEPTED**

## Purpose

Stage 02.5 is a research-only checkpoint between accepted Stage 2 and the next production deployment stage. It reconciles the complete remaining Cloud Infrastructure roadmap after the accepted late deferral of `app.escloud.us`, Backrest, Semaphore and the maintenance page.

No production deployment or configuration mutation is part of Stage 02.5.

## Accepted scope

Stage 02.5 must:

1. Analyze **all remaining previously listed implementation stages together**, not only historical Stage 3.
2. Reassess the current remaining tasks, dependencies and execution order.
3. Remove work already satisfied by Stage 1/2 and identify duplicate, misplaced, premature or dependency-inverted tasks.
4. Research every still-required capability that currently exists only as a functional requirement and does not yet have a selected concrete product/package/mechanism.
5. Determine where no new service is required because an already accepted component such as n8n, Stalwart/mail, nginx, Authelia, CloudCLI, Codex or Antigravity can satisfy the requirement adequately.
6. Preserve already accepted product anchors and avoid replacement research without a concrete incompatibility or changed requirement.
7. Produce a revised remaining roadmap before any next deployment branch is opened.

## Minimum research inventory

Research must cover all still-unresolved functional domains, including at minimum:

- external uptime/availability monitoring;
- dead-man / heartbeat monitoring;
- alert and notification delivery mechanisms;
- Universal Capture Inbox implementation surfaces;
- human-in-the-loop approval mechanisms/surfaces;
- mail-triggered automation where implementation choices remain unresolved;
- VPS working-file access and web file management;
- MacBook/iPhone/iPad/`ai-node` access mechanisms;
- selected-directory synchronization;
- free/self-hosted Obsidian synchronization and the useful `edge` role while the canonical vault stays on `ai-node`;
- continuous information intake / change detection additions beyond existing n8n capabilities;
- bounded cloud-AI research/agent orchestration additions;
- Hermes role, if any, relative to n8n, CloudCLI, Codex and Antigravity;
- durable `edge ↔ Home/PAI` task handoff / store-and-forward mechanism;
- eventual cross-site/private connectivity candidates driven by real required flows;
- remaining off-site/recovery topology details around the already accepted Backrest/Restic direction;
- optional messaging/control frontend;
- optional password/2FA vault;
- limited failover/secondary-endpoint role;
- any other accepted-scaffold capability that still lacks a concrete implementation decision.

## Research outcome classes

Each capability must end Stage 02.5 with one of these outcomes:

- `SELECTED` — concrete product/mechanism accepted for later implementation;
- `REUSE EXISTING` — no new package/service is needed;
- `DEFERRED` — useful, but decision must wait for a concrete dependency;
- `REJECTED` — insufficient value or unnecessary duplication/complexity;
- `RESEARCH STILL REQUIRED` — only when available evidence is genuinely insufficient.

## Selection priorities

1. correctness / fit to the actual requirement;
2. simplicity;
3. minimum number of components and manual operations;
4. reliability and maintainability;
5. compatibility with accepted `edge`, Home Infrastructure and PAI architecture.

Do not import enterprise observability, IAM, security or orchestration complexity without a demonstrated need.

## Accepted late-stage dependency constraints

Stage 02.5 may change stage numbering/grouping, but must preserve these already accepted relationships:

1. `app.escloud.us` is deployed near the end after the service inventory substantially stabilizes;
2. Backrest is deployed/configured before Semaphore update testing;
3. Semaphore and the maintenance page are developed/tested together;
4. the existing PVE/Home update tooling is an engineering reference to audit/adapt, not a template to copy blindly;
5. final server-wide acceptance follows portal, Backrest restore, Semaphore/update, maintenance integration and final cleanup.

## Required deliverables

Stage 02.5 cannot close until the user explicitly accepts:

1. reconciled remaining capability inventory;
2. research matrix for every unresolved capability;
3. normalized remaining service/product inventory;
4. revised dependency graph and execution order;
5. revised stage names/numbers/scopes where appropriate;
6. explicit placement of late portal / Backrest / Semaphore + maintenance / final acceptance;
7. explicit list of intentionally unresolved decisions and the dependency blocking each;
8. canonical GitHub updates and read-back.

Only then may the next production deployment branch begin.
