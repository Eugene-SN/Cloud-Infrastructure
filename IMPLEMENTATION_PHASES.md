# Cloud Infrastructure — Accepted Implementation Phases

**Status:** ACCEPTED chronology; Stage 02.5 is the active research/reconciliation checkpoint and all post-Stage-2 deployment stages remain subject to its final acceptance.

This document is the canonical stage chronology for Cloud Infrastructure / `edge`.

## Core workflow rule

Each implementation stage has its own work branch and follows the accepted-first lifecycle:

1. requirements/baseline review;
2. legacy implementation reconstruction where relevant;
3. deployment of known/accepted dependency-ready components;
4. research/selection only for genuinely unresolved mechanisms or concrete incompatibilities;
5. stage-composition acceptance;
6. stage-scoped architecture/deployment contract;
7. deployment;
8. verification/acceptance;
9. persistence/read-back in GitHub;
10. branch transition only after complete stage acceptance.

Do not reopen accepted products without a concrete reason. Historical versions are evidence, not automatic pins. Docker + Compose are the default runtime for suitable application services; host-native remains valid where materially simpler.

## Roadmap construction rule after Stage 2

Post-Stage-2 work is ordered by dependency direction rather than by broad thematic categories.

The governing sequence is:

1. deploy remaining standalone core services that can be fully accepted on `edge` without depending on future Home/PAI integration or late lifecycle tooling;
2. establish the required `edge ↔ ai-node ↔ PVE/Home` connectivity foundation before deploying services whose correctness depends on that connectivity;
3. deploy cross-site data/integration services such as working-file access, selected-directory synchronization and Obsidian synchronization only after the transport they depend on is accepted;
4. finish any remaining infrastructure services so the production service inventory is substantially stable;
5. deploy Backrest and prove backup/restore against the substantially complete server;
6. deploy Semaphore and the dedicated maintenance/update surface together, using working Backrest pre-update backups during update testing;
7. deploy infrastructure-wide monitoring/heartbeats/alerts only after the monitored service inventory, cross-site connectivity and lifecycle services substantially exist;
8. build the final `app.escloud.us` portal on top of the accepted monitoring/status sources and final service inventory;
9. perform final server-wide integrated acceptance and cleanup;
10. only after the infrastructure framework is accepted, develop ongoing user-specific n8n/agent automations and application workflows as a separate, continuously evolving layer.

This prevents repeated rework of monitoring, backup policy, update tooling and portal composition as new services are added.

---

## Stage 0 — Discovery, preservation and migration preparation

### Work branch

`00 — Cloud Infrastructure Architecture Discovery & Target Design`

### Status

**COMPLETE / ACCEPTED.**

Accepted outcome includes the historical legacy baseline, provider backup, sensitive migration-preservation archive, sanitized `migration-reference/`, clean-rebuild decision and verified recovery paths.

---

## Stage 1 — Base `edge` Platform

### Work branch

`01 — Edge Clean Rebuild & Base Platform Deployment`

### Status

**COMPLETE / ACCEPTED.**

Final acceptance:

`EDGE_STAGE1_FINAL_INTEGRATED_ACCEPTANCE=PASS`

Accepted composition includes Ubuntu substrate, SSH, journald policy, Docker/Compose, nginx, Certbot/TLS lifecycle, Xray, Hysteria2, public masking page, Authelia ingress/auth foundation, UFW, `maintctl`/`vpnctl`, extension-point contract and the Stage 1 recovery checkpoint.

---

## Stage 2 — Core Applications

### Work branch

`02 — Edge Core Applications`

### Status

**COMPLETE / ACCEPTED.**

Final acceptance:

`EDGE_STAGE2_FINAL_INTEGRATED_ACCEPTANCE=PASS`

Accepted Stage 2 production set:

- Authelia clean reinitialization;
- n8n;
- CloudCLI;
- Codex CLI;
- Antigravity CLI;
- Stalwart;
- Bulwark;
- accepted mail migration, DNS/DKIM/TLS/public-protocol contract and external bidirectional E2E verification.

Backrest, Semaphore, the maintenance/update page and the full private `app.escloud.us` portal were explicitly removed from Stage 2 completion scope because their correct design depends on a substantially complete final service inventory.

---

## Stage 02.5 — Remaining Functional Scope Reconciliation & Research

### Work branch

`02.5 — Remaining Functional Scope Reconciliation & Research`

### Status

**ACTIVE / RESEARCH-ONLY / NO RUNTIME DEPLOYMENT.**

### Purpose

Stage 02.5 is the post-Stage-2 architecture/research checkpoint for the entire remaining Cloud Infrastructure roadmap. It reconciles the full remaining capability inventory, selects unresolved products/mechanisms where evidence permits, and replaces the old thematic Stage 3–7 ordering with dependency-aware deployment stages.

### Accepted dependency-aware direction

Stage 02.5 must preserve the following execution model:

1. `Remaining Standalone Core Services` first;
2. `Cross-site Connectivity Foundation` before any service that requires Home/PAI connectivity;
3. cross-site file/sync/Obsidian/integration services after connectivity;
4. all remaining infrastructure services before infrastructure-wide lifecycle/presentation layers;
5. Backrest before Semaphore/update testing;
6. Semaphore plus a dedicated maintenance/update page as one workstream;
7. monitoring/heartbeats/alerts after the service inventory and lifecycle components substantially exist;
8. final `app.escloud.us` after monitoring/status sources are accepted;
9. final integrated infrastructure acceptance;
10. user-specific n8n/agent workflows after the infrastructure framework is accepted.

### Required research domains

Research must still cover every unresolved functional domain, including:

- remaining standalone full services that provide enduring infrastructure value on `edge`;
- `edge ↔ ai-node ↔ PVE/Home` connectivity and the actual flows it must support;
- VPS working-file access and web file management;
- MacBook/iPhone/iPad/`ai-node` file access;
- selected-directory synchronization;
- free/self-hosted Obsidian synchronization while `ai-node:/srv/ai-data/knowledge/obsidian` remains canonical;
- off-site/recovery topology around the accepted Backrest/Restic direction;
- monitoring, external availability checks, dead-man/heartbeats and alert delivery;
- optional messaging/control frontend, password/2FA vault and limited failover/secondary endpoint;
- Hermes or any other additional agent runtime only if it closes a concrete gap not already satisfied by n8n, CloudCLI, Codex CLI and Antigravity CLI;
- application/workflow capabilities such as Capture Inbox, approvals, mail-triggered automation, durable store-and-forward and bounded AI research, while recognizing that their deployment belongs to the post-infrastructure workflow layer unless they prove to require a dedicated infrastructure service.

### Research outcome classes

Each unresolved capability must end Stage 02.5 with one of:

- `SELECTED` — concrete product/mechanism accepted for later implementation;
- `REUSE EXISTING` — no new package/service required;
- `DEFERRED` — useful but correctly decided only after a later dependency becomes concrete;
- `REJECTED` — insufficient value or unnecessary duplication/complexity;
- `RESEARCH STILL REQUIRED` — only when available evidence is genuinely insufficient.

### Required Stage 02.5 deliverables

Before Stage 02.5 closes, explicitly accept:

1. reconciled remaining capability inventory;
2. research matrix for every unresolved capability;
3. normalized remaining service/product inventory;
4. revised dependency graph and execution order;
5. final post-Stage-2 stage names/numbers/scopes;
6. explicit placement of Backrest, Semaphore + maintenance/update page, monitoring, `app.escloud.us` and final integrated acceptance;
7. explicit list of intentionally deferred decisions and their blocking dependencies;
8. canonical GitHub updates and read-back.

No production deployment branch after Stage 2 becomes authoritative until these deliverables are accepted.

---

## Provisional post-Stage-02.5 deployment skeleton

The following is an **accepted dependency skeleton, not yet the final numbered roadmap**. Exact stage numbers and component composition will be finalized after the research matrix is accepted.

### A. Remaining Standalone Core Services

Deploy any still-required full services that can operate and be accepted independently on `edge` without relying on later Home/PAI connectivity, monitoring, backup-management or update/portal layers.

This stage intentionally excludes user-specific n8n workflows and agent tasks; those belong to the post-infrastructure application/workflow layer.

### B. Cross-site Connectivity Foundation

Define and deploy the minimum required transport between `edge`, `ai-node` and PVE/Home from real flows. Compare NetBird, direct WireGuard, authenticated HTTPS and other simple mechanisms only against those requirements.

The stage establishes connectivity, routing/reachability and required machine endpoints. It does not prematurely implement application-level durable queues or user workflows.

### C. Cross-site Data & Knowledge Services

After connectivity is accepted, deploy services that depend on it, including as selected by Stage 02.5 research:

- VPS working-file access and web file management;
- cross-device access from MacBook/iPhone/iPad/`ai-node`;
- selected-directory synchronization;
- Obsidian synchronization/relay/mirror role while the canonical vault remains on `ai-node`.

### D. Remaining Infrastructure Services

Deploy any other selected infrastructure service whose dependencies are now satisfied, so the overall production service inventory becomes substantially stable before lifecycle tooling is finalized.

### E. Backrest & Recovery

Deploy/configure the already accepted Backrest + Restic direction against the substantially complete server. Define repositories, exclusions, schedules, retention, off-site topology and verified restore procedures.

Backrest restore acceptance is mandatory before update testing.

### F. Semaphore & Maintenance / Update

Deploy Semaphore and the maintenance/update surface together, using the working PVE/Home update tooling as an engineering reference that is audited and adapted for `edge` rather than copied blindly.

The dedicated custom maintenance/update page is `update.escloud.us`; it is separate from the general `app.escloud.us` portal.

A dedicated Codex substage will build `update.escloud.us` only after the real Semaphore/update backend contract and status/control interfaces are known.

### G. Monitoring, Heartbeats & Alerts

Deploy production monitoring only after the infrastructure it monitors substantially exists. The final monitoring scope may include:

- `edge` service availability;
- cross-site connectivity;
- selected Home/PVE/`ai-node` heartbeats;
- file/sync health where useful;
- Backrest backup/job health;
- Semaphore/update health/state;
- important external availability checks and alert delivery.

Avoid a heavyweight metrics/logging stack unless Stage 02.5 research demonstrates concrete value.

### H. `app.escloud.us` Portal

Build the private Cloud Infrastructure portal after the final service inventory and monitoring/status sources are known.

The portal is a navigation/status surface, not a replacement operational control plane. Detailed update/maintenance control remains on `update.escloud.us`.

A dedicated Codex substage will build `app.escloud.us` against the accepted service URLs and monitoring/status interfaces.

### I. Final Integrated Infrastructure Acceptance

Perform server-wide acceptance only after:

- all selected infrastructure services are accepted;
- cross-site integration is accepted;
- Backrest backup/restore is accepted;
- Semaphore/update and `update.escloud.us` are accepted;
- monitoring/alerts are accepted;
- `app.escloud.us` is accepted;
- final cleanup is complete.

### J. Automation & User Workflows

This is a separate post-infrastructure layer rather than a blocker for infrastructure completion.

Examples include:

- Universal Capture Inbox — user submission of URLs/text/files/images into workflows;
- human-in-the-loop approvals — approve/reject/choice gates inside n8n/agent workflows;
- mail-triggered automation;
- continuous vendor/document intake;
- bounded AI research jobs;
- durable application-level store-and-forward/retry for cross-site tasks;
- user-facing bot/messaging commands;
- ongoing Codex/Antigravity/CloudCLI orchestration.

These workflows will evolve continuously and therefore should not prevent the infrastructure itself from reaching final acceptance.

---

## Historical Stage 3–7 disposition

The previous historical groupings:

- `03 — Edge Monitoring & Human Interaction`;
- `04 — Edge Files, Sync & Obsidian`;
- `05 — Edge Information & Cloud AI`;
- `06 — Edge Home & PAI Integration`;
- `07 — Edge Optional Capabilities`;

are retained only as historical planning context and are **not authoritative future deployment stages**. They mixed infrastructure services, cross-site dependencies, late lifecycle tooling and user workflows in ways that would cause repeated rework.

Final replacement stage numbering will be accepted at the end of Stage 02.5.

---

## Current canonical checkpoint

Stage 0: **COMPLETE / ACCEPTED**.  
Stage 1: **COMPLETE / ACCEPTED**.  
Stage 2: **COMPLETE / ACCEPTED**.  
Stage 02.5: **ACTIVE / RESEARCH-ONLY**.

Current branch:

`02.5 — Remaining Functional Scope Reconciliation & Research`

Next activity: research and selection for **Remaining Standalone Core Services** before any new production deployment branch is opened.
