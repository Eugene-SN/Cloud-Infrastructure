# Cloud Infrastructure — Architecture State

## Status

**Stage 0:** COMPLETE / ACCEPTED  
**Stage 1:** COMPLETE / ACCEPTED  
**Stage 2:** COMPLETE / ACCEPTED  
**Stage 02.5:** COMPLETE / ACCEPTED  
**Stage 3:** COMPLETE / ACCEPTED  
**Stage 4:** COMPLETE / ACCEPTED  
**Stage 5:** COMPLETE / ACCEPTED  
**Stage 6:** COMPLETE / ACCEPTED  
**Stage 7:** COMPLETE / ACCEPTED  
**Stage 8:** COMPLETE / ACCEPTED  
**Stage 9:** COMPLETE / ACCEPTED  
**Stage 10:** COMPLETE / ACCEPTED  
**Stage 11:** COMPLETE / ACCEPTED  
**Stage 12:** COMPLETE / ACCEPTED  
**Stage 13:** COMPLETE / ACCEPTED

Key markers: `EDGE_STAGE3_FINAL_INTEGRATED_ACCEPTANCE=PASS`, `STAGE4_FINAL_ACCEPTANCE=PASS`, `STAGE05_FINAL_ACCEPTANCE=PASS`, `STAGE06_FINAL_ACCEPTANCE=PASS`, `STAGE07_FINAL_ACCEPTANCE=PASS`, `STAGE07_2_FINAL_MASTER_BATCH_EXECUTION=PASS`, `STAGE08_FINAL_ACCEPTANCE=PASS`, `STAGE09_FINAL_ACCEPTANCE=PASS`, `STAGE10_FINAL_ACCEPTANCE=PASS`, `STAGE11_FINAL_ACCEPTANCE=PASS`, `STAGE12_FINAL_ACCEPTANCE=PASS`, `STAGE13_FINAL_ACCEPTANCE=PASS`.

Current accepted checkpoint: `Stage 13 — Backrest WebUI Ingress — COMPLETE / ACCEPTED`.

Next finite focus: Post-infrastructure application/workflow layer.

## Accepted architectural invariants

Unless superseded by a later ACCEPTED decision:

1. `edge` is the external 24/7 Cloud Infrastructure node and complements Home Infrastructure and Personal Agents Infrastructure rather than duplicating them.
2. `edge` remains independently useful without Home/PAI connectivity.
3. Home Infrastructure owns the accepted PVE canonical knowledge foundation. Cloud Infrastructure does not redesign or duplicate that authority.
4. Home accepted canonical cutover on 2026-09-18: PVE `/srv/knowledge/obsidian` is canonical and `ai-node:/srv/ai-data/knowledge/obsidian` is an active RW Syncthing replica. Cloud Stage 5 must revalidate that accepted cross-project state before deployment.
5. After Home cutover, `edge` is an active synchronized RW knowledge replica/producer, not canonical authority.
6. PVE is the single full server-side Obsidian application/WebUI node (`obsidian.lan`); edge remains the accepted future Internet-reachable Knowledge client-access node for iOS/macOS/Windows/Android through a separately selected mechanism, while ai-node remains a replica/application-consumer node without server-side Obsidian runtime by default.
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

### Accepted Stage 4B executor trust and invocation model

- `edge` is a single-operator trusted host; Hermes and its specialist executors run under trusted Unix user `core`.
- Hermes remains the main Qwen3.8/vLLM orchestrator. Codex and Antigravity are direct specialist executors, not replacement main runtimes.
- Default Codex one-shot delegation is foreground, non-PTY `codex exec`; use background process management only for genuinely long/parallel work and PTY only for interactive TUI sessions.
- Default Antigravity one-shot delegation is foreground, non-PTY `agy -p/--print`, preferring structured JSON output supported by the installed CLI; use background/PTY only when the task requires those modes.
- Do not impose blanket executor sandboxing, container isolation, workspace-only filesystem restriction or network denial. Executors receive the host/workspace access needed for the delegated task.
- Critical destructive/system-wide/production/network/credential/data mutations are controlled by Hermes/orchestration instructions: obtain explicit operator approval before delegation unless the current instruction already explicitly authorizes that exact mutation.
- After approval, do not add a second artificial permission barrier that prevents the executor from completing the authorized task.
- Ordinary non-critical work proceeds without unnecessary approval prompts.
- Existing standalone Codex OAuth and Antigravity auth/state are reused; no duplicate Hermes-specific executor credentials are required.


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
- **n8n → Mattermost:** official built-in n8n Mattermost node/credential path; accepted end-to-end with an isolated throwaway-clone workflow and production non-regression.
- **Mattermost → Stalwart SMTP:** explicitly reviewed and **not required / not enabled** in the accepted target state.

For any other service or direction, verify current upstream support first. Do not substitute a custom plugin, patched source, shim service, direct database coupling, bespoke bridge, compatibility hack or n8n-mediated relay solely to connect otherwise unrelated products.

The prepackaged Mattermost Agents plugin is not part of the accepted agent architecture and does not supersede Hermes. It remains installed but is explicitly disabled in runtime; `STAGE4E_MATTERMOST_AGENTS_NORMALIZATION=PASS`.

Detailed research: `STAGE_04_MATTERMOST_RESEARCH_BRIEF_2026-09-18.md`.

`STAGE4D_MATTERMOST_TARGET_ARCHITECTURE_ACCEPTANCE=PASS`

Stage 4E implementation is **COMPLETE / ACCEPTED**. Final record: `STAGE_04E_FINAL_ACCEPTANCE_2026-09-18.md`; `STAGE4E_FINAL_ACCEPTANCE=PASS`.

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

Authoritative accepted record: `STAGE_05_1_FINAL_KNOWLEDGE_RUNTIME_ARCHITECTURE_ACCEPTANCE_2026-09-19.md`.

## Accepted topology

```text
PAI / ai-node                           Cloud / edge
active RW replica                      active RW replica
/srv/ai-data/knowledge/obsidian        /srv/knowledge/obsidian
        ^                                      ^
        | existing LAN Syncthing               | Syncthing over accepted
        |                                      | edge -> Home NetBird path
        +--------------- PVE ------------------+
                    canonical RW hub
                 /srv/knowledge/obsidian
```

PVE remains the canonical administrative/recovery authority and Syncthing hub. Canonical does not mean an online master required for local application operation: ai-node and edge stay locally usable while disconnected and reconcile when connectivity returns.

A direct edge ↔ ai-node Syncthing peer is intentionally not part of the target because current edge -> Home/PAI reachability itself depends on CT300 hosted on PVE.

### PVE — canonical Knowledge + full Obsidian application node

PVE owns:

- canonical RW vault `/srv/knowledge/obsidian`;
- PVE Syncthing hub;
- canonical Home backup/restore authority;
- CT220/OpenClaw canonical read-only Knowledge source;
- the single Ignis-based server-side Obsidian-aware application runtime.

Stage 05.2 deploys the Obsidian runtime in a new lightweight LXC. Accepted LXC envelope after the runtime packaging gate:

- 1 vCPU;
- 512 MiB RAM;
- 256 MiB LXC swap limit;
- 8 GiB rootfs;
- onboot enabled.

The canonical vault stays on the existing dedicated `pve/knowledge` 32 GiB ext4 LV and is bind-mounted RW into the LXC. The vault must not become dependent on the LXC rootfs.

The PVE Obsidian runtime provides:

- File Recovery;
- Obsidian index/metadata model;
- Ignis headless bridge (`ob` / Headless Sync) where applicable;
- core plugins and future explicitly selected plugins;
- private browser UI at `obsidian.lan`.

`obsidian.lan` is private to Home LAN and NetBird-routed Home clients; no public Internet Obsidian UI is part of Stage 5.

Runtime packaging inside the LXC is resolved: Ignis is the accepted implementation. Ignis runs the official Obsidian client code through its browser compatibility layer while keeping the vault as ordinary filesystem data. Native Electron parity is not a requirement unless a concrete workflow later needs it. The production update boundary is the Ignis image and its upstream-supported Obsidian version; do not independently advance Obsidian ahead of Ignis without a concrete compatibility reason.

Fresh PVE resource evidence from `PVE_OBSIDIAN_RESOURCE_READINESS_AUDIT=PASS`:

- Intel Core i3-N305, 8 cores;
- ~15 GiB RAM total, ~6.5 GiB available;
- 8 GiB host swap total, ~5.6 GiB free;
- low normal load.

The existing 8 GiB host swap is sufficient for the accepted LXC target. Do not increase PVE host swap without measured post-deployment pressure.

### ai-node — secondary PAI/application replica

ai-node owns:

- active RW non-canonical replica `/srv/ai-data/knowledge/obsidian`;
- current n8n RW consumption;
- future OCR/RAG/local-agent/AI consumers.

No server-side Obsidian runtime/WebUI is planned on ai-node by default after this decision. Stage 5 preserves ai-node application architecture and uses it for propagation/non-regression verification only.

OpenClaw keeps its current PVE canonical RO relationship. A direct ai-node Knowledge fallback remains optional future work.

### edge — secondary Cloud/agent + future external client-access node

Stage 05.3 target:

- active RW non-canonical replica `/srv/knowledge/obsidian`;
- `/srv/knowledge` = `core:core 0755`;
- `/srv/knowledge/obsidian` = `core:core 2775`;
- Syncthing under `core`;
- Hermes/Codex/Antigravity direct local path access;
- edge n8n RW bind at `/srv/knowledge/obsidian`;
- no Obsidian WebUI;
- no Obsidian runtime in Stage 5.

Future access role: edge is the preferred globally reachable Knowledge endpoint for iOS, macOS, Windows and Android client applications. Exact third-party application/protocol/access service remains unresolved and is not implemented in Stage 5. A future lightweight edge Obsidian runtime is conditional only if the selected client-access mechanism or an explicit edge-local File Recovery/API/index/plugin requirement needs a running Obsidian process. Syncthing must not be exposed publicly as the client-access interface.

## Recovery model

```text
Live data:
  PVE canonical + ai-node replica + edge replica

Short-term Obsidian-native recovery:
  PVE full Obsidian runtime / File Recovery

Primary durable Knowledge recovery:
  PVE canonical Backrest/Restic chain

Additional independent/off-site protection:
  handled by accepted/future backup stages where justified
```

File Recovery complements rather than replaces Restic. Live replicas are synchronization/availability copies, not backups.

## Failure semantics

- edge loss: PVE ↔ ai-node continues;
- ai-node loss: PVE ↔ edge continues;
- CT300/NetBird path loss: edge remains locally usable; PVE ↔ ai-node continues;
- PVE host loss: edge and ai-node remain locally usable but cannot synchronize with each other under the current topology;
- returning connectivity causes normal Syncthing reconciliation; simultaneous edits may create conflict copies.

## Stage 5 implementation structure

Stage 5 is COMPLETE / ACCEPTED:

- `05.1 — Cross-project Knowledge Reconciliation & Target Architecture` — COMPLETE / ACCEPTED;
- `05.2 — PVE Canonical Obsidian Runtime & WebUI` — COMPLETE / ACCEPTED;
- `05.3 — Edge Knowledge Replication & Data Integration` — COMPLETE / ACCEPTED.

Final topology is PVE ↔ ai-node plus PVE ↔ edge. edge is an active RW replica at `/srv/knowledge/obsidian`; no direct edge ↔ ai-node peer exists.

Accepted edge runtime:

- `/srv/knowledge` = `core:core 0755`;
- `/srv/knowledge/obsidian` = `core:core 2775`;
- Syncthing `2.1.5` under `core`, boot-persistent;
- edge initiates PVE connection to `tcp://192.168.1.3:22000`;
- local Syncthing listener/API remain loopback-only;
- Hermes/Codex/Antigravity use the local host path directly;
- n8n uses `/srv/knowledge/obsidian:/srv/knowledge/obsidian:rw`;
- no edge Obsidian runtime/WebUI and no public Syncthing exposure.

Propagation, outage/reconnect, conflict preservation and full edge reboot recovery all passed. Stage 4 runtime/network contracts remained intact.

Authoritative final record: `STAGE_05_3_FINAL_ACCEPTANCE_2026-09-20.md`.

# Final dependency-aware remaining architecture

## Stage 3 — Cross-site Connectivity Foundation

**COMPLETE / ACCEPTED.** `EDGE_STAGE3_FINAL_INTEGRATED_ACCEPTANCE=PASS`.

The accepted baseline path is `edge -> Home/PAI`; VM100/MikroTik remain unchanged for hypothetical LAN-wide Home -> `edge` access. Public Cloud ingress remains the normal reverse-direction path. Stage 3 does not own vLLM service/provider configuration beyond reachability.

## Stage 4 — Hermes Agent Runtime

**COMPLETE / ACCEPTED.** `STAGE4_FINAL_ACCEPTANCE=PASS`.

Accepted architecture:

```text
Browser / macOS Hermes Desktop
        |
        v
https://hermes.escloud.us
        |
Xray TLS -> nginx proxy_protocol
        |
127.0.0.1:9119 Hermes Dashboard
        |
Hermes native self-hosted OIDC
        |
https://auth.escloud.us (Authelia 4.39.27)

n8n container
        |
Bearer-authenticated HTTP Request
        |
172.19.0.1:8642 Hermes API Server
        |
Hermes -> qwen3.8-27b-fp8/vLLM
        |                 \
        |                  -> Codex CLI / Antigravity CLI
        v
structured result to n8n
```

Runtime roles:

- Hermes `0.21.3` at exact source commit `d177b119e9c56c9ddc0b7379ffce52341ec06584`, host-native under `core`;
- private `ai-node` vLLM at `http://192.168.1.30:8000/v1`, model `qwen3.8-27b-fp8`, is the main reasoning backend;
- Codex CLI and Antigravity CLI are trusted specialist executors invoked directly by Hermes;
- Mattermost at `https://chat.escloud.us` is the native collaboration/control surface;
- n8n remains the deterministic workflow plane and invokes Hermes through its native private API Server;
- Hermes Dashboard and macOS Desktop use the native self-hosted OIDC/RFC8252 PKCE contract.

Dashboard ingress/auth:

- public TCP/443 through existing Xray/nginx/shared `escloud.us` TLS;
- backend exclusively `127.0.0.1:9119`;
- exactly one provider, `self-hosted`, with Authelia as IdP;
- no nginx `auth_request`, no Basic/Nous fallback, no public 9119;
- browser callback `/auth/callback`, native Desktop authorize/token broker and WebSocket forwarding are accepted.

Private machine interface:

- upstream Hermes API Server binds `172.19.0.1:8642` only;
- n8n uses the explicitly named Docker network `n8n_hermes` with stable Linux bridge `n8n-hermes`, subnet `172.19.0.0/16` and gateway `172.19.0.1`;
- Bearer authentication is stored as an encrypted n8n credential;
- UFW permits only the n8n Docker subnet on `n8n-hermes`;
- no public nginx route or public 8642 listener;
- the production n8n subworkflow supports `vllm`, `codex` and `antigravity` selectors;
- native HTTP JSON avoids the known CLI `stream-json` Tirith stdout contamination.

Mattermost intentionally retains a different authentication contract:

- public TCP/443 -> Xray/nginx -> loopback Mattermost backend;
- Mattermost-native authentication, no Authelia;
- PostgreSQL remains private; Calls remains disabled;
- native Hermes and n8n integrations are accepted.

The controlled Hermes SIGTERM exit-status-1 behavior remains an accepted upstream lifecycle constraint. Requested restart/reboot recovery succeeds; no source patch or `SuccessExitStatus=1` masking is used.

User-specific automation workflows remain outside infrastructure acceptance.

## Stage 5 — Knowledge Fabric Runtime Deployment

**05.1 COMPLETE / ACCEPTED; 05.2 NEXT; 05.3 PLANNED.**

Authoritative record: `STAGE_05_1_FINAL_KNOWLEDGE_RUNTIME_ARCHITECTURE_ACCEPTANCE_2026-09-19.md`.

- `05.2 — PVE Canonical Obsidian Runtime & WebUI`: deploy the dedicated lightweight PVE LXC, bind the canonical vault, install the selected Ignis runtime, enable File Recovery and private `obsidian.lan`, and verify resource/reboot/non-regression behavior.
- `05.3 — Edge Knowledge Replication & Data Integration`: deploy the edge RW replica, integrate PVE↔edge Syncthing and edge consumers, then verify propagation/conflict/outage/reboot behavior and final Stage 5 acceptance.

External iOS/macOS/Windows/Android client-access implementation through edge remains future work and is not part of Stage 5.


## Stage 6 — Backrest & Recovery

Backrest using Restic remains the accepted Cloud backup-management direction. Restore acceptance precedes Stage 7 deployment/update testing so recovery capability is available if maintenance implementation or testing causes damage. This sequencing does not make Backrest a mandatory precondition of every routine production update; per-update backup behavior is component-specific and must be justified by the supported update/recovery path.

## Stage 7 — Maintenance & Update

Semaphore remains the accepted operational execution product. The implementation baseline is the already accepted Home Maintenance runtime on CT1000: preserve its proven Semaphore + Ansible/native-script separation, version/status collection and cache, fixed-target dispatch, component-specific update drivers, post-update refresh/acceptance flow, and dashboard contract wherever applicable.

Do not create an independent edge maintenance framework unless a concrete incompatibility is demonstrated. Port/adapt the live Home implementation, while replacing Home/PVE-specific inventory, VMID/PCT/QGA logic, target definitions, collectors and drivers with edge-specific equivalents. Home credentials and controller-specific state are not portable implementation content.

`update.escloud.us` starts from an adapted copy of the existing Home Maintenance dashboard source and status/action contract. Stage 7C refines that copied UI for Cloud/edge targets; it is not a greenfield frontend build. `update.escloud.us` remains separate from `app.escloud.us`.

Stage 7A is COMPLETE / ACCEPTED: the Home-derived framework is proven on edge in read-only mode, including the copied dashboard/status contract, Semaphore project/repository/inventory/environment/template model, canonical GitHub refresh playbook, local collector/cache refresh and full dashboard-triggered E2E. Stage 7B adds and accepts real edge component update drivers and Master Batch behavior; Stage 7A's read-only action boundary remains authoritative until each Stage 7B driver is explicitly accepted.

Stage 07.2 supersedes the Stage 7B blanket manual-only ownership rule with native-first ownership and a strictly manual Maintenance execution plane. `update.escloud.us` remains the operator surface for the 18 Maintenance-owned targets. Codex managed-daemon auto-update, Hermes native cron + settlement, and Ubuntu security updates through package-owned unattended-upgrades remain authoritative outside Maintenance; Codex and Hermes are absent from Maintenance collection, generated targets, actions, dashboard and Semaphore templates. The generated Maintenance model is `update_units_v5`; `actions.json` is manual-only with `auto_update=false`. Stage 8 consumes `maintenance.json` as authoritative update state. Semaphore has no autonomous schedules.

The accepted operator ingress is `https://update.escloud.us/` through the existing Xray -> host nginx -> Authelia chain. The dashboard backend remains private at `127.0.0.1:18070`; TCP/18070 is not a public listener or firewall opening. Redirects emitted by that loopback server must remain origin-relative, including the root redirect to `/status/`, so internal scheme/port details cannot leak through the reverse proxy.

The maintenance dashboard and full Semaphore UI share this origin, matching the accepted Home pattern. `/` redirects to `/status/`; `/status/` serves the maintenance dashboard; the dashboard's Semaphore button opens `/project/1/history`; Semaphore SPA routes and static assets are proxied to `127.0.0.1:3000`; `/api/` and `/api/ws` retain the Semaphore API and live-task WebSocket contract. Semaphore `web_host` is `https://update.escloud.us/`. The former `ops.escloud.us` candidate was fully retired from edge on 2026-09-21; its remaining Cloudflare DNS record is operator-owned cleanup.

## Stage 8 — Monitoring, Heartbeats & Alerts

**COMPLETE / ACCEPTED** with `STAGE08_FINAL_ACCEPTANCE=PASS`. Production monitoring covers the accepted stable inventory/connectivity/backup/update layers using the edge-only persistent-agent architecture documented below.

## Stage 9 — `app.escloud.us` Cloud Portal

**COMPLETE / ACCEPTED** with `STAGE09_FINAL_ACCEPTANCE=PASS`.

Production architecture: static files under `/var/www/app.escloud.us`, existing Xray -> nginx -> shared TLS ingress, ordinary Authelia `auth_request`, and a same-origin read-only `/api/status` view of the accepted Stage 8 `/run/edge-monitor/snapshot.json`. No portal backend service, container, database, SSE/WebSocket or second monitoring collector is used. The frontend presents concise current status plus explicit LIVE/STALE/UNAVAILABLE freshness and links only to real operator-facing services. Stage 7 update execution remains exclusively on `update.escloud.us`; the portal exposes no update mutation plane.

Architecture contract: `STAGE_09_ARCHITECTURE_ACCEPTANCE_2026-09-22.md`.

Final acceptance: `STAGE_09_FINAL_ACCEPTANCE_2026-09-22.md`.

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

## Accepted Stage 6 backup topology

Stage 6 general backup architecture is intentionally simple and is now fully specified by `STAGE_06_6_DEPLOYMENT_CONTRACT_2026-09-21.md`:

- one general plan `edge-state`; no separate broad system/data plans;
- sources: `/etc`, `/home/core`, `/root`, `/opt`, `/srv`, `/usr/local`, `/var/lib`, `/var/spool`, `/var/www`;
- schedule: `01:00/07:00/13:00/19:00` local;
- local edge repo = short rollback tier with all snapshots within `7d`, grouped by `host,tags`;
- successful snapshots are tier-copied to CT208/D5 through append-only rest-server before local retention is applied;
- CT208 owns D5 retention/prune: daily30, weekly8, monthly6, yearly0, grouped by `host,tags`;
- exclude the local backup repo, dedicated Knowledge, Docker/containerd layers and selected rebuildable caches; retain `/srv/backups`;
- live transactional application state is captured through a self-recovering consistency-staging wrapper; Mattermost uses a staged PostgreSQL dump and quiesced app state, mail uses a brief quiesced staged copy, and SQLite-backed services receive consistent snapshots;
- no recurring Restic full/bare-metal chain for the VPS;
- one provider-panel golden backup/snapshot is created manually only after final infrastructure acceptance;
- Knowledge remains the only independent backup chain: `/srv/knowledge`, schedule `04/10/16/22`, rolling local `14d`, no D5 replication.

The rejected rolling-180d D5 policy is not part of the architecture. Restore acceptance must exercise isolated application usability, not only repository integrity.


## Accepted Stage 8 monitoring architecture

Stage 8 uses a minimal edge-only monitoring runtime derived from the proven Home/PVE monitoring pattern, but without copying Home-specific receiver/UI complexity.

A single host-native persistent `edge-monitor.service` (`Type=simple`) is supervised by systemd. The Python agent uses separated cadences: FAST 5s for cheap local state and atomic snapshot publication, NORMAL 20s for concurrent application/container/network probes, SLOW 60s for semantic checks, and OPERATIONS 300s for backup/maintenance freshness checks. Ordinary endpoint failure is confirmed after two consecutive failed probes.

Live telemetry is published atomically to `/run/edge-monitor/snapshot.json`. Only durable transition/notification state is persisted under `/var/lib/edge-monitor/state.json`. Monitoring domains remain EDGE, APPLICATIONS, HOME_PAI, KNOWLEDGE and OPERATIONS. Alerts go directly to Mattermost only on meaningful transitions and recovery; unchanged failure states remain silent.

No Prometheus/Grafana/Loki/Gatus stack, monitoring database, separate receiver service, monitoring WebUI, external uptime service, independent vantage point or Home/PAI monitoring agent is part of the accepted current scope. PVE-specific D5/RAPL/EDAC/guest/gateway/SMART collectors and CT200 push/SSE presentation are not copied. Stage 7 update state is read as metadata rather than refreshed automatically by Stage 8. Backrest monitoring is based on authoritative successful-backup freshness. Full edge loss remains an accepted uncovered failure class in this edge-only design. The transition engine has final runtime acceptance: two consecutive failed probes confirmed FAIL, unchanged FAIL was deduplicated, recovery emitted one notification, and production returned to overall OK with no synthetic artifacts.


## Stage 12 — Nextcloud Cloud Drive & Private Workspace Access

Accepted architecture:

- `cloud.escloud.us` provides the personal cloud-drive UX through Nextcloud;
- Nextcloud runtime/state is isolated under `/srv/nextcloud`; portable user-visible files are under `/srv/cloud`;
- `go.escloud.us` provides direct project/workspace file access without changing Home routing;
- the WebDAV authority is exactly `/home/core/projects/`;
- rclone WebDAV runs as `core` on loopback `127.0.0.1:18081`;
- public WebDAV path is `go.escloud.us:443 -> Xray TLS -> nginx 127.0.0.1:8080 -> rclone 127.0.0.1:18081`;
- authentication is WebDAV-native Basic over TLS, not browser/OIDC redirect middleware;
- Samba/SMB is rejected for this deployment because its required LAN-wide overlay routing would introduce disproportionate Home infrastructure changes for an occasional workspace-access use case;
- no Home VM100/MikroTik/CT300 mutation is part of Stage 12;
- Syncthing is not used for project access because replication/conflict semantics are not desired;
- Nextcloud External Storage is not used for `/home/core/projects` because project/workspace data must remain outside the cloud-drive dataset.

## Stage 13 — Backrest WebUI Ingress

Accepted architecture:

- `backup.escloud.us` publishes the existing Backrest WebUI; it does not introduce a new backup engine or replacement product;
- Backrest remains host-native and bound only to `127.0.0.1:9898`;
- public path is `backup.escloud.us:443 -> Xray TLS -> nginx 127.0.0.1:8080 -> Authelia -> Backrest 127.0.0.1:9898`;
- TCP/80 redirects to HTTPS;
- reuse the existing shared `escloud.us` certificate, public DNS and Authelia `one_factor` policy for `backup.escloud.us`;
- no direct public Backrest listener and no dedicated UFW opening are permitted;
- nginx preserves the client `Authorization` header so Backrest-native bearer-token behavior continues to work behind the outer Authelia gate;
- reverse proxying supports Backrest ConnectRPC/streaming behavior without response buffering and with long-lived request timeouts;
- Stage 13 does not change Backrest/Restic repositories, plans/schedules, retention, restore semantics or service lifecycle.

Final acceptance: `STAGE_13_FINAL_ACCEPTANCE_2026-09-23.md`.

