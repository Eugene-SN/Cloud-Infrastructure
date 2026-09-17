# Cloud Infrastructure — Accepted Implementation Phases

**Status:** Stage 0–2 COMPLETE / ACCEPTED; Stage 02.5 ACTIVE / RESEARCH-ONLY. Stage 3 composition is selected, but no post-Stage-2 production branch opens until Stage 02.5 is fully accepted.

This document is the canonical stage chronology for Cloud Infrastructure / `edge`.

## Core workflow rule

Each implementation stage has its own work branch and follows the accepted-first lifecycle:

1. requirements/baseline review;
2. legacy implementation reconstruction where relevant;
3. research/selection only for genuinely unresolved mechanisms or concrete incompatibilities;
4. explicit stage-composition acceptance;
5. stage-scoped architecture/deployment contract and recovery path;
6. deployment;
7. verification and explicit acceptance;
8. persistence/read-back in GitHub;
9. branch transition only after complete stage acceptance.

Do not reopen accepted products without a concrete incompatibility or changed requirement. Historical versions are evidence, not automatic pins. Docker + Compose remain the default for suitable application services; host-native placement is preferred where containerization materially complicates the supported operating model or integration with existing host-native executors.

## Roadmap construction rule after Stage 2

Post-Stage-2 work is ordered by dependency direction rather than by historical thematic categories.

The governing sequence is:

1. deploy Hermes as the one selected remaining standalone core service;
2. establish `edge ↔ ai-node ↔ PVE/Home` connectivity before services that depend on it;
3. deploy cross-site data/knowledge services such as files, selected-directory synchronization and Obsidian only after connectivity is accepted;
4. complete any other selected infrastructure services whose dependencies are now satisfied;
5. deploy Backrest + Restic and prove restore against the substantially complete service inventory;
6. deploy Semaphore and the maintenance/update workflow, then build `update.escloud.us` as a separate Codex substage against the real backend contract;
7. deploy infrastructure-wide monitoring, Home/PAI heartbeats and alerts after the monitored inventory and lifecycle services substantially exist;
8. build `app.escloud.us` as a separate Codex substage on top of the final service inventory and accepted monitoring/status sources;
9. perform final server-wide integrated acceptance and cleanup;
10. only after infrastructure acceptance, develop ongoing user-specific n8n/agent workflows as a separate continuously evolving workstream.

This prevents repeated rework of connectivity-dependent services, backup policy, update tooling, monitoring and portal composition.

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

Backrest, Semaphore, maintenance/update UI and `app.escloud.us` were deliberately moved out of Stage 2 so they can be designed against the substantially complete server.

---

## Stage 02.5 — Remaining Functional Scope Reconciliation & Research

### Work branch

`02.5 — Remaining Functional Scope Reconciliation & Research`

### Status

**ACTIVE / RESEARCH-ONLY / NO RUNTIME DEPLOYMENT.**

### Purpose

Stage 02.5 reconciles the complete remaining capability inventory, selects unresolved products/mechanisms, fixes dependency order and produces the final remaining roadmap before any new production branch opens.

### Research outcome classes

Each unresolved capability ends Stage 02.5 as one of:

- `SELECTED`;
- `REUSE EXISTING`;
- `DEFERRED`;
- `REJECTED`;
- `RESEARCH STILL REQUIRED` only where evidence is genuinely insufficient.

### Current accepted research result — Remaining Standalone Core Services

**Hermes Agent — SELECTED.**

Hermes is the only selected full service in this block. Its role is a persistent cloud-side agent runtime on `edge`, distinct from both n8n and the manual Cloud AI workspace.

Role separation:

- **n8n** — deterministic automation/orchestration: schedules, webhooks, mail/API triggers, data routing and workflow state;
- **Hermes** — agentic reasoning, tool use, supervisory/delegation logic and long-running autonomous agent execution;
- **CloudCLI / Codex CLI / Antigravity CLI** — manual cloud-AI workspace and specialized executors available directly to the user; Codex/Antigravity can also be delegated to by Hermes;
- **OpenClaw in Home/PAI** — local personal agent role;
- **vLLM on `ai-node`** — local inference backend, connected to Hermes only after cross-site connectivity exists.

Stage 3 should use a **host-native Hermes deployment under `core`** unless a concrete Stage 3 compatibility finding requires otherwise. Docker is not the preferred design because Hermes must directly reuse the existing host-native Codex/Antigravity executors and their working user context; containerizing Hermes would add avoidable binary/auth/runtime bridging.

Stage 3 must establish the infrastructure integration contract for this future flow without prematurely implementing user-specific workflows:

```text
Internet / schedule / mail / webhook
                |
               n8n
                |
        deterministic steps
                |
                v
             Hermes
        agentic reasoning
          +-----+-----+
          |     |     |
          v     v     v
        Codex   AGY   vLLM
          |             ^
          v             |
       result     enabled after Stage 4
          |
          v
         n8n
          |
notification / storage / next step
```

During Stage 3 the Codex and Antigravity branches can be implemented and verified locally on `edge`; the vLLM branch is explicitly deferred until Stage 4 connectivity is accepted. User-specific n8n/Hermes automations remain post-infrastructure work.

### Remaining Stage 02.5 research

Stage 02.5 still must research and disposition:

- cross-site connectivity and real flows;
- working-file access and web file management;
- MacBook/iPhone/iPad/`ai-node` access;
- selected-directory synchronization;
- free/self-hosted Obsidian synchronization while `ai-node:/srv/ai-data/knowledge/obsidian` stays canonical;
- any additional infrastructure service that proves necessary after those dependencies are understood;
- Backrest/off-site recovery topology details;
- external availability monitoring, dead-man/heartbeats and alert delivery;
- optional password/2FA vault, messaging/control frontend and limited failover;
- application/workflow capabilities, while their actual implementation remains outside the finite infrastructure build unless they require a dedicated infrastructure service.

No Stage 3 production branch becomes authoritative until the complete Stage 02.5 deliverables are explicitly accepted and canonical files are read back.

---

# Planned post-Stage-02.5 deployment roadmap

The dependency order below is accepted. Stage 3 composition is selected now; later stage composition remains subject to the relevant Stage 02.5 research decisions. If the conditional Stage 6 slot is empty at Stage 02.5 closure, it should be removed rather than creating an empty deployment branch, with later stage numbering normalized before Stage 3 opens.

## Stage 3 — Edge Hermes Agent Runtime

### Planned work branch

`03 — Edge Hermes Agent Runtime`

### Scope

Only Hermes and its infrastructure-level integration with already accepted local `edge` executors.

Planned requirements:

- host-native runtime under `core` by default;
- persistent upstream-supported service lifecycle;
- persistent Hermes state/configuration using the accepted host layout conventions where compatible with upstream;
- no new public WebUI/port/domain by assumption;
- direct Hermes access to Codex and Antigravity executors without routing through CloudCLI;
- a stable machine interface by which n8n can invoke Hermes and receive task result/status;
- verify the `n8n -> Hermes -> Codex/AGY -> Hermes -> n8n` infrastructure path with a minimal non-user-specific acceptance flow;
- reserve the `vLLM on ai-node` provider/inference branch in architecture, but do not implement it before Stage 4 connectivity;
- no Capture Inbox, vendor watchers, bounded research jobs or other user-specific automations in Stage 3.

## Stage 4 — Edge Cross-site Connectivity Foundation

### Planned work branch

`04 — Edge Cross-site Connectivity Foundation`

### Scope

Define real flows first, then select/deploy the minimum required transport/reachability among:

- `edge`;
- `ai-node`;
- PVE/Home Infrastructure.

Candidate mechanisms such as NetBird, direct WireGuard, authenticated HTTPS or another simple transport remain unselected until compared against actual flows and real operating conditions. This stage also enables the deferred Hermes -> local vLLM relationship after connectivity acceptance.

Connectivity is transport/reachability/endpoints. Durable application-level task queues/retry semantics remain a later workflow concern.

## Stage 5 — Edge Cross-site Data & Knowledge Services

### Planned work branch

`05 — Edge Cross-site Data & Knowledge Services`

### Scope

After Stage 4 acceptance, deploy the selected connectivity-dependent data services:

- VPS working-file access and web file management;
- MacBook/iPhone/iPad/`ai-node` access;
- selected-directory synchronization;
- Obsidian synchronization/relay/mirror role.

Canonical Obsidian remains `ai-node:/srv/ai-data/knowledge/obsidian`.

## Stage 6 — Edge Remaining Infrastructure Services

### Planned status

**CONDITIONAL.**

Use this stage only if the remaining Stage 02.5 research selects another full infrastructure service whose dependencies are satisfied after Stage 5 and which does not belong to backup/update/monitoring/portal layers. Do not create an empty branch merely to preserve numbering.

## Stage 7 — Edge Backrest & Recovery

### Planned work branch

`07 — Edge Backrest & Recovery`

### Scope

Deploy/configure the already accepted Backrest + Restic direction against the substantially complete server. Define:

- backup scope and exclusions;
- repository/off-site topology;
- retention and schedules;
- recovery procedures;
- verified restore acceptance.

A usable restore path is mandatory before Stage 8 update testing.

## Stage 8 — Edge Maintenance & Update

### Planned work branch

`08 — Edge Maintenance & Update`

### Scope

Deploy Semaphore and the maintenance/update workflow after Backrest acceptance. Audit/adapt the existing PVE/Home updater; do not copy PVE-specific implementation blindly.

Dedicated Codex substage:

**Stage 8C — Codex: build `update.escloud.us`**

This substage begins only after the real Semaphore/update backend, status model and control contract are known. `update.escloud.us` remains separate from `app.escloud.us`.

## Stage 9 — Edge Monitoring, Heartbeats & Alerts

### Planned work branch

`09 — Edge Monitoring, Heartbeats & Alerts`

### Scope

Deploy production monitoring against the substantially complete infrastructure, including as selected:

- `edge` service availability;
- important external availability checks;
- cross-site connectivity health;
- selected Home/PVE/`ai-node` heartbeats;
- file/sync health where useful;
- Backrest job/backup health;
- Semaphore/update health/state;
- alert delivery.

Avoid a heavyweight metrics/logging platform unless research proves concrete value.

## Stage 10 — Edge Cloud Portal

### Planned work branch

`10 — Edge Cloud Portal`

### Scope

Build `app.escloud.us` only after Stage 9 monitoring/status sources and the final service inventory are accepted.

Dedicated Codex substage:

**Stage 10C — Codex: build `app.escloud.us`**

The portal is navigation plus concise infrastructure/status presentation. It does not absorb detailed maintenance/update controls from `update.escloud.us`.

## Stage 11 — Edge Final Integrated Infrastructure Acceptance

### Planned work branch

`11 — Edge Final Integrated Infrastructure Acceptance`

### Scope

Perform final server-wide acceptance only after:

- all selected infrastructure services are accepted;
- cross-site connectivity and data/knowledge integration are accepted;
- Backrest backup/restore is accepted;
- Semaphore/update and `update.escloud.us` are accepted;
- monitoring/heartbeats/alerts are accepted;
- `app.escloud.us` is accepted;
- final cleanup is complete.

Stage 11 closes the finite Cloud Infrastructure build.

---

## Post-infrastructure continuous workstream — Automation & User Workflows

This is deliberately **not** an infrastructure-completion stage. It begins only after Stage 11 and evolves continuously.

Examples:

- n8n workflows;
- Hermes/agent workflows;
- Universal Capture Inbox — submission of URLs/text/files/images/commands into workflows;
- human-in-the-loop approvals;
- mail-triggered automation;
- continuous vendor/document intake and change detection;
- bounded AI research jobs;
- durable application-level store-and-forward/retry for real cross-site tasks;
- messaging/bot commands;
- user-specific orchestration among n8n, Hermes, Codex, Antigravity, local vLLM and other accepted endpoints.

Infrastructure stages should provide stable primitives for these workflows without attempting to prebuild the workflows themselves.

---

## Historical Stage 3–7 disposition

The previous thematic groupings:

- `03 — Edge Monitoring & Human Interaction`;
- `04 — Edge Files, Sync & Obsidian`;
- `05 — Edge Information & Cloud AI`;
- `06 — Edge Home & PAI Integration`;
- `07 — Edge Optional Capabilities`;

are historical planning context only and are not authoritative future deployment stages.

---

## Current canonical checkpoint

Stage 0: **COMPLETE / ACCEPTED**.  
Stage 1: **COMPLETE / ACCEPTED**.  
Stage 2: **COMPLETE / ACCEPTED**.  
Stage 02.5: **ACTIVE / RESEARCH-ONLY**.

Current branch:

`02.5 — Remaining Functional Scope Reconciliation & Research`

Current next research block: **Cross-site Connectivity Foundation**. Hermes selection for Stage 3 is accepted, but Stage 3 does not begin until all Stage 02.5 deliverables are accepted.