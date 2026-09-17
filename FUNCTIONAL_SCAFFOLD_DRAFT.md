# Cloud Infrastructure — Preliminary Functional Scaffold

**Status:** global capability scaffold retained as requirements input; post-Stage-2 sequencing superseded by the accepted Stage 02.5 dependency-aware roadmap.

This document intentionally describes broad functional directions for `edge`. It does not by itself define the final service/product inventory, network topology, container layout, domains, storage paths, private-backbone technology or final deployment architecture.

Its purpose is to preserve the functional requirements identified during architecture discovery while allowing Stage 02.5 to normalize which requirements are infrastructure services, which are cross-site dependencies, and which are later user/workflow capabilities.

## Design rule

Cloud Infrastructure should complement Home Infrastructure and PAI by exploiting capabilities that materially benefit from an external 24/7 VPS: foreign Internet location, stable public reachability, external failure domain, continuous Internet observation, public event reception and subscription/cloud-agent execution.

Do not duplicate Home/PAI capabilities merely because they can also run on a VPS.

## Current sequencing rule

The historical thematic Stage 3–7 grouping is no longer authoritative.

Post-Stage-2 deployment now follows dependency direction:

1. remaining standalone core services;
2. cross-site connectivity foundation;
3. cross-site data/knowledge services such as files/sync/Obsidian;
4. remaining infrastructure services;
5. Backrest/restore;
6. Semaphore + dedicated `update.escloud.us` maintenance/update page;
7. infrastructure-wide monitoring/heartbeats/alerts;
8. final `app.escloud.us` portal/dashboard;
9. final integrated infrastructure acceptance;
10. user-specific n8n/agent workflows as a separate post-infrastructure layer.

Products already explicitly ACCEPTED in `DECISIONS.md` are anchors and should not be re-opened for replacement search without a concrete incompatibility or changed requirement.

---

## 1. Public edge and universal service access

### Accepted base

- Xray
- Hysteria2
- nginx
- Authelia
- Stalwart + Bulwark

### Functional intent

- DPI-resistant foreign Internet egress for the user.
- Public HTTP/HTTPS ingress for services that require it.
- Managed HTTPS/TLS for web access as part of the ingress layer.
- Convenient access to Cloud Infrastructure services from MacBook, iPhone, iPad, Windows and other authorized devices.
- Separate human WebUI, native protocol and machine/API access where appropriate; not every service API must be publicly exposed.
- Unified web login through Authelia where the application supports external-auth trust correctly.
- Public plausible/decoy page for the VPN-facing domain/endpoint.
- Private Cloud Infrastructure portal/status page replacing legacy Homepage.

### Current state

The base ingress/TLS/auth/decoy implementation is already deployed and accepted in Stage 1/2. Future work in this area is limited to new service-specific ingress as those services are selected and deployed.

---

## 2. Always-on automation, Internet event ingress and user interaction

### Accepted base

- n8n is the common always-on automation plane.

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

Provide one or more low-friction user-facing entry points for URLs, text/notes, files/PDFs, images and commands into automation/knowledge workflows.

### Human-in-the-loop approvals — ручное подтверждение действий

Selected n8n/agent workflows should be able to pause for an explicit approve/reject/choice/confirmation through existing user interaction surfaces.

### Mail as automation transport — почта как транспорт автоматизаций

The accepted Stalwart + Bulwark stack may provide inbound mail/attachment triggers and outbound system notifications for n8n workflows.

### Placement

These are primarily **post-infrastructure user/workflow capabilities**, not reasons to delay completion of the infrastructure framework. Stage 02.5 should still research whether any of them genuinely requires a dedicated infrastructure service; otherwise they are implemented later using the accepted n8n/mail/agent stack.

Do not add a second generic cron/job automation stack merely because a task is simple; use n8n unless a concrete technical reason requires another execution mechanism.

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

Research the implementation during Stage 02.5, but deploy production monitoring **late**, after the main service inventory, cross-site connectivity, Backrest and update subsystem substantially exist. This avoids a second monitoring deployment simply to add services introduced later.

Do not assume full duplicate observability or centralized heavy log/metric replication unless a concrete requirement proves value.

---

## 4. Backup operations and off-site recovery role

### Accepted base

- Backrest is the accepted future backup management/orchestration direction;
- Restic remains acceptable as the underlying backup engine.

### Functional intent

- protect `edge` application/configuration state;
- maintain verified restore capability;
- evaluate whether `edge` or another external backend should hold selected geographically independent copies of critical Home/PAI data;
- avoid treating a repository on the same VPS filesystem as complete disaster recovery.

### Placement

Backrest is deployed only after the primary infrastructure service inventory is substantially complete, so backup scope, exclusions, retention, repositories and restore procedures are defined against the real system.

Backrest restore acceptance must precede Semaphore/update testing.

### Still unresolved

- repository destinations;
- Home ↔ Cloud backup division;
- what Home/PAI data actually deserves off-site replication;
- whether external object storage should complement VPS-local storage;
- retention and restore policy.

A separate dedicated bootstrap/DR subsystem is not currently justified; GitHub plus verified backup/recovery context should cover rebuild needs unless later evidence shows a gap.

---

## 5. Working storage, file access, synchronization and Obsidian

### Accepted functional requirements

- selected VPS working storage accessible from MacBook, iPhone/iPad and `ai-node`;
- web file browsing/upload/download/editing;
- the same working data usable by n8n and cloud AI agents where useful;
- continuous synchronization of selected working directories where justified;
- free/self-hosted Obsidian synchronization without paid Obsidian Sync;
- canonical Obsidian vault remains on `ai-node` at `/srv/ai-data/knowledge/obsidian`.

### Dependency placement

These services are deployed only **after** the required `edge ↔ ai-node ↔ PVE/Home` connectivity foundation is selected, deployed and accepted.

### Still unresolved

- Filestash or alternative file layer;
- network filesystem/access protocol;
- Syncthing or alternative synchronization mechanism;
- exact role of `edge` in Obsidian synchronization;
- concrete Obsidian synchronization product/mechanism;
- conflict/versioning semantics.

SFTPGo, Self-hosted LiveSync/CouchDB, Syncthing or any other proposal is not accepted merely because it appeared in a prior architecture draft.

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
- user-submitted material from the Universal Capture Inbox.

High-value example:

`edge` detects a new OEM technical document → n8n acquires/queues it → PAI performs OCR/translation/knowledge processing → result is stored in canonical knowledge and a notification is sent.

### Placement

The infrastructure stage should select/deploy only any dedicated full service that proves necessary. The actual vendor/document watchers, workflow logic and content-specific jobs belong to the post-infrastructure automation/workflow layer after cross-site connectivity and all required services exist.

Do not assume a separate scraping platform if n8n and ordinary HTTP/feed/mail mechanisms are sufficient.

---

## 7. Cloud AI workspace and long-running agents

### Accepted base

- CloudCLI
- Codex CLI
- Antigravity CLI

### Functional intent

- persistent foreign-IP cloud AI execution environment;
- access from user devices without tying work to one laptop;
- long-running coding/agent tasks;
- use of subscription-based cloud tooling rather than forcing all workloads through paid token APIs;
- controlled access to repositories and working files;
- ability to request human approval before selected agent actions when a workflow requires it.

### Hermes candidate

Hermes remains only a candidate for a persistent personal-agent/supervisor role on `edge`.

Stage 02.5 should select Hermes only if it closes a concrete infrastructure/runtime gap not already served by n8n + CloudCLI + Codex CLI + Antigravity CLI. Otherwise reject it as duplicate complexity.

Actual user-specific long-running agent tasks and orchestration workflows belong to the post-infrastructure application layer.

---

## 8. Bounded AI web research and intelligence jobs

### Functional intent

Run scheduled or event-triggered research tasks rather than an unconstrained autonomous crawler.

Examples:

- analyze release changes after a monitored project updates;
- summarize vendor documentation changes;
- collect current community reports about a detected firmware/software release;
- prepare a structured research report for Obsidian or notification;
- periodically research narrowly defined topics;
- pause for user approval before an expensive, disruptive or consequential follow-up action where appropriate.

### Placement

These are post-infrastructure workflows unless Stage 02.5 proves that a dedicated infrastructure service is required. Orchestration should preferentially reuse n8n plus the accepted Cloud AI anchors and PAI.

---

## 9. Cloud ↔ Home/PAI orchestration and durable handoff

### Infrastructure prerequisite: connectivity

Before any cross-site dependent service or workflow is deployed, establish the required connectivity among `edge`, `ai-node` and PVE/Home from actual flows.

The private transport is not preselected. NetBird/WireGuard, authenticated HTTPS over public endpoints, another tunnel or another simple mechanism must be compared against the real flows and operating conditions.

### Application-level durable store-and-forward — гарантированная отложенная доставка задач

Cross-site workflows should later be able to survive temporary destination unavailability through persisted state, retry/resume, observable outcomes and safe re-delivery where required.

This requirement does not imply a dedicated message broker. It is an application/workflow concern to be implemented when real cross-site jobs exist, using the simplest mechanism that satisfies their durability semantics.

Connectivity foundation and application-level task durability are therefore separate layers.

Existing Home Mihomo policy routing already covers Home-side foreign egress and should not be duplicated as a new Cloud capability.

---

## 10. Late lifecycle, monitoring and presentation

### Backrest & Recovery — резервное копирование и восстановление

Deploy after the main service inventory is substantially complete. Verify restore before update testing.

### Semaphore + `update.escloud.us` — обслуживание и обновления

Semaphore is the accepted operational execution product. The dedicated maintenance/update page lives at `update.escloud.us`, not inside `app.escloud.us`.

`update.escloud.us` is built in a separate Codex substage only after the real update backend contract is known.

### Monitoring, Heartbeats & Alerts — мониторинг, heartbeat и оповещения

Deploy after the service inventory, cross-site connectivity, Backrest and update subsystem exist so production monitoring can cover the finished infrastructure in one coherent stage.

### `app.escloud.us` — основной портал Cloud Infrastructure

Build after monitoring/status sources and the final service inventory are known. The page provides navigation and concise status/summary information, while detailed update controls remain on `update.escloud.us`.

`app.escloud.us` is built in a separate Codex substage.

### Final integrated infrastructure acceptance

Infrastructure is considered complete only after all selected services, cross-site integration, backup/restore, update/maintenance, monitoring, portal and cleanup are accepted.

---

## 11. Optional / later capabilities

These remain candidates but are not part of the current accepted product set:

### Password / 2FA vault — хранилище паролей и 2FA

Potential future cross-platform/self-hosted credential service. Keep low priority while the existing Apple/iCloud Passwords workflow remains satisfactory.

### Messaging/bot interface — интерфейс команд и уведомлений через мессенджер

Telegram or another messaging surface may become a convenient frontend for commands, notifications, approvals and status. Treat it primarily as an interface to workflows, not a separate orchestration platform.

### Limited failover/secondary endpoint — ограниченный резервный endpoint

May be considered only after the primary Home/PAI/Cloud architecture is complete. Do not design a duplicate cloud copy of Home Infrastructure.

---

## Explicitly outside the current `edge` scope

The following functions remain outside the current Cloud capability scaffold unless a new requirement appears:

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

This scaffold is now a **requirements map**, not a stage chronology.

Current project work is:

`02.5 — Remaining Functional Scope Reconciliation & Research`

The immediate next research block is **Remaining Standalone Core Services**: determine which additional full, independently deployable services are actually required before cross-site connectivity and late lifecycle stages, and select concrete packages only where a real capability gap exists.
