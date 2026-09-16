# Cloud Infrastructure — Preliminary Functional Scaffold

**Status:** working draft / global capability scaffold accepted as input for stage-by-stage design

This document is intentionally **not** the final Architecture Contract and does not define the complete service/product inventory, network topology, container layout, domains, storage paths, private-backbone technology or final deployment architecture.

Its purpose is to capture the broad functional directions for `edge` after screening common private-VPS use cases against the already developed Home Infrastructure and Personal Agents Infrastructure.

## Design rule

Cloud Infrastructure should complement Home Infrastructure and PAI by exploiting capabilities that materially benefit from an external 24/7 VPS: foreign Internet location, stable public reachability, external failure domain, continuous Internet observation, public event reception and subscription/cloud-agent execution.

Do not duplicate Home/PAI capabilities merely because they can also run on a VPS.

## Stage-selection rule

This scaffold defines primarily **what capabilities are wanted**, not **which final program implements every capability**.

Unresolved products/services are intentionally selected later, at the beginning of the implementation stage where they are actually needed:

1. review that stage's functional requirements from this scaffold;
2. research/discuss unresolved candidate services/mechanisms for that stage;
3. explicitly accept the stage composition;
4. define the stage-scoped architecture/deployment contract;
5. only then deploy.

Products already explicitly ACCEPTED in `DECISIONS.md` are anchors and should not be re-opened for replacement search without a concrete incompatibility or changed requirement. Their deployment/integration details may still remain unresolved until their implementation stage.

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

### Still unresolved

- exact domain layout;
- exact TLS/ACME mechanics;
- which interfaces are public, private or machine-only;
- final public decoy/masquerade implementation.

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

### Universal Capture Inbox

Provide one or more simple user-facing entry points that allow the user to submit material from any device into automation/knowledge workflows, for example:

- URL;
- text/note;
- file or PDF;
- image;
- message/command.

The functional goal is a low-friction `device → edge → n8n → target workflow` path. This does not imply a dedicated new service; implementation can reuse existing web, mail, messaging or file interfaces.

### Human-in-the-loop approvals

Automation and agent workflows should be able to pause for an explicit human decision where appropriate, for example:

- approve/reject a proposed action;
- choose between alternatives;
- confirm a potentially disruptive task;
- approve processing of a newly detected document/release;
- acknowledge or retry a failed operation.

Approvals should reuse existing notification/WebUI/messaging surfaces rather than create a separate orchestration platform.

### Mail as automation transport

The accepted Stalwart + Bulwark mail stack may also be used as a machine/user automation interface, for example:

- dedicated inbound addresses feeding n8n workflows;
- attachment/document ingestion;
- rule-driven classification and processing;
- outbound system notifications via the existing mail stack.

Mail remains both a user service and a useful event/transport channel.

### Boundary

Do not add a second generic cron/job automation stack merely because a particular task is simple; use n8n unless a concrete technical reason requires another execution mechanism.

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

### Boundary

Do not assume full duplicate observability. Centralized heavy log/metric replication to `edge` is currently considered unnecessary unless a later concrete requirement proves otherwise.

The concrete monitoring/notification products are intentionally selected during Stage 3, not by this scaffold.

---

## 4. Backup operations and off-site recovery role

### Accepted base

- future clean `edge` deployment uses Backrest as the backup management/orchestration direction;
- Restic remains acceptable as an underlying backup engine.

### Functional intent

- protect `edge` application/configuration state;
- maintain verified restore capability;
- evaluate whether `edge` or another external backend should hold selected geographically independent copies of critical Home/PAI data;
- avoid treating a repository on the same VPS filesystem as complete disaster recovery.

### Still unresolved

- repository destinations;
- Home ↔ Cloud backup division;
- what Home/PAI data actually deserves off-site replication;
- whether external object storage should complement or replace VPS-local backup storage;
- the exact Stage 1 basic-backup mechanism versus later full backup-management implementation.

A separate dedicated bootstrap/DR subsystem is not currently justified; GitHub plus verified backup should cover rebuild context unless later evidence shows a gap.

---

## 5. Working storage, file access, synchronization and Obsidian

### Accepted functional requirements

- selected VPS working storage accessible from MacBook, iPhone/iPad and `ai-node`;
- web file browsing/upload/download/editing;
- the same working data usable by n8n and cloud AI agents where useful;
- continuous synchronization of selected working directories where justified;
- free/self-hosted Obsidian synchronization without paid Obsidian Sync;
- canonical Obsidian vault remains on `ai-node` at `/srv/ai-data/knowledge/obsidian`.

### Still unresolved

- Filestash or alternative file layer;
- network filesystem/access protocol;
- Syncthing or alternative synchronization mechanism;
- exact role of `edge` in Obsidian synchronization;
- concrete Obsidian synchronization product/mechanism;
- conflict/versioning semantics.

These choices belong to Stage 4 requirements/product-selection work. SFTPGo, Self-hosted LiveSync/CouchDB, Syncthing or any other proposal is not accepted merely because it appeared in a prior architecture draft.

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

This capability absorbs the useful parts of generic continuous web/data collection; a separate data-scraping platform is not assumed.

Concrete implementation additions beyond already accepted anchors are selected in Stage 5.

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

### Candidate extension

Hermes remains a candidate for a persistent personal-agent/supervisor role on `edge`, coordinating cloud subscription tools and, later, selected Home/PAI capabilities. Hermes placement and responsibilities are not accepted and must be evaluated in the relevant stage.

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

Likely orchestration can involve n8n plus accepted Cloud AI anchors and any later accepted agent extension.

Do not assume an endlessly autonomous agent that decides its own research agenda.

---

## 9. Cloud ↔ Home/PAI orchestration and durable handoff

### Functional intent

Allow `edge` to coordinate tasks with Home Infrastructure and Personal Agents Infrastructure without duplicating their compute or storage roles.

Candidate flows:

- `edge` receives an Internet event and invokes a Home/PAI workflow;
- `edge` discovers a document and sends it to `ai-node` for OCR/translation;
- cloud agents use local vLLM when appropriate;
- `edge` receives job status/results and publishes notifications;
- working files/results move between cloud-agent workspaces and local PAI pipelines.

### Durable store-and-forward requirement

Cross-site workflows must not require `edge` and Home/PAI to be online simultaneously.

The functional contract should allow:

1. `edge` to accept/persist a task or event;
2. temporary Home/PAI unavailability without losing that task;
3. retry/resume when the destination becomes available;
4. observable success/failure state;
5. idempotent or otherwise safe re-delivery where the workflow requires it.

This requirement does **not** imply a dedicated message broker. The simplest implementation that satisfies durability and retry semantics should be preferred.

### Boundary

The private transport is **not selected**. NetBird/WireGuard, authenticated HTTPS over the existing home public IP, another tunnel or another simple mechanism must be compared in Stage 6 only after the required flows are known.

Existing Home Mihomo policy routing already covers Home-side foreign egress and should not be duplicated as a new Cloud capability.

---

## 10. Optional / later capabilities

These remain candidates but are not part of the core accepted product set:

### Password / 2FA vault

Potential future cross-platform/self-hosted credential service. Keep low priority while the Apple/iCloud Passwords workflow remains satisfactory.

### Messaging/bot interface

Telegram or another messaging surface may become a convenient frontend to n8n/a later agent runtime for commands, notifications, approvals and status. Treat it as an interface, not a separate orchestration platform.

### Limited failover/secondary endpoint

May be considered only after the primary Home/PAI/Cloud architecture is complete. Do not design a duplicate cloud copy of Home Infrastructure.

---

## Explicitly outside the current `edge` scope

The following functions are intentionally not part of the current Cloud capability scaffold unless a new requirement appears:

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

This scaffold is the **global requirements map** used as input to implementation stages.

It must not be converted into one giant pre-deployment product-selection exercise.

Current project work remains in Stage 1 / branch:

`01 — Edge Clean Rebuild & Base Platform Deployment`

The next activity is to take only the Stage 1-relevant requirements from this scaffold, discuss/select unresolved Stage 1 implementation choices, accept the Stage 1 composition/contract, and finish Base Platform deployment.

Only after Stage 1 acceptance does the project open `02 — Edge Core Applications`, which begins its own requirements/product-selection cycle.
