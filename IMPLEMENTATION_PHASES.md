# Cloud Infrastructure — Accepted Implementation Phases

**Status:** Stage 0–2 COMPLETE / ACCEPTED; Stage 02.5 ACTIVE / RESEARCH-ONLY. No post-Stage-2 production branch opens until Stage 02.5 is fully accepted.

This document is the canonical stage chronology for Cloud Infrastructure / `edge`.

## Core workflow rule

Each implementation stage has its own work branch and follows the accepted-first lifecycle:

1. requirements/baseline review;
2. legacy implementation reconstruction where relevant;
3. research only for genuinely unresolved mechanisms or concrete incompatibilities;
4. explicit stage-composition acceptance;
5. stage-scoped architecture/deployment contract and recovery path;
6. deployment;
7. verification and explicit acceptance;
8. persistence/read-back in GitHub;
9. branch transition only after complete stage acceptance.

Do not reopen accepted products without a concrete incompatibility or changed requirement. Docker + Compose remain the default for suitable application services; host-native placement is preferred where containerization materially complicates the supported operating model or integration with existing host-native executors.

## Dependency order after Stage 2

The accepted post-Stage-2 sequence is dependency-driven:

1. establish the cross-site private connectivity foundation first;
2. deploy Hermes only after that foundation exists so Hermes can be accepted with Codex, Antigravity and local vLLM in one coherent stage;
3. deploy connectivity-dependent data/knowledge services;
4. complete any other selected infrastructure services whose dependencies are satisfied;
5. deploy Backrest + Restic and prove restore against the substantially complete service inventory;
6. deploy Semaphore and the maintenance/update workflow, then build `update.escloud.us` as a separate Codex substage against the real backend contract;
7. deploy infrastructure-wide monitoring, Home/PAI heartbeats and alerts after the monitored inventory and lifecycle services substantially exist;
8. build `app.escloud.us` as a separate Codex substage on top of the final service inventory and accepted monitoring/status sources;
9. perform final server-wide integrated acceptance and cleanup;
10. only after infrastructure acceptance, develop ongoing user-specific n8n/agent workflows as a separate continuously evolving workstream.

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

Accepted production set:

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

Stage 02.5 reconciles the remaining capability inventory, selects unresolved products/mechanisms, fixes dependency order and produces the final remaining roadmap before any new production branch opens.

### Accepted research result — Hermes

**Hermes Agent — SELECTED.**

Role separation:

- **n8n** — deterministic automation/orchestration;
- **Hermes** — persistent agentic reasoning, tools, supervision and delegation;
- **CloudCLI** — manual web/remote Cloud AI workspace;
- **Codex CLI / Antigravity CLI** — specialized executors usable manually and delegatable by Hermes;
- **OpenClaw** — Home/PAI local personal-agent role;
- **vLLM on `ai-node`** — local inference backend to be consumed by Hermes after Stage 3 connectivity exists.

Preferred Hermes placement is host-native under `core` unless a concrete Stage 4 compatibility finding requires otherwise.

### Accepted research result — Cross-site Connectivity Foundation

**Existing self-hosted NetBird — SELECTED / REUSE EXISTING.**

The accepted architecture is documented in `STAGE_02_5_CONNECTIVITY_SELECTION_ACCEPTANCE_2026-09-17.md`.

Key contract:

- reuse Home CT300 self-hosted NetBird control/relay/routing architecture;
- NetBird account overlay is `100.105.0.0/16`;
- CT300 remains the routing peer for Home LAN `192.168.1.0/24`;
- `edge` becomes an ordinary host-native NetBird service peer;
- `edge` receives Home LAN reachability but **not** the existing Home Internet resource `0.0.0.0/0`;
- `edge` keeps its VPS-provider default Internet route;
- Home/PAI clientless hosts reach `edge` through gateway-level routing of `100.105.0.0/16` via CT300 `192.168.1.90`;
- route semantics must work through both VM100 and MikroTik so VRRP ownership does not change private reachability;
- reuse the existing NetBird-managed Site-to-VPN masquerade behavior before considering any manual duplicate NAT;
- reuse the existing `.lan` split-DNS (`192.168.1.1:53` for match domain `lan`) on `edge`; general Internet DNS remains VPS-local;
- add `edge.lan` through the existing Home DNS mechanism after enrollment/routing acceptance;
- direct WireGuard and Tailscale are rejected as duplicate parallel backbones; AmneziaWG remains contingency only if real NetBird transport acceptance fails.

Fresh Home audit also established that CT300's own traffic uses MikroTik `192.168.1.1`, while NetBird Internet-exit traffic is policy-routed through VRRP VIP `192.168.1.254`. This preserves the existing User Devices Internet-via-Home behavior without assigning that capability to `edge`.

### Remaining Stage 02.5 research

Stage 02.5 still must research and disposition:

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

## Stage 3 — Edge Cross-site Connectivity Foundation

### Planned work branch

`03 — Edge Cross-site Connectivity Foundation`

### Scope

Deploy and accept the selected bidirectional NetBird private fabric before any connectivity-dependent application stage.

Planned requirements:

- host-native NetBird peer on `edge`;
- dedicated Cloud Infrastructure service-peer grouping/policy;
- `edge -> Home/PAI` through existing `Home LAN 192.168.1.0/24` resource;
- no `0.0.0.0/0` Home Internet resource for `edge`;
- preserve direct provider Internet/default route on `edge`;
- Home/PAI -> `edge` through `100.105.0.0/16` gateway-level routing via CT300;
- corresponding narrow VM100 forwarding allowance and MikroTik/VM100 route persistence;
- reuse/verify NetBird-managed Site-to-VPN masquerade rather than add duplicate NAT by assumption;
- reuse `.lan` split-DNS and add `edge.lan` through the existing Home DNS mechanism;
- verify private reachability to `ai-node`, PVE and selected Home targets;
- verify direct/relay behavior on the real path;
- verify reboot persistence and non-regression of public `edge` services;
- perform controlled VRRP failover acceptance when the stage recovery plan permits it.

Stage 3 establishes transport/routing/private naming only. It does not own the vLLM service bind/provider configuration; that consumer-specific work belongs to Stage 4 Hermes.

## Stage 4 — Edge Hermes Agent Runtime

### Planned work branch

`04 — Edge Hermes Agent Runtime`

### Scope

Deploy Hermes after Stage 3 connectivity is accepted so Hermes can be completed in one stage rather than leaving the local-vLLM branch deferred.

Planned requirements:

- host-native runtime under `core` by default;
- persistent upstream-supported service lifecycle/state;
- no new public WebUI/port/domain by assumption;
- direct Hermes access to Codex and Antigravity executors without routing through CloudCLI;
- stable machine interface by which n8n can invoke Hermes and receive task result/status;
- minimal non-user-specific acceptance of `n8n -> Hermes -> Codex/AGY -> Hermes -> n8n`;
- inspect the current `ai-node` vLLM bind/exposure state and make only the minimum change needed to expose the selected OpenAI-compatible endpoint through the accepted private fabric;
- verify `Hermes -> vLLM` inference through the Stage 3 private path;
- no Capture Inbox, vendor watchers, bounded research jobs or other user-specific automations in Stage 4.

## Stage 5 — Edge Cross-site Data & Knowledge Services

### Planned work branch

`05 — Edge Cross-site Data & Knowledge Services`

### Scope

After Stage 3 connectivity and Stage 4 Hermes are accepted, deploy selected connectivity-dependent data services:

- VPS working-file access and web file management;
- MacBook/iPhone/iPad/`ai-node` access;
- selected-directory synchronization;
- Obsidian synchronization/relay/mirror role.

Canonical Obsidian remains `ai-node:/srv/ai-data/knowledge/obsidian`.

## Stage 6 — Edge Remaining Infrastructure Services

### Planned status

**CONDITIONAL.**

Use only if remaining Stage 02.5 research selects another full infrastructure service whose dependencies are satisfied after Stage 5 and which does not belong to backup/update/monitoring/portal layers. Do not create an empty branch merely to preserve numbering.

If this slot is empty at Stage 02.5 closure, remove it and normalize later numbering before Stage 3 opens.

## Stage 7 — Edge Backrest & Recovery

### Planned work branch

`07 — Edge Backrest & Recovery`

Deploy/configure Backrest + Restic against the substantially complete server. Define backup scope/exclusions, repository/off-site topology, retention/schedules, recovery procedures and verified restore acceptance.

A usable restore path is mandatory before Stage 8 update testing.

## Stage 8 — Edge Maintenance & Update

### Planned work branch

`08 — Edge Maintenance & Update`

Deploy Semaphore and the maintenance/update workflow after Backrest acceptance. Audit/adapt the existing PVE/Home updater; do not copy PVE-specific implementation blindly.

Dedicated Codex substage:

**Stage 8C — Codex: build `update.escloud.us`**

This begins only after the real Semaphore/update backend, status model and control contract are known. `update.escloud.us` remains separate from `app.escloud.us`.

## Stage 9 — Edge Monitoring, Heartbeats & Alerts

### Planned work branch

`09 — Edge Monitoring, Heartbeats & Alerts`

Deploy production monitoring against the substantially complete infrastructure, including as selected external availability, cross-site connectivity health, selected Home/PVE/`ai-node` heartbeats, file/sync health, Backrest health, Semaphore/update state and alert delivery.

Avoid a heavyweight metrics/logging platform unless research proves concrete value.

## Stage 10 — Edge Cloud Portal

### Planned work branch

`10 — Edge Cloud Portal`

Build `app.escloud.us` only after Stage 9 monitoring/status sources and the final service inventory are accepted.

Dedicated Codex substage:

**Stage 10C — Codex: build `app.escloud.us`**

The portal is navigation plus concise infrastructure/status presentation. It does not absorb detailed maintenance/update controls from `update.escloud.us`.

## Stage 11 — Edge Final Integrated Infrastructure Acceptance

### Planned work branch

`11 — Edge Final Integrated Infrastructure Acceptance`

Perform final server-wide acceptance only after all selected infrastructure services, cross-site connectivity/data integration, Backrest restore, Semaphore/update, monitoring/alerts, `app.escloud.us` and final cleanup are accepted.

Stage 11 closes the finite Cloud Infrastructure build.

---

## Post-infrastructure continuous workstream — Automation & User Workflows

This is deliberately **not** an infrastructure-completion stage. It begins only after Stage 11 and evolves continuously.

Examples include n8n workflows, Hermes/agent workflows, Universal Capture Inbox, human approvals, mail-triggered automation, continuous vendor/document intake, bounded AI research, durable application-level store-and-forward/retry, messaging/bot commands and user-specific orchestration among n8n, Hermes, Codex, Antigravity and local vLLM/PAI.

---

## Historical stage disposition

The earlier plan placing Hermes in Stage 3 and connectivity in Stage 4 is historical only and is superseded by the accepted 2026-09-17 connectivity decision.

The still older thematic Stage 3–7 plan is also historical only.

---

## Current canonical checkpoint

Stage 0: **COMPLETE / ACCEPTED**.  
Stage 1: **COMPLETE / ACCEPTED**.  
Stage 2: **COMPLETE / ACCEPTED**.  
Stage 02.5: **ACTIVE / RESEARCH-ONLY**.

Current branch:

`02.5 — Remaining Functional Scope Reconciliation & Research`

Cross-site Connectivity Foundation research is **COMPLETE / SELECTED**. The next Stage 02.5 research block is **Cross-site Data & Knowledge Services**. No Stage 3 production branch opens until all Stage 02.5 deliverables are accepted.