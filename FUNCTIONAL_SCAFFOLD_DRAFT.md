# Cloud Infrastructure — Functional Scaffold

**Status:** capability scaffold reconciled with accepted Stage 3/4 and Home Knowledge records on 2026-09-19.

This document preserves functional requirements for `edge`. It is not an independent chronology source; implementation order is defined by `IMPLEMENTATION_PHASES.md`.

## Design rule

Cloud Infrastructure should complement Home Infrastructure and Personal Agents Infrastructure by using capabilities that materially benefit from an external 24/7 VPS: foreign Internet location, stable public reachability, external failure domain, continuous Internet observation, public event reception and cloud/subscription-agent execution.

Do not duplicate Home/PAI capabilities merely because they can also run on a VPS.

## Final sequencing

1. Stage 3 — Cross-site Connectivity Foundation;
2. Stage 4 — Hermes Agent Runtime;
3. Stage 5 — Knowledge Replication & Data Integration;
4. Stage 6 — Backrest & Recovery;
5. Stage 7 — Maintenance & Update;
6. Stage 8 — Monitoring, Heartbeats & Alerts;
7. Stage 9 — Cloud Portal;
8. Stage 10 — Final Integrated Infrastructure Acceptance;
9. post-infrastructure Automation & User Workflows.

Apple-device/Obsidian integration is not part of the Cloud sequence; it belongs to Home Infrastructure as a later user-integration project.

---

## 1. Public edge and universal service access

### Accepted base

- Xray
- Hysteria2
- nginx
- Authelia
- Stalwart + Bulwark

### Functional intent

- DPI-resistant foreign Internet egress;
- public HTTP/HTTPS ingress for services that require it;
- managed TLS;
- human WebUI, native protocol and machine/API access where appropriate;
- Authelia web login where application semantics support it;
- public plausible/decoy page;
- private Cloud Infrastructure portal/status page replacing legacy Homepage.

Base ingress/TLS/auth/decoy implementation is already deployed and accepted in Stage 1/2.

---

## 2. Always-on automation, Internet event ingress and user interaction

### Accepted base

- n8n is the deterministic automation/orchestration plane.

### Functional intent

- public webhooks;
- schedules;
- Internet/SaaS events;
- RSS/feed triggers;
- website/document-change workflows;
- mail/event automation;
- orchestration across Cloud, Home and PAI;
- notifications and results.

### Later user/workflow capabilities

- Universal Capture Inbox;
- human-in-the-loop approvals;
- mail as automation transport;
- durable application-level store-and-forward/retry;
- messaging/bot commands.

These do not delay finite infrastructure completion unless a concrete dedicated infrastructure dependency later appears.

Do not add another generic scheduler beside n8n without a concrete requirement.

---

## 3. External monitoring, heartbeats and notifications

### Disposition

**DEFERRED TO STAGE 8.**

Research/final selection occurs against the substantially complete real infrastructure rather than during Stage 02.5.

Functional scope may include:

- external availability checks;
- dead-man/heartbeat monitoring from Home/PVE/PAI;
- cross-site connectivity health;
- knowledge-sync health;
- backup/job-health signals;
- important alert delivery;
- status presentation on the Cloud portal.

Do not assume Prometheus/Grafana/Netdata-class complexity without concrete need. `ntfy` remains a possible alert/push mechanism if Stage 8 proves push useful; Gotify is not preferred.

---

## 4. Backup operations and off-site recovery role

### Accepted base

- Backrest is the accepted backup management/orchestration direction;
- Restic is the accepted underlying engine family.

### Placement

**Stage 6 — Edge Backrest & Recovery.**

Functional intent:

- protect `edge` application/configuration state;
- maintain verified restore capability;
- decide repository/off-site topology against the final service/data inventory;
- avoid treating same-VPS storage as complete disaster recovery.

Exact repositories, retention and schedules are Stage 6 implementation details, not Stage 02.5 blockers.

---

## 5. Knowledge replication and working data

### Cross-project ownership

The knowledge platform is not owned end-to-end by Cloud Infrastructure.

**Home Infrastructure** owns the accepted PVE 24/7 canonical knowledge foundation and server-side synchronization authority.

**Personal Agents Infrastructure** owns the `ai-node` active RW replica and local AI producers/consumers after Home cutover.

**Cloud Infrastructure** owns the `edge` active RW replica and Cloud-side n8n/Hermes/cloud-AI integration.

Home Infrastructure records `KNOWLEDGE_FABRIC_CANONICAL_CUTOVER=PASS` on 2026-09-18: PVE `/srv/knowledge/obsidian` is canonical and `ai-node:/srv/ai-data/knowledge/obsidian` is an active RW Syncthing replica. This is accepted cross-project evidence; a fresh Home/PAI runtime audit remains mandatory before Cloud Stage 5 deployment.

### Stage 5 placement

**Stage 5 — Edge Knowledge Replication & Data Integration.**

Stage 5 begins with an expanded read-only cross-project audit before any mutation.

The audit must establish:

- actual accepted PVE canonical path/filesystem/backing storage;
- capacity/filesystem health;
- ownership/permissions/export semantics;
- Home-selected sync mechanism/version/runtime/peer model;
- conflict/versioning and accepted outage/reconnect behavior;
- actual PVE ↔ `ai-node` synchronization health;
- CT206 relevance if retained;
- CT208/Backrest canonical-knowledge protection and restore status;
- `ai-node` replica path, sync health and producer/consumer permissions;
- Stage 3 NetBird route/DNS non-regression;
- Stage 4 Hermes/vLLM non-regression;
- `edge` storage/path and actual RW/RO consumers.

If the fresh Stage 5 audit cannot confirm the accepted PVE canonical runtime and healthy PVE ↔ `ai-node` synchronization, Stage 5 stops before mutation and reconciles the dependency.

### Implementation principle

- reuse the Home-accepted server-side synchronization mechanism by default;
- do not create a second primary synchronization engine for the same knowledge tree without concrete incompatibility and explicit superseding acceptance;
- `edge` should work from a local persistent replica rather than requiring every write to traverse a remote filesystem;
- verify bidirectional propagation, conflict behavior, peer outage/reconciliation and reboot persistence;
- expose only minimum local paths needed by n8n/Hermes/tools;
- working-file/web-file software such as Filestash or SFTPGo is **not preselected** and should be added only if Stage 5 audit proves a real Cloud-side requirement.

### Explicitly removed from Cloud scope

MacBook/iPhone/iPad Obsidian synchronization and product research for Self-hosted LiveSync/CouchDB, Remotely Save/WebDAV, iOS Syncthing clients or similar user-device mechanisms.

That entire problem is deferred to a separate late Home Infrastructure user-integration branch.

---

## 6. Continuous information intake and change detection

### Disposition

**POST-INFRASTRUCTURE WORKFLOW CAPABILITY.**

Use the 24/7 foreign Internet presence of `edge` to monitor vendor documentation, releases, websites, feeds, email/webhooks/APIs and user-submitted material.

Preferred first implementation is n8n + Hermes + existing protocols/tools. A dedicated change-detection/feed product is installed only if a real workflow proves n8n insufficient.

Example:

`edge` detects a new OEM document → n8n queues it → Hermes and/or PAI processing is invoked → local/cloud AI is selected as appropriate → result is written to the `edge` knowledge replica → server-side sync propagates it to PVE canonical knowledge.

---

## 7. Cloud AI workspace and persistent agents

### Accepted base

- CloudCLI
- Codex CLI
- Antigravity CLI
- Hermes Agent
- n8n
- OpenClaw in Home/PAI
- vLLM on `ai-node`

### Role separation

**CloudCLI** — manual Cloud AI workspace.  
**Codex CLI** — specialized OpenAI coding/agent executor.  
**Antigravity CLI / `agy`** — specialized Google cloud-agent/coding executor.  
**Hermes** — persistent cloud-side agentic reasoning/tool/supervision layer.  
**n8n** — deterministic workflow orchestrator.  
**OpenClaw** — Home/PAI local agent.  
**vLLM** — local inference backend available to Hermes after private connectivity and minimal exposure are accepted.

Stage 4 verifies both cloud-executor and real `Hermes -> vLLM` paths. User-specific agent tasks remain post-infrastructure workflows.

---

## 8. Bounded AI web research and intelligence jobs

### Disposition

**POST-INFRASTRUCTURE WORKFLOW CAPABILITY.**

Examples:

- analyze release changes;
- summarize vendor documentation updates;
- collect bounded community reports;
- prepare structured research reports for knowledge;
- periodically research narrowly defined topics;
- request human approval before consequential follow-up.

No standalone SearXNG/Karakeep/research stack is selected by assumption.

---

## 9. Cloud ↔ Home/PAI private connectivity and durable handoff

### Accepted foundation

Existing self-hosted Home NetBird is **SELECTED / REUSE EXISTING**.

Detailed acceptance:

`STAGE_02_5_CONNECTIVITY_SELECTION_ACCEPTANCE_2026-09-17.md`

Accepted architecture:

- CT300 remains Home routing peer at `192.168.1.90`;
- NetBird account overlay `100.105.0.0/16`;
- Home LAN `192.168.1.0/24`;
- `edge` becomes ordinary host-native service peer;
- `edge` gets Home LAN reachability but not Home `0.0.0.0/0` Internet exit;
- Home/PAI clientless hosts use accepted public edge ingress; LAN-wide overlay routing via CT300 remains deferred until a concrete private-only workload requires it; VM100/MikroTik were unchanged in Stage 3;
- reuse `.lan` split DNS;
- reuse existing NetBird-managed masquerade before considering duplicate NAT;
- direct WireGuard/Tailscale rejected as duplicate backbones;
- AmneziaWG contingency only if real Stage 3 acceptance proves NetBird transport failure.

### Durable application-level handoff

Persisted retry/resume and safe re-delivery belong to real post-infrastructure workflows. This requirement does not imply a dedicated broker.

---

## 10. Lifecycle, monitoring and presentation

### Stage 6 — Backrest & Recovery

Deploy after main service/data integration and verify restore before update testing.

### Stage 7 — Semaphore + `update.escloud.us`

Semaphore is accepted for operational execution. `update.escloud.us` is a separate maintenance/update UI implemented after the real backend contract exists.

### Stage 8 — Monitoring, Heartbeats & Alerts

Research/finalize and deploy against the stable inventory.

### Stage 9 — `app.escloud.us`

Navigation plus concise infrastructure/status presentation after monitoring/status sources exist. Detailed maintenance controls remain on `update.escloud.us`.

### Stage 10 — Final integrated infrastructure acceptance

Finite Cloud infrastructure closes only after selected services, cross-site integration, restore, update/maintenance, monitoring, portal and cleanup are accepted.

---

## 11. Optional / later capabilities

### Password / 2FA vault

**DEFERRED / OPTIONAL.** Existing Apple/iCloud Passwords workflow remains sufficient absent a changed requirement. 2FAuth is rejected as a separate requirement.

### Messaging/bot interface

Mattermost and its native Hermes/n8n integrations are deployed and accepted in Stage 4. Additional user-specific bot commands and automation remain deferred to user workflows; they do not constitute another orchestration platform.

### Limited failover / secondary endpoint

**DEFERRED.** Consider only after the primary architecture is complete and a concrete failure requirement exists.

### Generic server-control UI

**REJECTED.** Do not add Portainer/Cockpit-class duplicate control planes without a concrete need.

---

## Explicitly outside current `edge` scope

- Apple-device/Obsidian synchronization;
- authoritative/recursive Home DNS replacement;
- full household cloud drive platform;
- calendar/contact DAV platform;
- Git hosting/mirroring;
- CI/CD/package/artifact registries;
- generic sandbox/staging infrastructure;
- standalone database without a consumer;
- separate generic scheduler beside n8n;
- standalone browser service;
- central MCP gateway;
- generic multi-provider AI API router;
- CGNAT bridge;
- standalone TURN/STUN;
- MQTT/IoT broker;
- VoIP/realtime communications;
- game/media/download/photo hosting;
- generic lab/learning use.

---

## Current usage rule

This scaffold is a requirements map, not an independent chronology source.

Stage 02.5 is **COMPLETE / ACCEPTED**.

`CLOUD_STAGE_02_5_FINAL_SCOPE_ACCEPTANCE=PASS`

Stages 3 and 4 are COMPLETE / ACCEPTED. Next finite infrastructure stage:

`05 — Edge Knowledge Replication & Data Integration`

Begin with the required cross-project read-only entry audit; this scaffold does not authorize deployment.
