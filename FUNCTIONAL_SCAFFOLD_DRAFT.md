# Cloud Infrastructure — Preliminary Functional Scaffold

**Status:** working draft / capability composition accepted for further discussion

This document is intentionally **not** the final Architecture Contract and does not define network topology, container layout, domains, storage paths, private-backbone technology or migration method.

Its purpose is to capture the current functional directions for `edge` after screening common private-VPS use cases against the already developed Home Infrastructure and Personal Agents Infrastructure.

## Design rule

Cloud Infrastructure should complement Home Infrastructure and PAI by exploiting capabilities that materially benefit from an external 24/7 VPS: foreign Internet location, stable public reachability, external failure domain, continuous Internet observation, public event reception and subscription/cloud-agent execution.

Do not duplicate Home/PAI capabilities merely because they can also run on a VPS.

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

## 2. Always-on automation and Internet event ingress

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

---

## 4. Backup operations and off-site recovery role

### Accepted base

- future clean `edge` deployment uses Backrest as the backup management/orchestration layer;
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
- whether external object storage should complement or replace VPS-local backup storage.

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
- network filesystem protocol;
- Syncthing or alternative synchronization mechanism;
- exact role of `edge` in Obsidian synchronization;
- conflict/versioning semantics.

Detailed product research is deferred until the complete functional scaffold is accepted.

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
- email/webhooks/API events.

High-value example:

`edge` detects a new OEM technical document → n8n acquires/queues it → PAI performs OCR/translation/knowledge processing → result is stored in canonical knowledge and a notification is sent.

This capability absorbs the useful parts of generic continuous web/data collection; a separate data-scraping platform is not assumed.

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
- controlled access to repositories and working files.

### Candidate extension

Hermes is a strong candidate for a persistent personal-agent/supervisor role on `edge`, coordinating cloud subscription tools and, later, selected Home/PAI capabilities. Hermes placement and responsibilities are not yet accepted as final architecture.

---

## 8. Bounded AI web research and intelligence jobs

### Functional intent

Run scheduled or event-triggered research tasks rather than an unconstrained autonomous crawler.

Examples:

- analyze release changes after a monitored project updates;
- summarize vendor documentation changes;
- collect current community reports about a detected firmware/software release;
- prepare a structured research report for Obsidian or notification;
- periodically research narrowly defined topics.

Likely orchestration can involve n8n plus the accepted Cloud AI stack/Hermes candidate.

Do not assume an endlessly autonomous agent that decides its own research agenda.

---

## 9. Cloud ↔ Home/PAI orchestration

### Functional intent

Allow `edge` to coordinate tasks with Home Infrastructure and Personal Agents Infrastructure without duplicating their compute or storage roles.

Candidate flows:

- `edge` receives an Internet event and invokes a Home/PAI workflow;
- `edge` discovers a document and sends it to `ai-node` for OCR/translation;
- cloud agents use local vLLM when appropriate;
- `edge` receives job status/results and publishes notifications;
- working files/results move between cloud-agent workspaces and local PAI pipelines.

### Boundary

The private transport is **not yet selected**. NetBird/WireGuard, authenticated HTTPS over the existing home public IP, another tunnel, or another simple mechanism must be compared only after the required flows are known.

Existing Home Mihomo policy routing already covers Home-side foreign egress and should not be duplicated as a new Cloud capability.

---

## 10. Optional / later capabilities

These remain candidates but are not part of the core scaffold yet:

### Password / 2FA vault

Potential future cross-platform/self-hosted credential service. Keep low priority while the Apple/iCloud Passwords workflow remains satisfactory.

### Messaging/bot interface

Telegram or another messaging surface may become a convenient frontend to n8n/Hermes for commands, notifications and status. Treat it as an interface, not a separate orchestration platform.

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

## Next discovery rule

This scaffold is a starting point for sequential discussion, not a final architecture. Each block can still be refined, merged, split, deferred or rejected. Only after the functional composition is mature should the project start detailed product selection for unresolved domains, followed by topology and deployment architecture.