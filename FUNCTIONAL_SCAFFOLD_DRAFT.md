# Cloud Infrastructure — Preliminary Functional Scaffold

**Status:** global capability scaffold retained as requirements input; post-Stage-2 sequencing is governed by the accepted Stage 02.5 dependency-aware roadmap.

This document describes broad functional directions for `edge`. It does not by itself define every final product, network topology, container layout, domain, storage path or deployment architecture.

Its purpose is to preserve functional requirements while Stage 02.5 normalizes which requirements are infrastructure services, which depend on cross-site connectivity, and which are later user/workflow capabilities.

## Design rule

Cloud Infrastructure should complement Home Infrastructure and PAI by exploiting capabilities that materially benefit from an external 24/7 VPS: foreign Internet location, stable public reachability, external failure domain, continuous Internet observation, public event reception and subscription/cloud-agent execution.

Do not duplicate Home/PAI capabilities merely because they can also run on a VPS.

## Current sequencing rule

The historical thematic Stage 3–7 grouping is no longer authoritative.

Current planned post-Stage-02.5 sequence:

1. Stage 3 — Cross-site Connectivity Foundation;
2. Stage 4 — Hermes Agent Runtime;
3. Stage 5 — Cross-site Data & Knowledge Services;
4. Stage 6 — conditional Remaining Infrastructure Services only if further research selects any;
5. Stage 7 — Backrest & Recovery;
6. Stage 8 — Semaphore + maintenance/update workflow + separate Codex `update.escloud.us` substage;
7. Stage 9 — infrastructure-wide Monitoring, Heartbeats & Alerts;
8. Stage 10 — final `app.escloud.us` Cloud Portal + separate Codex implementation substage;
9. Stage 11 — Final Integrated Infrastructure Acceptance;
10. post-infrastructure Automation & User Workflows as a continuous workstream.

If Stage 6 is empty at Stage 02.5 closure, remove it and normalize later numbering rather than creating an empty deployment branch.

Products already explicitly ACCEPTED in `DECISIONS.md` are anchors and should not be re-opened without a concrete incompatibility or changed requirement.

---

## 1. Public edge and universal service access

### Accepted base

- Xray
- Hysteria2
- nginx
- Authelia
- Stalwart + Bulwark

### Functional intent

- DPI-resistant foreign Internet egress for the user;
- public HTTP/HTTPS ingress for services that require it;
- managed HTTPS/TLS as part of ingress;
- convenient access from MacBook, iPhone, iPad, Windows and other authorized devices;
- separate human WebUI, native protocol and machine/API access where appropriate;
- unified web login through Authelia where application semantics support it;
- public plausible/decoy page for the VPN-facing endpoint;
- private Cloud Infrastructure portal/status page replacing legacy Homepage.

### Current state

Base ingress/TLS/auth/decoy implementation is already deployed and accepted in Stage 1/2. Future work is service-specific ingress only when a selected service requires it.

---

## 2. Always-on automation, Internet event ingress and user interaction

### Accepted base

- n8n is the common deterministic automation/orchestration plane.

### Functional intent

- public webhooks;
- scheduled automation;
- Internet/SaaS event handling;
- RSS/feed triggers;
- website-change workflows;
- mail/event-driven automation;
- orchestration of Cloud, Home and PAI workflows;
- notifications and result delivery.

### Universal Capture Inbox — универсальный приём материалов

Provide low-friction user-facing entry points for URLs, text/notes, files/PDFs, images and commands into automation/knowledge workflows.

### Human-in-the-loop approvals — ручное подтверждение действий

Selected n8n/agent workflows should be able to pause for explicit approve/reject/choice/confirmation through existing user interaction surfaces.

### Mail as automation transport — почта как транспорт автоматизаций

The accepted Stalwart + Bulwark stack may provide inbound mail/attachment triggers and outbound system notifications for n8n workflows.

### Placement

These are primarily **post-infrastructure user/workflow capabilities**. They do not delay infrastructure completion unless one later proves to require a dedicated infrastructure service.

Do not add another generic scheduler/job stack beside n8n without a concrete requirement.

---

## 3. External monitoring, heartbeats and notifications

### Functional intent

Use the independent external failure domain of `edge` to detect failures that cannot be reliably observed from inside Home Infrastructure.

Candidate scope:

- external availability checks;
- dead-man/heartbeat monitoring from Home/PVE/PAI;
- selected backup/job-health signals;
- important alert delivery;
- status presentation on the private Cloud portal.

### Placement

Research implementation during Stage 02.5, but deploy production monitoring in Stage 9 after the main service inventory, cross-site connectivity, Backrest and update subsystem substantially exist.

Do not assume full duplicate observability or centralized heavy log/metric replication unless a concrete requirement proves value.

---

## 4. Backup operations and off-site recovery role

### Accepted base

- Backrest is the accepted future backup management/orchestration direction;
- Restic remains acceptable as the underlying backup engine.

### Functional intent

- protect `edge` application/configuration state;
- maintain verified restore capability;
- evaluate geographically independent copies of selected Home/PAI data;
- avoid treating same-VPS storage as complete disaster recovery.

### Placement

Stage 7 after the primary infrastructure service inventory is substantially complete. Backrest restore acceptance must precede Stage 8 Semaphore/update testing.

### Still unresolved

- repository destinations;
- Home ↔ Cloud backup division;
- what Home/PAI data warrants off-site replication;
- whether external object storage should complement VPS-local storage;
- retention and restore policy.

---

## 5. Working storage, file access, synchronization and Obsidian

### Accepted functional requirements

- selected VPS working storage accessible from MacBook, iPhone/iPad and `ai-node`;
- web file browsing/upload/download/editing;
- same working data usable by n8n and cloud AI agents where useful;
- continuous synchronization of selected working directories where justified;
- free/self-hosted Obsidian synchronization without paid Obsidian Sync;
- canonical Obsidian vault remains on `ai-node` at `/srv/ai-data/knowledge/obsidian`.

### Dependency placement

Deploy in Stage 5 after Stage 3 private connectivity is deployed and accepted.

### Still unresolved

- Filestash or alternative file layer;
- network filesystem/access protocol;
- Syncthing or alternative synchronization mechanism;
- exact role of `edge` in Obsidian synchronization;
- concrete Obsidian synchronization product/mechanism;
- conflict/versioning semantics.

SFTPGo, Self-hosted LiveSync/CouchDB, Syncthing or another proposal is not accepted merely because it appeared in an earlier draft.

---

## 6. Continuous information intake and change detection

### Functional intent

Use the 24/7 foreign Internet presence of `edge` to continuously observe external information sources and initiate workflows when useful changes occur.

Candidate inputs:

- RSS/Atom feeds;
- vendor documentation pages;
- firmware/software release pages;
- support portals;
- selected websites;
- email/webhooks/API events;
- user-submitted material.

High-value example:

`edge` detects a new OEM document → n8n acquires/queues it → Hermes and/or PAI processing is invoked as appropriate → PAI performs local OCR/translation/knowledge work where required → result is stored in canonical knowledge and a notification is sent.

### Placement

Actual vendor/document watchers, content rules and workflow logic belong to the post-infrastructure automation/workflow layer. A dedicated change-detection/feed product is installed only if a concrete later requirement proves n8n/ordinary protocols insufficient.

---

## 7. Cloud AI workspace and persistent agents

### Accepted base

- CloudCLI
- Codex CLI
- Antigravity CLI
- Hermes Agent

### Accepted role separation

**CloudCLI — ручной Cloud AI workspace.** Provides the user's remote/manual cloud-AI working surface on `edge`.

**Codex CLI — специализированный OpenAI coding/agent executor.** Used directly by the user and delegatable by Hermes.

**Antigravity CLI / `agy` — специализированный Google cloud-agent/coding executor.** Used directly by the user and delegatable by Hermes.

**Hermes Agent — постоянный облачный агент на `edge`.** Performs agentic reasoning, tool use, supervisory logic and delegation in parallel with n8n.

**n8n — deterministic workflow orchestrator.** Handles triggers, schedules, APIs, data routing and explicit workflow state rather than replacing Hermes reasoning.

**OpenClaw in Home/PAI — локальный персональный агент.** Remains the Home/PAI-side agent centered on local resources and local inference.

**vLLM on `ai-node` — локальный inference backend.** Hermes uses it after Stage 3 private connectivity is accepted.

### Stage 4 placement

Hermes is the sole selected Remaining Standalone Core Service, but deployment is intentionally Stage 4 so the complete Hermes acceptance can include local vLLM from the start.

Preferred deployment is host-native under `core`. Docker is not preferred because Hermes must directly reuse the existing host-native Codex and Antigravity executors and their user/runtime context; containerizing it would add avoidable bridging.

Target infrastructure flow:

```text
Internet / schedule / mail / webhook
                |
               n8n
                |
                v
             Hermes
        agentic reasoning
          +-----+-----+
          |     |     |
          v     v     v
        Codex   AGY   vLLM
          |            ^
          v            |
       result      ai-node over
          |         Stage 3 fabric
          v
         n8n
```

Stage 4 verifies both the cloud-executor path and actual `Hermes -> vLLM` inference. Actual user-specific agent tasks remain post-infrastructure workflows.

---

## 8. Bounded AI web research and intelligence jobs

### Functional intent

Run scheduled or event-triggered narrow research tasks rather than an unconstrained autonomous crawler.

Examples:

- analyze release changes after a monitored project updates;
- summarize vendor documentation changes;
- collect current community reports about a detected firmware/software release;
- prepare a structured research report for Obsidian or notification;
- periodically research narrowly defined topics;
- pause for user approval before selected consequential follow-up actions.

### Placement

Post-infrastructure workflows using n8n + Hermes + Codex/Antigravity + PAI/local vLLM as appropriate. Do not install a separate metasearch/research service unless a concrete workflow later proves it necessary.

---

## 9. Cloud ↔ Home/PAI private connectivity and durable handoff

### Accepted infrastructure foundation

Existing self-hosted Home NetBird is **SELECTED / REUSE EXISTING** as the Stage 3 bidirectional routed private fabric.

Detailed acceptance:

`STAGE_02_5_CONNECTIVITY_SELECTION_ACCEPTANCE_2026-09-17.md`

Accepted architecture:

- CT300 `remote-access` remains the Home NetBird routing peer at `192.168.1.90`;
- NetBird account IPv4 overlay is `100.105.0.0/16`;
- Home LAN is `192.168.1.0/24`;
- `edge` becomes an ordinary host-native NetBird service peer;
- `edge` gets Home LAN reachability but does **not** get the existing Home `0.0.0.0/0` Internet resource;
- `edge` therefore keeps direct provider-local Internet egress;
- Home/PAI clientless hosts reach `edge` through gateway-level `100.105.0.0/16 via 192.168.1.90` routing on both VM100 and MikroTik;
- reuse/verify existing NetBird-managed Site-to-VPN masquerade instead of adding duplicate NAT by assumption;
- reuse existing `.lan` split DNS: `192.168.1.1:53` only for match domain `lan`;
- add `edge.lan` through the existing Home DNS mechanism after Stage 3 enrollment/routing acceptance;
- direct WireGuard and Tailscale are rejected as duplicate parallel backbones;
- AmneziaWG is contingency only if real NetBird deployment acceptance demonstrates an unresolved transport/DPI failure.

Fresh audit also established that the current remote-user Home Internet Exit is intentionally separate: CT300's own default gateway is MikroTik `192.168.1.1`, while NetBird traffic arriving through `wt0` uses a policy table whose default is VRRP VIP `192.168.1.254`, normally reaching VM100/Mihomo.

### Application-level durable store-and-forward — гарантированная отложенная доставка задач

Cross-site workflows should later survive temporary destination unavailability through persisted state, retry/resume, observable outcomes and safe re-delivery where required.

This requirement does not imply a dedicated message broker. It is a post-infrastructure workflow concern to implement when real cross-site jobs exist.

Connectivity foundation and application-level task durability are separate layers.

---

## 10. Late lifecycle, monitoring and presentation

### Stage 7 — Backrest & Recovery

Deploy after the main service inventory is substantially complete. Verify restore before update testing.

### Stage 8 — Semaphore + `update.escloud.us`

Semaphore is the accepted operational execution product. The dedicated maintenance/update page lives at `update.escloud.us`, not inside `app.escloud.us`.

`update.escloud.us` is built in a separate Codex substage only after the real update backend contract is known.

### Stage 9 — Monitoring, Heartbeats & Alerts

Deploy after the service inventory, cross-site connectivity, Backrest and update subsystem exist so production monitoring covers the finished infrastructure in one coherent stage.

### Stage 10 — `app.escloud.us`

Build after monitoring/status sources and final service inventory are known. The page provides navigation and concise status/summary information, while detailed update controls remain on `update.escloud.us`.

`app.escloud.us` is built in a separate Codex substage.

### Stage 11 — Final integrated infrastructure acceptance

Infrastructure is complete only after all selected services, cross-site integration, backup/restore, update/maintenance, monitoring, portal and cleanup are accepted.

---

## 11. Optional / later capabilities

### Password / 2FA vault

Potential future cross-platform/self-hosted credential service. Low priority while the existing Apple/iCloud Passwords workflow remains satisfactory.

### Messaging/bot interface

Telegram or another messaging surface may become a frontend for commands, notifications, approvals and status. Treat it as an interface to workflows, not another orchestration platform.

### Limited failover/secondary endpoint

Consider only after the primary Home/PAI/Cloud architecture is complete. Do not design a duplicate cloud copy of Home Infrastructure.

---

## Explicitly outside the current `edge` scope

- authoritative/recursive home DNS replacement;
- full personal cloud drive as the main household storage platform;
- calendar/contact DAV platform;
- Git hosting/mirroring;
- CI/CD and package/artifact registries;
- generic test/sandbox/staging infrastructure;
- standalone database service without a consumer;
- separate generic job scheduler beside n8n;
- standalone headless/interactive browser service;
- central MCP gateway;
- multi-provider AI API router while subscription tools are primary;
- CGNAT bridge;
- TURN/STUN;
- MQTT/IoT broker;
- VoIP/realtime communication stack;
- game/media/download/photo hosting;
- generic lab/learning use.

---

## Current usage rule

This scaffold is a **requirements map**, not an independent chronology source.

Current project work:

`02.5 — Remaining Functional Scope Reconciliation & Research`

Completed research blocks:

- Hermes Agent selection;
- Cross-site Connectivity Foundation selection.

Immediate next research block: **Cross-site Data & Knowledge Services — working files, web file access, selected-directory synchronization and free/self-hosted Obsidian synchronization/edge role**.