# Cloud Infrastructure — Architecture State

## Status

**Stage 0:** COMPLETE / ACCEPTED  
**Stage 1:** COMPLETE / ACCEPTED  
**Stage 2:** COMPLETE / ACCEPTED  
**Stage 02.5:** COMPLETE / ACCEPTED  
**Stage 3:** COMPLETE / ACCEPTED

`EDGE_STAGE2_FINAL_INTEGRATED_ACCEPTANCE=PASS`  
`CLOUD_STAGE_02_5_FINAL_SCOPE_ACCEPTANCE=PASS`  
`EDGE_STAGE3_FINAL_INTEGRATED_ACCEPTANCE=PASS`

Next production branch:

`04 — Edge Hermes Agent Runtime`

Final Stage 02.5 record:

`STAGE_02_5_FINAL_SCOPE_ACCEPTANCE_2026-09-18.md`

## Accepted architectural invariants

Unless superseded by a later ACCEPTED decision:

1. `edge` is the external 24/7 Cloud Infrastructure node and complements Home Infrastructure and Personal Agents Infrastructure rather than duplicating them.
2. `edge` remains independently useful without Home/PAI connectivity.
3. Home Infrastructure owns the future PVE canonical knowledge foundation. Cloud Infrastructure does not redesign or duplicate that authority.
4. Until Home explicitly accepts PVE canonical migration, the existing `ai-node:/srv/ai-data/knowledge/obsidian` remains factual current runtime state rather than the final architecture target.
5. After Home cutover, `edge` is an active synchronized RW knowledge replica/producer, not canonical authority.
6. Apple-device/Obsidian integration is outside Cloud Infrastructure and belongs to a separate late Home Infrastructure user-integration branch.
7. VPN/DPI-bypass functionality and the private infrastructure backbone are separate concerns.
8. Single-operator simplicity is preferred over enterprise-style complexity without demonstrated need.
9. Fresh verified runtime/configuration outranks historical reference.
10. User-specific n8n/agent workflows are an application layer above the finite infrastructure framework.
11. Presentation, backup, monitoring and maintenance tooling that depends on final inventory is deployed late rather than repeatedly reworked.

## Accepted Stage 1 platform architecture

### Host/runtime placement

- Ubuntu host provides SSH, nginx, Xray, Hysteria2, Certbot, UFW and systemd-native lifecycle where host-native placement is materially simpler.
- Docker + Compose are the default runtime for suitable application services.
- Authelia is containerized.
- Host-native Xray/Hysteria2/nginx remain accepted because they directly own/shared public ingress and preserve a simple proven operating model.

### Persistent layout

- `/opt/<service>` — runtime definitions/scripts;
- `/srv/<service>` — persistent application state;
- `/etc/<service>` — host-native configuration;
- `/var/www/<site>` — static web roots.

### Public ingress

Accepted public listeners:

- TCP/22 — SSH;
- TCP/80 — nginx;
- TCP/443 — Xray with nginx fallback;
- UDP/443 — Hysteria2;
- TCP/25 — SMTP;
- TCP/465 — SMTPS submission;
- TCP/993 — IMAPS.

Application HTTP backends normally bind loopback and are published through nginx rather than directly exposing Docker ports.

### TLS lifecycle

- Certbot/ACME webroot;
- webroot `/var/www/letsencrypt`;
- lineage `/etc/letsencrypt/live/escloud.us`;
- renewal through Certbot timer;
- deploy hooks synchronize/reload Xray, Hysteria2 and Stalwart consumers.

### Firewall

- UFW active/enabled;
- default deny incoming;
- default allow outgoing;
- default deny routed;
- IPv6 enabled;
- Docker firewall integration retained;
- application containers loopback-published by default.

## Accepted Stage 2 application architecture

Production anchors:

- Authelia;
- n8n;
- CloudCLI;
- Codex CLI;
- Antigravity CLI;
- Stalwart;
- Bulwark.

Do not reopen them without concrete incompatibility or changed requirement.

## Accepted Cloud AI role separation

- **n8n** — deterministic automation/orchestration;
- **Hermes** — persistent cloud-side agentic reasoning, tools, supervision and delegation;
- **CloudCLI** — manual/remote Cloud AI workspace;
- **Codex CLI** — OpenAI coding/agent executor;
- **Antigravity CLI / `agy`** — Google cloud-agent/coding executor;
- **OpenClaw** — Home/PAI local personal-agent role;
- **vLLM on `ai-node`** — local inference backend for Hermes after private connectivity exists.

Hermes invokes Codex/Antigravity directly; CloudCLI is not a proxy between them.

## Stage 4 private collaboration/control surface — Mattermost

Stage 4D research/design is **COMPLETE / ACCEPTED**.

Acceptance record:

`STAGE_04D_MATTERMOST_DESIGN_ACCEPTANCE_2026-09-18.md`

Accepted target architecture:

- **Mattermost Team Edition**;
- current official Mattermost Docker Compose pattern;
- separate Mattermost application and dedicated PostgreSQL containers;
- local persistent `/srv` state;
- existing Xray -> host nginx -> shared TLS ingress;
- public human endpoint `https://chat.escloud.us`;
- **no Authelia in front of Mattermost**; use Mattermost-native authentication for web/desktop/mobile clients;
- Mattermost application backend remains non-public;
- PostgreSQL remains private;
- free Mattermost Test Push Notification Service (TPNS) is accepted for official mobile clients;
- Mattermost Calls is explicitly out of current Stage 4 scope;
- no Preview all-in-one image, bundled Mattermost nginx, Kubernetes, HA, Elasticsearch/OpenSearch, MinIO/S3, custom push stack or custom mobile build without a later concrete requirement.

`chat.escloud.us` is therefore an explicit exception to the normal service-subdomain Authelia rule, analogous in principle to other native-client services that must retain their own protocol/authentication semantics.

Architectural role:

- Mattermost = private/self-hosted collaboration, command and notification surface;
- Hermes remains the persistent agent runtime/reasoning/delegation layer;
- n8n remains deterministic orchestration;
- Codex/Antigravity remain specialist executors;
- CloudCLI remains manual cloud-AI workspace;
- Stalwart remains the existing mail subsystem.

### Native-only Mattermost integration invariant

Cloud Infrastructure implements a direct Mattermost integration only when the relevant upstream provides a supported path.

Accepted/current directions:

- **Hermes ↔ Mattermost:** Hermes built-in Mattermost gateway over Mattermost REST API v4 + WebSocket; accepted end-to-end.
- **n8n → Mattermost:** official built-in n8n Mattermost node/credential path; provisioning/authentication is valid, final node E2E acceptance remains pending.
- **Mattermost → Stalwart SMTP:** explicitly reviewed and **not required / not enabled** in the accepted target state.

For any other service or direction, verify current upstream support first. Do not substitute a custom plugin, patched source, shim service, direct database coupling, bespoke bridge, compatibility hack or n8n-mediated relay solely to connect otherwise unrelated products.

The enabled prepackaged Mattermost Agents plugin is not part of the accepted agent architecture and does not supersede Hermes; its runtime presence requires explicit disposition before final Stage 4 acceptance.

Detailed research: `STAGE_04_MATTERMOST_RESEARCH_BRIEF_2026-09-18.md`.

`STAGE4D_MATTERMOST_TARGET_ARCHITECTURE_ACCEPTANCE=PASS`

# Accepted Cross-site Connectivity Architecture

Selection record:

`STAGE_02_5_CONNECTIVITY_SELECTION_ACCEPTANCE_2026-09-17.md`

Final implementation acceptance:

`STAGE_03_ACCEPTANCE_2026-09-18.md`

## Technology choice

Reuse existing self-hosted Home NetBird as the bidirectional routed private fabric for Cloud ↔ Home/PAI.

Do not create a second parallel WireGuard/Tailscale backbone without demonstrated failure of the accepted design.

## Audited Home baseline

- Home LAN `192.168.1.0/24`;
- CT300 `remote-access` `192.168.1.90`;
- NetBird routing peer `100.105.97.126/16`;
- NetBird account overlay `100.105.0.0/16`;
- Home resources `192.168.1.0/24` and `0.0.0.0/0`;
- `.lan` split DNS through `192.168.1.1:53`;
- CT300 own default gateway via MikroTik `192.168.1.1`;
- NetBird ingress policy table default via VRRP VIP `192.168.1.254`.

## Private routed fabric

```text
                         NetBird private fabric
                            100.105.0.0/16
                                   |
                 +-----------------+-----------------+
                 |                                   |
               edge                                CT300
         ordinary service peer               existing routing peer
                 |                             192.168.1.90
                 |                                   |
                 |                           Home LAN 192.168.1.0/24
                 |                           /        |        \
                 |                         PVE     ai-node    CT220...
                 |
         direct VPS Internet
         remains provider-local
```

This is routed L3 connectivity, not an L2 bridge.

### `edge -> Home/PAI`

`edge` receives Home LAN reachability through CT300 but does **not** receive the Home Internet `0.0.0.0/0` resource. Public/default Internet stays provider-local.

### `Home/PAI -> edge`

The baseline architecture does **not** inject the NetBird overlay into the whole Home LAN.

For current workloads, Home/PAI consumers reach Cloud services through the existing VPS public IP or `escloud.us` / service-subdomain ingress. Hosts that are themselves NetBird peers may use normal peer-to-peer NetBird reachability.

Do not add `100.105.0.0/16 via 192.168.1.90` to VM100/MikroTik and do not alter VM100 forwarding merely to provide hypothetical LAN-wide private access. Clientless gateway routing is an on-demand extension only when a concrete private-only workload proves that public ingress and a peer on the specific initiating host are both inferior.

## Private DNS

Reuse Home `.lan` split DNS only for `edge` resolving Home services:

- `*.lan` from `edge` → Home DNS through the accepted NetBird split-DNS policy;
- general Internet DNS stays VPS-local;
- do not create `edge.lan`: Cloud services already have the accepted public VPS IP and `escloud.us` / service-subdomain namespace, and ordinary Home LAN hosts are not routed into the NetBird overlay by default.

## Accepted Stage 3 runtime

- NetBird `0.78.2` runs host-native on `edge`;
- `edge` overlay IPv4 is `100.105.178.187/16`;
- CT300 overlay IPv4 is `100.105.97.126/16`;
- `192.168.1.0/24 dev wt0` and Home `.lan` split DNS persist across reboot;
- direct CT300 <-> `edge` P2P over UDP/51820 is verified;
- synchronized final reboot recovery reached working P2P approximately `13.187s` after actual edge boot;
- sustained post-recovery traffic passed with 0% loss;
- public `ens3` is IPv4-only; IPv6 remains available for link-local/NetBird overlay use;
- Docker `live-restore=false` is the separately accepted current platform state after correction of the Stage 1 reboot-lifecycle regression.

## Transport fallback

Reuse existing NetBird management/signal/relay plane including TCP/443 relay fallback. Stage 3 must observe real direct/relay behavior rather than assume it.

AmneziaWG remains contingency only if real Stage 3 deployment acceptance exposes an unresolved transport/DPI problem.

# Cross-project Knowledge Architecture Boundary

## Ownership

The target architecture is deliberately split across projects:

```text
                         Home Infrastructure
                               PVE 24/7
                       canonical knowledge hub
                               /       \
                              /         \
                             v           v
                 PAI / ai-node          Cloud / edge
                 active RW replica      active RW replica
                 local AI producer      24/7 cloud producer
```

### Home Infrastructure owns

- PVE canonical storage layout/filesystem;
- PVE-side synchronization service and peer model;
- Home consumers/file-access integration;
- Home-side Backrest/Restic knowledge protection;
- availability/restore semantics of the canonical copy.

### Personal Agents Infrastructure owns

- `ai-node` local active RW replica after Home cutover;
- local paths and permissions;
- n8n/OpenClaw/vLLM/OCR/RAG consumers and producers.

### Cloud Infrastructure owns

- `edge` local active RW replica;
- Cloud-side persistent storage/path;
- n8n/Hermes/cloud-AI read/write integration;
- PVE ↔ `edge` synchronization extension over the accepted private fabric.

Cloud must not establish an independent competing canonical knowledge service.

## Stage 5 expanded audit gate

Stage 5 must start with fresh read-only inspection of all three relevant states before mutation.

Audit must prove at least:

- Home PVE canonical migration is actually ACCEPTED;
- exact PVE canonical path/filesystem/backing storage and capacity/health;
- current ownership/permissions/export/mount semantics;
- Home-selected synchronization mechanism/version/runtime/peer model;
- conflict/versioning and accepted outage/reconnect semantics;
- actual PVE ↔ `ai-node` synchronization health;
- CT206 relevance if retained;
- CT208/Backrest canonical-knowledge backup and restore state;
- `ai-node` replica path, sync health and producer/consumer permissions;
- Stage 3 NetBird route/DNS non-regression;
- Stage 4 Hermes/vLLM non-regression;
- `edge` storage and actual RW/RO consumer requirements.

If Home PVE canonical migration is not accepted, Stage 5 stops before mutation and reconciles that prerequisite instead of inventing a parallel architecture.

The Home-accepted server-side sync mechanism is reused by default. A second primary engine for the same knowledge tree requires concrete incompatibility plus explicit superseding acceptance.

MacBook/iPhone/iPad sync mechanisms are intentionally absent from this architecture.

# Final dependency-aware remaining architecture

## Stage 3 — Cross-site Connectivity Foundation

**COMPLETE / ACCEPTED.** `EDGE_STAGE3_FINAL_INTEGRATED_ACCEPTANCE=PASS`.

The accepted baseline path is `edge -> Home/PAI`; VM100/MikroTik remain unchanged for hypothetical LAN-wide Home -> `edge` access. Public Cloud ingress remains the normal reverse-direction path. Stage 3 does not own vLLM service/provider configuration beyond reachability.

## Stage 4 — Hermes Agent Runtime

Preferred Hermes placement: host-native under `core`.

Stage 4 architecture combines:

- Hermes core runtime using private `ai-node` vLLM;
- direct Codex CLI and Antigravity CLI executors;
- authenticated Hermes Web Dashboard at `https://hermes.escloud.us`;
- private authenticated n8n machine interface;
- Mattermost at `https://chat.escloud.us` as the private collaboration/control/notification surface;
- final macOS Hermes Desktop Remote Gateway integration.

Hermes Dashboard ingress:

- public TCP/443 -> Xray/nginx -> Authelia -> loopback Hermes backend;
- backend remains non-public;
- use the self-hosted Remote Gateway/session-token path first for Hermes Desktop;
- add another Hermes-native credential mode only if the installed runtime proves the simple path incompatible.

Mattermost ingress/auth is intentionally different:

- public TCP/443 -> Xray/nginx -> loopback Mattermost backend;
- Mattermost-native authentication;
- no Authelia in front of `chat.escloud.us`;
- PostgreSQL remains private;
- Calls remains excluded.

Stage 4 acceptance requires:

- real Hermes -> vLLM inference;
- practical selected Hermes tool surfaces;
- direct Hermes -> Codex and Hermes -> Antigravity delegation;
- Hermes Dashboard through nginx + Authelia;
- accepted native Hermes↔Mattermost and n8n↔Mattermost paths;
- private authenticated n8n -> Hermes machine interface;
- `n8n -> Hermes -> Codex/AGY -> Hermes -> n8n`;
- clean Hermes gateway lifecycle, including controlled stop/restart and reboot persistence;
- no unintended public Hermes machine/API listener;
- server-side integrated non-regression;
- final macOS Hermes Desktop readiness/live chat/WebSocket/reconnect acceptance.

User-specific automation workflows remain outside infrastructure acceptance.

## Stage 5 — Edge Knowledge Replication & Data Integration

Integration stage against the accepted Home/PAI knowledge contract.

Sequence:

1. expanded cross-project read-only audit;
2. reuse Home sync mechanism by default;
3. add `edge` active RW replica/producer;
4. expose minimum local paths to n8n/Hermes/tools;
5. verify bidirectional propagation, conflict behavior, peer outage/reconciliation and reboot persistence;
6. verify Home/PAI/Cloud non-regression.

Apple-device integration is out of scope.

## Stage 6 — Backrest & Recovery

Backrest using Restic remains the accepted Cloud backup-management direction. Restore acceptance precedes update testing.

## Stage 7 — Maintenance & Update

Semaphore is the accepted operational execution product. `update.escloud.us` is a separate UI built in a dedicated Codex substage after the real backend contract exists.

## Stage 8 — Monitoring, Heartbeats & Alerts

Production monitoring is intentionally late-stage so it covers actual stable inventory/connectivity/backup/update layers.

## Stage 9 — `app.escloud.us` Cloud Portal

Build after monitoring/status sources and final service inventory are accepted. It provides navigation and concise status, not detailed update controls.

## Stage 10 — Final Integrated Infrastructure Acceptance

Final server-wide acceptance occurs only after selected infrastructure services, cross-site data integration, backup/restore, update/maintenance, monitoring, portal and cleanup are accepted.

## Post-infrastructure automation/workflow layer

User-specific automation begins after Stage 10 and evolves continuously: Capture Inbox, approvals, mail-triggered workflows, vendor/document intake, bounded AI research, durable cross-site task handoff, messaging/bot surfaces and orchestration across n8n, Hermes, Codex, Antigravity and local vLLM/PAI.

Apple-device/Obsidian integration belongs to Home Infrastructure, not this Cloud workstream.

## Accepted global product anchors

Do not replace without concrete incompatibility or changed requirement:

- Xray;
- Hysteria2;
- nginx;
- n8n;
- CloudCLI;
- Stalwart + Bulwark;
- Authelia;
- Codex CLI;
- Antigravity CLI;
- Hermes Agent;
- existing self-hosted NetBird.

Additional accepted directions:

- Hermes host-native under `core` by default;
- Backrest using Restic;
- Semaphore;
- dedicated `update.escloud.us` maintenance/update page;
- late infrastructure-wide monitoring;
- dedicated `app.escloud.us` portal after monitoring/status sources.

## Architecture authority

1. current user instruction;
2. latest applicable ACCEPTED decision/acceptance record;
3. `CURRENT_STATE.md` for confirmed runtime;
4. this file for accepted architecture/invariants;
5. `IMPLEMENTATION_PHASES.md` and stage-specific records;
6. `FUNCTIONAL_SCAFFOLD_DRAFT.md` for capability intent;
7. `migration-reference/` and historical baseline for legacy evidence only.
