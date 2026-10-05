# Cloud Infrastructure — Inventory

## Current interaction/AI tool foundation — 2026-10-02

The unified interaction/AI tool fabric is complete, with final recovery verification recorded in `EDGE_INTERACTION_AI_TOOL_FABRIC_ACCEPTANCE_2026-10-02.md`. It supersedes earlier deferral of the generic Nextcloud automation foundation; user-specific Knowledge/calendar/intake/business workflows remain future concrete-use work. Stage0–13 acceptance and the Plane Part2 core remain accepted.

- Fresh relevant runtime: n8n2.40.7, Nextcloud35.0.1, Plane MCP0.3.3, GitHub MCP1.13.0, Playwright MCP0.0.83 with existing Chromium153. Hermes native source is `5bba024d8ddd388f56f354c1f789be825e3d8a3c`; its own prior native update was not issued by this workstream.
- Plane deletion pagination is repaired and native scheduled reconciliation repeatedly succeeds. Edge Monitor now has one generic `n8n-workflow-health` incident for PlaneMattermost01, PlaneDeletionReconcile01 and PlaneGitHubPoll01; manual tests are excluded from scheduled freshness/failure counters.
- Hermes, Codex and Antigravity each have the same CE13 Plane subset, full native35-tool n8n instance MCP, official44-tool GitHub MCP and official25-tool isolated Playwright MCP. Codex alone has official read-only OpenAI Docs MCP. Existing Context7/security/browser integrations remain. Codex and Antigravity have independent ordinary operator Plane PATs; native n8n MCP uses the owner's shared one-per-user key, with autoexposure disabled and two workflows explicitly exposed.
- AIExecution01 has an explicit vllm/codex/antigravity/hermes selector. vLLM is direct private HTTP with real JSON-schema proof; CLI backends use native n8n SSH to trusted core through one dedicated encrypted key and one transparent one-shot helper, bounded to two CLI processes with timeout/cancellation/exit/stderr results. Hermes4FMachine01 was deleted by explicit operator decision on 2026-10-05; AIExecution01 and its Hermes credential remain unchanged. No automatic router, custom daemon or new Docker network.
- Nextcloud35.0.1 uses an app password of the existing OIDC operator and one encrypted native n8n credential. NextcloudTools01 provides11 reusable file/share operations through all three agents' n8n MCP. Four native file events enter a header-authenticated durable Data Table inbox before204, through existing cron and edge_internal. Nextcloud app/cron now join that existing network; public OIDC/HTTPS and native Nextcloud→Mattermost remain unchanged.
- Canonical runtime, secret-free client definitions, workflow exports and recovery contract: `deployments/edge/interaction-fabric/README.md`. Final Backrest edge-state flow395 / operations395–398 SUCCESS; actual snapshot `78d8c27cfe06be6ad31e3e7b0ec441832ea8e5c6aadefc7727ba8df084bb3007`, D5 copy `8e3b3c07bbe19661120d1d3af3c1799e8baa408db471929c03326434849c39ab`. Protected configs/helpers byte-match; native snapshot credential decryption and Plane/Nextcloud logical table readback passed. No remaining implementation scope in this authorized foundation workstream.


## Current runtime override — 2026-10-02

Plane Community Part 1, **P2-1 outbound SMTP** and **Part 2 core integrations** are **COMPLETE / ACCEPTED**, with `PLANE_PART1_CORE_DEPLOYMENT=PASS`, `PLANE_P2_1_SMTP=PASS` and `PLANE_PART2_CORE_INTEGRATIONS=PASS`. Authoritative records: `PLANE_PART_1_ACCEPTANCE_2026-10-01.md`, `PLANE_P2_1_SMTP_ACCEPTANCE_2026-10-02.md`, `PLANE_PART_2_CORE_INTEGRATIONS_ACCEPTANCE_2026-10-02.md`; deployment/recovery contract: `deployments/plane/README.md`. This current override supersedes earlier project-management runtime descriptions below.

- Plane v1.4.2 (official release ID 375236829, published 2026-08-23T14:39:21Z) serves `https://projects.escloud.us` through existing Xray/nginx/shared TLS with Plane-native authentication. Native administrator `es@escloud.us` is active; password is outside Git.
- Official vendor Compose remains unmodified at `/opt/plane/plane-app/docker-compose.yaml`. Site override, protected `plane.env` and sole transparent `/usr/local/sbin/plane-compose` wrapper enforce the accepted layout.
- Ten persistent Plane services: web, api, admin, space, live, worker, beat-worker, plane-redis (Valkey), plane-mq (RabbitMQ, stable hostname), plane-minio. Official migrator is one-shot. Embedded plane-db and bundled proxy are absent from normal startup; no Plane pgdata or public direct container ports.
- Shared PostgreSQL 18.6 retains existing Mattermost/Nextcloud plus dedicated `plane` database/login-owner role. Plane role is non-superuser, no CREATEDB/CREATEROLE. Existing postgres container identity/Env/data are unchanged by Plane deployment.
- `postgres_net` members: postgres, Mattermost, Nextcloud app/cron, Plane api/worker/beat-worker; migrator joins only during migration. `edge_internal`: n8n, Mattermost, Plane api/worker and Nextcloud app/cron, with `plane-api`, `plane-worker`, `n8n`, `n8n.edge.internal`, `nextcloud.edge.internal` aliases. Other Plane services stay on `plane_default` only. Backend webhook hostname allowlist is exactly `n8n.edge.internal`, with empty IP allowlist.
- Loopback ingress: 18110 web:3000; 18111 api:8000; 18112 admin:3000; 18113 space:3000; 18114 live:3000; 18115 MinIO:9000. nginx routes `/`, `/api/`, `/auth/`, `/static/`, `/god-mode/`, `/spaces/`, `/live/`, `/uploads/`; WebSockets and native upload signatures passed.
- Plane named volumes: plane_uploads, plane_redisdata, plane_rabbitmq_data, plane_logs_api, plane_logs_worker, plane_logs_beat-worker, plane_logs_migrator. DB/uploads/protected runtime and immutable image identities enter the existing Backrest edge-state recovery set. Valkey cache and RabbitMQ task queues persist normally but are reconstructed for historical recovery; no shared physical DB rollback.
- Nineteen persistent production containers / sixteen persistent-service images, plus one official on-demand GitHub MCP image (seventeen installed images). Monitor expects nineteen persistent containers and reports one correlated Plane service incident. Current Edge/overall state is OK. Maintenance has 16 manual targets, 9 Docker units, 23 monitored components; PLANE installed/latest v1.4.2 CURRENT, updater preflight PASS. Semaphore Update Plane template 21; no scheduled Plane update.
- Portal has nine service tiles, including Plane, using current design and live monitor status. Desktop/tablet/mobile render passed. Temporary workspace/entities/uploads/auth sessions were removed after CRUD, worker and full-container-recreate persistence acceptance.
- Outbound SMTP is accepted: existing Stalwart 0.16.24 Account/User `plane@escloud.us` (id `e`, ordinary User role, no aliases), submission `mail.escloud.us:465`, implicit TLS and certificate verification, sender `Plane <plane@escloud.us>`. Plane God Mode/runtime DB owns settings and encrypted password; no SMTP secret in Git or `plane.env`. No additional listener, DNS record, service or network was introduced.
- Part 2 core: operator-owned separate `n8n Integration` / `Hermes MCP` PATs; one issue-only workspace webhook; `PlaneEventIngress01`, 30-second `PlaneMattermost01`, 5-minute native API deletion reconciliation, 15-minute GitHub polling + idempotent PR comment sync, and official Hermes MCP stdio. Existing n8n bot serves private `plane` channel with exactly eugene+n8n. Current CE API/MCP deletes require activity reconciliation (not an emitted delete webhook). Knowledge/user-specific workflows, external calendar and intake are deferred pending concrete use cases; the generic Nextcloud automation/tool foundation is now complete.
- Unified Part 2 recovery: Backrest flow384 / operations384–387 SUCCESS, actual snapshot `3977cc69b645d86cbaf35dcdd3be6cc00b8af70d0c431dfa96ed7167bb414906` read back for Plane/n8n/Hermes/Mattermost/mail. Final Edge/overall OK; no additional endpoint/network/database/service. Secret-free definitions: `deployments/plane/integrations/`.
- OpenProject remains **DECOMMISSIONED**, with zero active runtime/integration residue. Historical records/recovery artifacts remain unchanged; historical matched DB/opdata recovery is in Restic snapshot `79ac237d`. External Apple Calendar subscription remains a manual client-side check from the decommission workstream.

All earlier dated OpenProject deployment/integration/rollback descriptions are **HISTORICAL_REFERENCE**. The decommission acceptance record describes its own earlier checkpoint; its `PLANE_DEPLOYMENT=NOT_STARTED` marker is historical and superseded by this Plane acceptance.


## Semantics

Fresh runtime verification outranks this file. This inventory records accepted live components, selected/deferred targets, external dependencies and unresolved later-stage choices.

## Nodes

| Node | Role | State |
|---|---|---|
| `edge` / `edge.escloud.us` | Cloud Infrastructure VPS | LIVE; Stage 0–13 COMPLETE / ACCEPTED |
| `nl-core-vds` | historical legacy VPS identity | HISTORICAL ONLY |
| `ai-node` | PAI compute/data/knowledge node | external dependency/context; Stage 3 private target; Stage 4 local-vLLM endpoint |
| PVE / Home Infrastructure | home infrastructure plane | external dependency/context; Stage 3 private routed fabric |
| CT300 `remote-access` | Home self-hosted NetBird control/routing plane | EXISTING / REUSED / Stage 3 ACCEPTED |
| VM100 `gateway-core` | Home VRRP/Mihomo gateway | EXISTING / routing participant for Home→NetBird account path |
| MikroTik | Home physical router / VRRP backup | EXISTING / routing participant and fallback |

## Live `edge` substrate

- Ubuntu 26.04.1 LTS, kernel `7.0.0-31-generic`;
- public IPv4 `45.92.156.17`; no public/global IPv6 on `ens3`; IPv6 retained for link-local/NetBird overlay use;
- Docker `29.8.1`, Compose `5.5.1`, containerd `2.3.5`; `live-restore=false`; production application containers use `restart=unless-stopped`;
- nginx `1.28.3-2ubuntu1.11`;
- Xray `26.3.27`;
- Hysteria2 `2.12.3`;
- Authelia `4.39.27`;
- trusted service/operator account `core` UID/GID `1000:1000`, locked password, full non-interactive root via `/etc/sudoers.d/90-core-root` (`NOPASSWD: ALL`), no separate `docker` group membership required;
- UFW intentional ingress: TCP 22/80/443/25/465/993 and UDP 443;
- WebUI application backends are loopback-only by default.

## Stage 3 — COMPLETE / ACCEPTED

`EDGE_STAGE3_FINAL_INTEGRATED_ACCEPTANCE=PASS` on 2026-09-18.

Accepted live connectivity inventory:

- NetBird `0.79.0` host-native on `edge`;
- `edge` overlay IPv4 `100.105.178.187/16`;
- CT300 overlay IPv4 `100.105.97.126/16`;
- Home LAN `192.168.1.0/24` routed through `wt0`;
- Home `.lan` split DNS available from `edge`;
- direct P2P CT300 <-> `edge` on UDP/51820 verified;
- final reboot P2P recovery approximately `13.187s` from actual `edge` boot;
- final sustained CT300 -> `edge`, `edge` -> CT300/PVE/`ai-node` traffic passed with 0% loss;
- VM100/MikroTik unchanged; LAN-wide clientless overlay routing remains deferred;
- no `edge.lan` baseline record.

Final record: `STAGE_03_ACCEPTANCE_2026-09-18.md`.

## Reboot lifecycle corrective state

- Stage 1's explicit `live-restore=true` setting was superseded on 2026-09-18;
- current Docker runtime uses `live-restore=false`;
- post-fix normal reboot: total boot `13.842s`, previous-journal-stop to new-kernel gap `4.203s`;
- all four production containers returned automatically via `restart=unless-stopped`;
- acceptance: `EDGE_REBOOT_AFTER_LIVE_RESTORE_FIX_ACCEPTANCE_V1=PASS`;
- detailed record: `EDGE_REBOOT_LIFECYCLE_FIX_ACCEPTANCE_2026-09-18.md`.

### 2026-09-23 follow-up reboot correction

- later ~90-second shutdown stall traced to unused `multipathd.service`, not SSH/network or Docker;
- edge has no multipath maps and no device-mapper devices; root remains ext4 on `/dev/vda1`;
- `multipathd.service` disabled/inactive; `multipath-tools` package retained;
- final reboot request -> SSH listening: ~26.7 s;
- new kernel -> SSH listening: ~7.9 s;
- full system startup: `18.348s`;
- Codex `0.156.0` native managed daemon + native updater boot persistence accepted through minimal oneshot start trigger;
- Antigravity `1.2.7` native registered user service reboot persistence accepted;
- acceptance: `EDGE_COMBINED_REBOOT_ACCEPTANCE=PASS`;
- detailed record: `EDGE_REMOTE_CLI_AND_REBOOT_LIFECYCLE_ACCEPTANCE_2026-09-23.md`.

## Stage 2 — COMPLETE / ACCEPTED

`EDGE_STAGE2_FINAL_INTEGRATED_ACCEPTANCE=PASS` on 2026-09-17.

| Component | State | Runtime / notes |
|---|---|---|
| Authelia | LIVE / ACCEPTED | current `4.39.28`; `127.0.0.1:19091`; fresh operator/auth secrets; `auth.escloud.us` |
| n8n | LIVE / ACCEPTED | current `2.39.10`; `127.0.0.1:15678`; fresh one-owner state; `n8n.escloud.us`; Authelia protected |
| CloudCLI | RETIRED / ACCEPTED | retired 2026-09-23; systemd/listener/npm/state/workspace removed; `code.escloud.us` preserved for T3 |
| Codex CLI | LIVE / ACCEPTED | current `0.156.0`; official standalone; fresh ChatGPT auth; native managed Remote Control via Unix socket; native updater enabled; minimal user oneshot boot-trigger invokes `codex remote-control start --json`; no legacy direct app-server service |
| Antigravity CLI | LIVE / ACCEPTED | current `1.2.7`; Stage 4G accepted `1.2.6`; Stage 2/4B historical `1.2.5`; Google OAuth; instance `edge`; persistent user service |
| Stalwart | LIVE / ACCEPTED | current `0.16.23`; public SMTP25/SMTPS465/IMAPS993; useful mail data migrated; fresh auth/DKIM |
| Bulwark | LIVE / ACCEPTED | `1.9.2`; `127.0.0.1:18084`; fresh session/admin state; default webmail route on `mail.escloud.us` |

### Accepted identities / hashes

- Authelia compose SHA256 `265dc881294e4b14bf9da5b529570ff6a2f234de2a3e335681d34d3deb447e96`;
- n8n compose SHA256 `03f6e88c137dedf5c5ed5cb8481c097bc2ab322e612c745f636a8fcc9117dda0`;
- historical CloudCLI systemd unit SHA256 `8bf303e000b3de0f5a761fc0a466139a75e72fd6ec5d07b08ab7cb82f95382af`; runtime unit is now absent;
- mail compose SHA256 `7de766ed23fd7c30f63870f25af648f018d3295685fb58e40b88eaa578d2d4de`;
- mail nginx SHA256 `601ff1feffcef8729901b1e00ab98001934db03a1315b55233965ba5d75f079c`;
- Stalwart image digest `sha256:388dcb75a70727c5b551249a6d34b1f1321294852489e4fa3a4e6be698b7c4f0`;
- Bulwark image digest `sha256:0e8d1339277033b6569a76c6f8192396e6edd66fd917d64d9ed505e8b81dac6d`;
- accepted mail TLS fingerprint `3D:5A:77:15:78:4C:53:74:4B:D7:C2:6C:86:96:5B:10:DB:F9:7B:32:45:9A:F0:CD:B9:BD:39:A1:8B:9B:9B:F8`.

## Mail inventory

- domain `escloud.us`;
- `mail.escloud.us` A `45.92.156.17`; no mail AAAA;
- MX `10 mail.escloud.us.`;
- PTR `45.92.156.17 -> mail.escloud.us`;
- SPF `v=spf1 ip4:45.92.156.17 -all`;
- DMARC `v=DMARC1; p=none; adkim=s; aspf=s`;
- active DKIM: `v1-rsa-20260917`, `v1-ed25519-20260917`;
- legacy DKIM `v1-rsa-20260713` retired;
- `es@escloud.us`: 6 mailboxes, 14 migrated messages plus useful address-book/calendar/identity state;
- outbound/inbound Gmail acceptance: delivery, SPF, DKIM and DMARC PASS as documented in Stage 2 acceptance.

## Domain inventory

### Public/current/future `escloud.us`

- `escloud.us` — public masking/masquerade page;
- `edge.escloud.us` — infrastructure hostname;
- `auth.escloud.us` — live Authelia;
- `n8n.escloud.us` — live n8n;
- `code.escloud.us` — RESERVED FOR T3; existing DNS/TLS/Authelia ingress preserved; current backend placeholder returns 503 until T3 WebUI deployment;
- `mail.escloud.us` — live Stalwart + Bulwark;
- `backup.escloud.us` — PLANNED / DEFERRED: future ingress for the existing Backrest management UI; no new backup product;
- `ops.escloud.us` — FULLY RETIRED; removed from edge runtime/configuration/certificate/recovery state on 2026-09-21 and public Cloudflare DNS A record confirmed absent during Stage 10;
- `update.escloud.us` — LIVE maintenance dashboard and full Semaphore UI through Xray, host nginx and Authelia; `/` redirects to `/status/`, the Semaphore history UI is `/project/1/history`, and both backends remain loopback-only;
- `app.escloud.us` — live Stage 9 Cloud Portal; static nginx + Authelia; same-origin read-only Stage 8 status
- `docs.escloud.us` — DEFERRED UNTIL CONTENT READY: future WenTian Product Guide/Datasheet publishing site for EN/RU translated corpus;
- `hermes.escloud.us` — LIVE accepted Hermes Dashboard/Remote Gateway; native self-hosted OIDC through Authelia; backend loopback-only;
- `chat.escloud.us` — LIVE Mattermost human endpoint; core runtime and public nginx ingress accepted; native Mattermost authentication without Authelia;
- `cloud.escloud.us` — LIVE / ACCEPTED: Nextcloud personal cloud-drive; user-visible files under `/srv/cloud`, Nextcloud-specific state under `/srv/nextcloud`, backend `127.0.0.1:18080`;
- `sync.escloud.us` — RETIRED: legacy public Syncthing UI role; current Syncthing remains private Knowledge replication and Stage 12 Nextcloud owns end-user cloud sync;
- `go.escloud.us` — LIVE / ACCEPTED Stage 12 WebDAV endpoint for exactly `/home/core/projects/`; Xray TLS -> nginx -> rclone `127.0.0.1:18081`; protocol-native Basic auth over HTTPS.

### Private `.lan`

- existing Home `.lan` namespace is accepted for NetBird split-DNS reuse on `edge`;
- `edge.lan` is intentionally not created in the baseline Stage 3 architecture; public `escloud.us` naming remains the Home/PAI access path to Cloud services;
- `.lan` does not replace public `*.escloud.us` service naming.

# Stage 02.5 — accepted research inventory

## Remaining Standalone Core Services

Status: **RESEARCH BLOCK COMPLETE / SELECTED**.

| Component | Outcome | Intended role |
|---|---|---|
| Hermes Agent | `DEPLOYED / ACCEPTED` | persistent cloud-side agent runtime for reasoning, tools, direct executors, Dashboard/Desktop and private n8n invocation |

Accepted placement/integration direction:

- host-native under `core` by default;
- n8n remains deterministic workflow/orchestration plane;
- Hermes remains agentic reasoning/delegation plane;
- Codex/Antigravity remain manually usable specialist tools/executors; CloudCLI is retired;
- Stage 4 verifies `n8n -> Hermes -> Codex/AGY -> Hermes -> n8n`;
- Stage 4 also verifies real `Hermes -> vLLM on ai-node` through the Stage 3 private fabric;
- `hermes.escloud.us` is the accepted Dashboard/Desktop endpoint using native self-hosted OIDC; the backend remains loopback-only.

## Cross-site Connectivity Foundation

Status: **RESEARCH BLOCK COMPLETE / SELECTED / REUSE EXISTING**.

Accepted mechanism: existing self-hosted Home NetBird.

Fresh audited baseline:

- Home LAN `192.168.1.0/24`;
- CT300 `192.168.1.90`;
- NetBird routing peer `100.105.97.126/16`;
- account overlay `100.105.0.0/16`;
- `Networks` model active; legacy routes empty;
- `Home LAN` resource `192.168.1.0/24`;
- `Internet` resource `0.0.0.0/0` currently restricted to `User Devices` policy;
- split-DNS `192.168.1.1:53` for `lan`;
- CT300 own default gateway `192.168.1.1`;
- NetBird `wt0` traffic policy-routed through VRRP VIP `192.168.1.254` for the existing Home Internet Exit use case.

Current Stage 3 runtime / accepted scope:

- host-native NetBird peer on `edge` version `0.78.2`;
- `edge` NetBird IPv4 `100.105.178.187/16`;
- dedicated Cloud service-peer grouping/policy deployed;
- Home LAN access for `edge`, no Home Internet Exit;
- provider-local `edge` default Internet route unchanged;
- Home `.lan` split DNS consumed by `edge`;
- CT300 remains the Home routing/control-plane foundation;
- no VM100/MikroTik route/firewall mutation in the baseline implementation;
- no `edge.lan` baseline record;
- LAN-wide clientless Home/PAI -> `edge` overlay routing deferred until a concrete private-only workload requires it;
- Stage 3 reboot acceptance uncovered and resolved the independent Docker `live-restore` shutdown regression; final connectivity acceptance is complete.

Detailed record: `STAGE_02_5_CONNECTIVITY_SELECTION_ACCEPTANCE_2026-09-17.md`.

## Stage 5 knowledge/data boundary

Status: **Stage 5 COMPLETE / ACCEPTED**.  
`STAGE05_FINAL_ACCEPTANCE=PASS`.

Authoritative records:

- `STAGE_05_1_FINAL_KNOWLEDGE_RUNTIME_ARCHITECTURE_ACCEPTANCE_2026-09-19.md`;
- `STAGE_05_2_FINAL_ACCEPTANCE_2026-09-19.md`;
- `STAGE_05_3_FINAL_ACCEPTANCE_2026-09-20.md`.

### PVE / CT210 `obsidian` — LIVE / ACCEPTED

- dedicated `pve/knowledge` 32 GiB ext4 LV mounted at `/srv/knowledge`;
- vault `/srv/knowledge/obsidian`;
- PVE Syncthing `2.1.5`, folder ID `knowledge-obsidian`, `sendreceive`;
- PVE Device ID `I6IHLDJ-2E2SH2D-RREAJIY-VFP7TG5-N4DKRDR-GDIUQHA-P2NHQ3O-MR4WOAY`;
- listener `192.168.1.3:22000`, GUI/API `127.0.0.1:8384`;
- peers: ai-node and edge;
- CT210 remains the accepted Ignis/Obsidian private runtime at `obsidian.lan`.

### ai-node — LIVE / ACCEPTED

- active RW replica `/srv/ai-data/knowledge/obsidian`;
- existing Syncthing peer to PVE;
- n8n/OCR/RAG/AI consumers remain in place;
- no server-side Obsidian runtime/WebUI by default;
- normal edge → PVE → ai-node propagation verified.

### edge — LIVE / ACCEPTED

- active RW replica `/srv/knowledge/obsidian`;
- `/srv/knowledge`: `core:core 0755`;
- `/srv/knowledge/obsidian`: `core:core 2775`;
- Syncthing `2.1.5` from upstream `stable-v2`;
- service `syncthing@core.service`: enabled and reboot-persistent;
- edge Device ID `DPBP3KW-L5BEWJM-RPDDHO2-ON5AYFR-VEE4TP5-NOIOOES-NGJ3D4R-VJFXQAE`;
- PVE peer `I6IHLDJ-2E2SH2D-RREAJIY-VFP7TG5-N4DKRDR-GDIUQHA-P2NHQ3O-MR4WOAY` at `tcp://192.168.1.3:22000`;
- folder ID `knowledge-obsidian`, type `sendreceive`, watcher enabled, rescan 3600 s;
- edge listener `127.0.0.1:22000`, GUI/API `127.0.0.1:8384`;
- global/local discovery, relays and NAT traversal disabled;
- no public Syncthing exposure;
- Hermes/Codex/Antigravity use the local path directly;
- n8n bind `/srv/knowledge/obsidian:/srv/knowledge/obsidian:rw`;
- n8n `node` UID/GID `1000:1000`;
- `n8n_hermes` bridge contract unchanged;
- propagation, outage/reconnect, conflict preservation and edge reboot acceptance passed;
- no edge Obsidian runtime/WebUI.

Future external client access through edge remains outside Stage 5.

# Deployment stage inventory

| Stage | Scope | Current status |
|---|---|---|
| 3 | Cross-site Connectivity Foundation | COMPLETE / ACCEPTED; `EDGE_STAGE3_FINAL_INTEGRATED_ACCEPTANCE=PASS` |
| 4 | Hermes Agent Runtime | COMPLETE / ACCEPTED; `STAGE4_FINAL_ACCEPTANCE=PASS` |
| 05.1 | Cross-project Knowledge Reconciliation & Target Architecture | COMPLETE / ACCEPTED |
| 05.2 | PVE Canonical Obsidian Runtime & WebUI | COMPLETE / ACCEPTED; `STAGE05_2_PVE_CANONICAL_OBSIDIAN_RUNTIME=PASS` |
| 05.3 | Edge Knowledge Replication & Data Integration | COMPLETE / ACCEPTED; `STAGE05_3_EDGE_KNOWLEDGE_REPLICATION_DATA_INTEGRATION=PASS` |
| 6 | Backrest & Recovery | COMPLETE / ACCEPTED; `STAGE06_FINAL_ACCEPTANCE=PASS` |
| 7 | Maintenance & Update | COMPLETE / ACCEPTED; `STAGE07_FINAL_ACCEPTANCE=PASS` |
| 8 | Monitoring, Heartbeats & Alerts | COMPLETE / ACCEPTED; `STAGE08_FINAL_ACCEPTANCE=PASS` |
| 9 | Cloud Portal: `app.escloud.us` | COMPLETE / ACCEPTED; `STAGE09_FINAL_ACCEPTANCE=PASS` |
| 10 | Final Integrated Infrastructure Acceptance | COMPLETE / ACCEPTED; `STAGE10_FINAL_ACCEPTANCE=PASS` |
| 11 | Remaining Infrastructure Gap Reconciliation & Completion | COMPLETE / ACCEPTED; `STAGE11_FINAL_ACCEPTANCE=PASS` |
| 12 | Nextcloud Cloud Drive & Private Workspace Access | COMPLETE / ACCEPTED; `STAGE12_FINAL_ACCEPTANCE=PASS` |
| 13 | Backrest WebUI Ingress | COMPLETE / ACCEPTED; `STAGE13_FINAL_ACCEPTANCE=PASS` |

## Post-infrastructure application/workflow layer

Continuous workstream after completed infrastructure Stage 13, not an infrastructure-completion stage:

- n8n workflows;
- Hermes/agent workflows;
- Universal Capture Inbox;
- human-in-the-loop approvals;
- mail-triggered automation;
- continuous information intake/change detection;
- bounded AI research jobs;
- durable application-level store-and-forward/retry for actual cross-site tasks;
- optional messaging/bot command frontend;
- user-specific orchestration among n8n, Hermes, Codex CLI, Antigravity CLI and local vLLM/PAI.

## Optional capabilities still requiring disposition

- password/2FA vault;
- limited failover/secondary-endpoint role;
- additional messaging/control frontend only if it adds value beyond selected workflow interaction surfaces.

## Recovery artifacts

- historical baseline: `NL_CORE_VDS_Current_State_Baseline_2026-09-14.md`;
- Stage 1 recovery archive `/srv/backups/edge-stage1/edge-stage1-base-20260916T234611Z.tar.gz`, SHA256 `37486e763ddac4c5ef3a92a35c3dad49787d75ffd8b97499073c79af617cc566`;
- historical migration-preservation archive identity: `/tmp/edge-migration-preservation-20260916T141048Z.tar.gz`, SHA256 `0203e5845f57bc1d04b384cef2b26a45fbff855c341e1edf1193034c34de9fdf`. The path is absent and the archive was declared no longer required on 2026-09-19. It must not be recreated; sanitized `migration-reference/` remains in Git.


### 2026-09-29 Stage 1 PostgreSQL consolidation rollback inventory (reconciled)

- **Mattermost dump**:
  - Primary persistent canonical artifact: `/srv/mattermost/backups/mattermost_dump_pre_consolidation.sql` (size: 531682 bytes, SHA256: `6ff90d4af634797cb8d96062977382e60ea62575cbd302a45b2757f86ca5aafa`);
  - Worktree copy (identical content and size): `/opt/mattermost/mattermost_dump_pre_consolidation.sql`;
  - Note: Both files exist and are verified bitwise identical; `/srv/mattermost/backups/` is the authoritative persistent location. Neither file was moved or deleted.
- **Nextcloud old PostgreSQL cluster**:
  - Exact verified path: `/srv/nextcloud/postgres` (contains `18/data`, cluster files owned by `70:70`);
  - Verified container mount: `nextcloud-db-1` was inspected, bind mount source is `/srv/nextcloud/postgres`;
  - Path `/srv/nextcloud/db` is **absent** (non-existent, reconciled as historical false reference).
- **OpenProject evaluation rollback state**:
  - Stopped container: `openproject-db-1` (image `postgres:17`, status `Exited (0)`);
  - Docker volume: `openproject_pgdata` (mountpoint `/var/lib/docker/volumes/openproject_pgdata/_data`);
  - Stopped container: `openproject-hocuspocus-1` (image `openproject/hocuspocus:17.8.0`, status `Exited (0)`);
  - Upstream backup manifests: `/opt/openproject/docker-compose.yml.bak`, `/opt/openproject/proxy/Caddyfile.template.bak`.
- **Other backup manifests**:
  - `/opt/mattermost/docker-compose.yml.bak`;
  - `/opt/nextcloud/compose.yaml.bak`.

## Stage 4 services — Hermes / Mattermost / n8n integration

### Hermes Dashboard / Desktop

- status: **COMPLETE / ACCEPTED**;
- Hermes `0.21.3`, commit `d177b119e9c56c9ddc0b7379ffce52341ec06584`;
- public `https://hermes.escloud.us` through Xray/nginx/shared TLS;
- loopback backend `127.0.0.1:9119`, persistent `hermes-dashboard.service`;
- native self-hosted OIDC with Authelia `4.39.27`, one provider, PKCE/S256;
- browser Dashboard Chat/session and WebSocket accepted;
- macOS Desktop native authorization/token/WebSocket/reconnect accepted;
- no nginx `auth_request` and no public TCP/9119.

### Hermes private n8n interface

- status: **COMPLETE / ACCEPTED**;
- native API Server `172.19.0.1:8642`, Bearer auth, n8n Docker bridge only;
- Compose network `n8n_hermes`, stable Linux bridge `n8n-hermes`, subnet `172.19.0.0/16`, gateway `172.19.0.1`;
- narrow UFW rule from `172.19.0.0/16` on `n8n-hermes`; no public nginx route/listener;
- current n8n Hermes caller: `AIExecution01`, ID `wQ9ZqMisMCGadGEE`, active/published; the former `Hermes4FMachine01` was retired by explicit operator decision on 2026-10-05;
- n8n encrypted Bearer credential `Hermes4FAuth01`;
- current explicit AIExecution01 backend values: `vllm`, `codex`, `antigravity`, `hermes`; historical Stage 4 selector acceptance is preserved;
- all three E2E paths accepted; temporary workflows removed;
- original recovery root: `/srv/backups/edge-stage4f/recovery-20260918T174246Z`;
- network-hardening recovery root: `/srv/backups/edge-stage4f-network/recovery-20260919T124318Z`.

### Mattermost

- status: **STAGE 4E COMPLETE / ACCEPTED**; core runtime, ingress, native config, Hermes↔Mattermost, n8n↔Mattermost, Agents normalization, mobile/TPNS and final non-regression all accepted;
- Mattermost Team `11.11.0`, official `mattermost/docker` commit `497414659ee7127677d2b91b44bb4f3ea9d14695`;
- PostgreSQL `18-alpine`;
- persistent state under `/srv/mattermost`, upstream deployment under `/opt/mattermost`;
- only host application publication: `127.0.0.1:18065 -> 8065`; PostgreSQL no host binding;
- public endpoint `https://chat.escloud.us` via Xray -> host nginx -> shared TLS;
- Mattermost-native auth, no Authelia;
- TPNS configured; Calls disabled;
- Hermes↔Mattermost accepted with bot `hermes`, private service channel `hermes` and real E2E response;
- Mattermost↔Stalwart SMTP explicitly not required / not enabled;
- prepackaged `mattermost-ai` / Agents `2.6.1` remains installed but is disabled; enabled-list count `0`, disabled-list count `1`, `config.json` state `Enable=false`.

Acceptance records:

- `STAGE_04D_MATTERMOST_DESIGN_ACCEPTANCE_2026-09-18.md`;
- `STAGE_04E_MATTERMOST_CORE_RUNTIME_ACCEPTANCE_2026-09-18.md`;
- `STAGE_04E_MATTERMOST_INGRESS_ACCEPTANCE_2026-09-18.md`;
- `STAGE_04E_MATTERMOST_NATIVE_SERVER_CONFIG_ACCEPTANCE_2026-09-18.md`;
- `STAGE_04E_HERMES_MATTERMOST_INTEGRATION_ACCEPTANCE_2026-09-18.md`;
- `STAGE_04E_N8N_MATTERMOST_INTEGRATION_ACCEPTANCE_2026-09-18.md`;
- `STAGE_04E_MATTERMOST_AGENTS_NORMALIZATION_ACCEPTANCE_2026-09-18.md`;
- `STAGE_04E_MATTERMOST_MOBILE_TPNS_ACCEPTANCE_2026-09-18.md`;
- `STAGE_04E_FINAL_ACCEPTANCE_2026-09-18.md`.

### n8n ↔ Mattermost

- status: **COMPLETE / ACCEPTED**;
- n8n `2.39.7`;
- official built-in `n8n-nodes-base.mattermost`, typeVersion `1`;
- one credential: `Mattermost API - chat.escloud.us`, ID `16a0a988ad514ab1`;
- Mattermost bot `n8n`, ID `4ty8tfwmdir9mxkeua3n7658mc`;
- one active bot access token, description `n8n-native-mattermost`;
- credential/API identity validation: PASS;
- operator DM channel ID `srzsm58fepgujjfnyxb8f7zo3o`;
- native-node E2E marker: `N8N_MATTERMOST_NATIVE_E2E_OK_20260918T135107Z`;
- verified Mattermost post ID `1fgnm3fumbyy8b4usrrs41kouc`;
- Stage 4E acceptance left production workflows at 0; current Stage 4F production state has one published Hermes machine workflow and two total credentials;
- `STAGE4E_N8N_MATTERMOST_INTEGRATION=PASS`.

Stage 4E final non-regression passed: `STAGE4E_FINAL_NON_REGRESSION=PASS`; `STAGE4E_FINAL_ACCEPTANCE=PASS`. No Stage 4E gates remain.

### Hermes lifecycle observation

- `hermes-gateway.service` currently active/enabled with `NRestarts=0`;
- controlled stop/restart currently exits status 1 after SIGTERM and is recorded by systemd as a failed stop before restart succeeds;
- exit-status-1 is an accepted documented upstream constraint; requested restart recovery passes and no `SuccessExitStatus=1` masking is used.

## Stage boundary

Stage 0 — COMPLETE / ACCEPTED.  
Stage 1 — COMPLETE / ACCEPTED.  
Stage 2 — COMPLETE / ACCEPTED.  
Stage 02.5 — COMPLETE / ACCEPTED.  
Stage 3 — COMPLETE / ACCEPTED.  
Stage 4 — COMPLETE / ACCEPTED.  
Stage 5 — COMPLETE / ACCEPTED.  
Stage 6 — COMPLETE / ACCEPTED.  
Stage 7 — COMPLETE / ACCEPTED.  
Stage 8 — COMPLETE / ACCEPTED.  
Stage 9 — COMPLETE / ACCEPTED.  
Stage 10 — COMPLETE / ACCEPTED.  
Stage 11 — COMPLETE / ACCEPTED.  
Stage 12 — COMPLETE / ACCEPTED.  
Stage 13 — COMPLETE / ACCEPTED.  

Final markers: `EDGE_STAGE3_FINAL_INTEGRATED_ACCEPTANCE=PASS`, `STAGE4_FINAL_ACCEPTANCE=PASS`, `STAGE05_FINAL_ACCEPTANCE=PASS`, `STAGE06_FINAL_ACCEPTANCE=PASS`, `STAGE07_FINAL_ACCEPTANCE=PASS`, `STAGE07_2_FINAL_MASTER_BATCH_EXECUTION=PASS`, `STAGE08_FINAL_ACCEPTANCE=PASS`, `STAGE09_FINAL_ACCEPTANCE=PASS`, `STAGE10_FINAL_ACCEPTANCE=PASS`, `STAGE11_FINAL_ACCEPTANCE=PASS`, `STAGE12_FINAL_ACCEPTANCE=PASS`, `STAGE13_FINAL_ACCEPTANCE=PASS`.


## Stage 8 monitoring runtime

- status: **COMPLETE / ACCEPTED**; `STAGE08_FINAL_ACCEPTANCE=PASS`;
- service: host-native `edge-monitor.service`, persistent Python process, systemd-supervised;
- cadence: FAST 5s / NORMAL 20s / SLOW 60s / OPERATIONS 300s;
- confirmation: two consecutive failed ordinary endpoint probes before `FAIL`;
- live status: `/run/edge-monitor/snapshot.json`;
- durable transition state: `/var/lib/edge-monitor/state.json`;
- domains: EDGE, APPLICATIONS, HOME_PAI, KNOWLEDGE, OPERATIONS;
- alert transport: dedicated Mattermost incoming webhook to private `Monitoring` channel; transition/recovery only;
- Docker monitoring contract at acceptance: six running workloads — `authelia`, `bulwark`, `mattermost-mattermost-1`, `mattermost-postgres-1`, `n8n`, `stalwart`;
- Backrest source: `/var/lib/backrest/oplog.sqlite`, successful snapshot operations joined by plan ID;
- accepted Backrest freshness thresholds: OK <=7h, DEGRADED >7h, FAIL >13h;
- Stage 7 update metadata is read-only/informational; monitoring does not trigger maintenance Refresh;
- no monitoring database, separate receiver/WebUI, external monitoring service or independent vantage point;
- accepted limitation: complete edge loss cannot be reported from the edge-only runtime while the node is unreachable;
- final record: `STAGE_08_FINAL_ACCEPTANCE_2026-09-22.md`.

## Stage 9 Cloud Portal runtime

- public endpoint: `https://app.escloud.us`;
- static root: `/var/www/app.escloud.us`;
- nginx vhost: `/etc/nginx/sites-available/app-escloud-us.conf` -> `/etc/nginx/sites-enabled/app-escloud-us.conf`;
- authentication: existing Authelia `auth_request`;
- status endpoint: same-origin `/api/status`;
- status source: `/run/edge-monitor/snapshot.json`;
- portal has no independent backend service, container, database or update mutation plane;
- final acceptance: `STAGE09_FINAL_ACCEPTANCE=PASS`.


## Stage 10 final integrated inventory checkpoint

Final acceptance: `STAGE10_FINAL_ACCEPTANCE=PASS`.

Fresh Stage 10 runtime reconciliation confirmed the following current mutable versions without rewriting historical stage-specific acceptance evidence:

- NetBird `0.79.0`;
- n8n `2.39.10`;
- Authelia `4.39.28`;
- Stalwart `0.16.23`;
- Codex CLI `0.155.1`;
- CloudCLI `1.37.3` at the historical Stage 10 checkpoint; subsequently retired on 2026-09-23;
- Antigravity CLI `1.2.7`;
- Hermes `0.21.3`;
- Mattermost `11.11.0`;
- PostgreSQL `18.6`;
- Syncthing `2.1.5`;
- Backrest `1.14.1`;
- Restic `0.19.1`;
- Semaphore `2.19.12`;
- Xray `26.3.27`;
- Hysteria2 `2.12.3`;
- Docker Engine `29.8.1`;
- Docker Compose `5.5.1`;
- containerd `2.3.5`;
- nginx `1.28.3-2ubuntu1.11`;
- Certbot `4.0.0-4`;
- UFW `0.36.2-9build1`.

The exact accepted runtime `maintenance/edge/scripts/manual-update` is now persisted in the canonical repository, closing the Stage 7 source drift noted at Stage 7 acceptance.

Final record: `STAGE_10_FINAL_ACCEPTANCE_2026-09-22.md`.

Post-acceptance recovery inventory: one provider golden VPS snapshot was created successfully by the operator after Stage 10 final acceptance, satisfying the one-time Stage 6 post-build snapshot requirement. Snapshot provider-side identifier is not recorded in the repository.


## Stage 10 clean production baseline

Final hygiene cleanup acceptance:

- `STAGE10_FINAL_BASELINE_CLEANUP=PASS`;
- `STAGE10_PRODUCTION_NON_REGRESSION=PASS`;
- `STAGE10_CLEANUP_FAILURES=0`;
- `REBOOT_REQUIRED=NO`;
- final RC=0.

Verified cleanup removed:
- APT package cache;
- npm/npx caches for root and core;
- core UV download/build cache;
- obsolete Codex standalone release `0.154.0`, while `current` remains `0.155.1`;
- completed Stage 1/3/4/5/7 local rollback artifacts superseded by accepted current state, Backrest recovery and the provider golden snapshot;
- confirmed Stage 7/9 temporary audit/test artifacts;
- verifier-generated Python bytecode;
- stale package/install residue files.

Preserved intentionally:
- running kernel `7.0.0-31` plus one fallback kernel `7.0.0-15`;
- system journals and normal logrotate history;
- Playwright Chromium runtime cache used by Hermes tooling;
- installed UV runtimes/tools under `/home/core/.local/share/uv`;
- Restic repository caches;
- runtime-managed temporary directories;
- all production Docker images/containers/networks;
- production nginx/systemd configuration;
- `pollinate` OS package.

Measured root filesystem reclaim: `1,900,048,384` bytes (`1.77 GiB`). Post-clean root usage: approximately `22 GiB used / 133 GiB available / 14%`.


## Stage 12 filesystem access — LIVE / ACCEPTED

Authoritative record: `STAGE_12_FINAL_ACCEPTANCE_2026-09-23.md`.

### Cloud drive

- `cloud.escloud.us`: live Nextcloud personal cloud drive;
- user-visible portable file tree: `/srv/cloud`;
- Nextcloud-specific persistent state: `/srv/nextcloud`;
- backend: `127.0.0.1:18080`.

### Direct project/workspace access

- `go.escloud.us`: live WebDAV endpoint;
- published tree: exactly `/home/core/projects/`;
- implementation: rclone `1.75.1`, `projects-webdav.service` under `core`;
- backend: `127.0.0.1:18081` only;
- public path: Xray TLS -> nginx -> rclone;
- authentication: HTTP Basic over HTTPS;
- Samba/SMB Stage 12 implementation is rejected and fully removed;
- no Home VM100/MikroTik/CT300 mutation is required.

### Other future tasks

- `backup.escloud.us`: publish existing Backrest WebUI through accepted ingress/auth;
- `docs.escloud.us`: deploy only after a useful EN/RU translated WenTian Product Guide/Datasheet corpus exists.

### Retired namespace

- `sync.escloud.us`: retired legacy public Syncthing hostname.


## Stage 07.2 current maintenance ownership

- status: **COMPLETE / ACCEPTED**;
- ownership policy: native-first; Maintenance execution plane: manual-only;
- target model: `update_units_v5`;
- raw Maintenance rows: 25;
- manual actionable Maintenance targets: 18;
- Hermes/Codex: absent from Maintenance collector, generated targets, actions, UI and Semaphore templates;
- native automatic owners outside Maintenance: Hermes native cron + settlement, Codex managed-daemon `pid-update-loop`, Ubuntu package-owned unattended-upgrades;
- `actions.json`: schema 10, 18 components, `execution_mode=manual_only`, `auto_update=false`;
- normal/third-party APT remains `APT_EDGE`; automatic reboot disabled;
- Codex accepted runtime: `0.156.1`, native updater active;
- Hermes accepted runtime: `v0.21.4`, native cron updater plus settlement timer active;
- Rclone: `1.75.1`, `/usr/bin/rclone`, persistent `core` user service `projects-webdav.service`;
- Nextcloud maintenance targets: app, PostgreSQL, Redis;
- Bulwark configured track: `ghcr.io/bulwarkmail/webmail:latest`;
- Semaphore template IDs: Refresh 1, Master 18, Rclone 14, Nextcloud 16, Nextcloud PostgreSQL 19, Nextcloud Redis 20;
- Stage 8 authoritative maintenance source: `/var/www/maintenance-status/maintenance.json`;
- final acceptance: `STAGE07_2_CORRECTIVE_MIGRATION=PASS`;
- record: `STAGE_07_2_FINAL_NATIVE_UPDATE_OWNERSHIP_ACCEPTANCE_2026-09-23.md`.


### T3 Code persistent remote workspace

- runtime owner: official `t3code.service` user unit under `core`;
- accepted version: `0.0.43-nightly.20260923.2150` (temporary compatibility pin);
- backend: `127.0.0.1:3773`;
- project root: `/home/core/projects`;
- public WebUI: `https://code.escloud.us` via existing Xray/nginx/Authelia ingress;
- remote client transport: T3 Connect;
- relay client: managed `cloudflared 2026.5.2`;
- accepted clients: macOS T3 Desktop, iPad T3 Code, browser WebUI;
- agent activity publication: disabled;
- T3 Desktop SSH transport: retired; `/home/core/.t3/ssh-launch` cleanup completed;
- ACP providers: Codex and Antigravity;
- standalone Antigravity daemon remains separate.

## Stage 1 Live Topology: Consolidated PostgreSQL & Applications (2026-09-29)

- **Database Engine**: single shared PostgreSQL 18 container (`postgres:18`), managed under `/opt/postgres/compose.yaml`, storage `/srv/postgres`.
- **Database Network**: isolated Docker network `postgres_net` (no host port publication).
- **Database Ownership & Roles**:
  - `mattermost`: owned by `mattermost` (`NOSUPERUSER NOCREATEDB NOCREATEROLE`);
  - `nextcloud`: owned by `nextcloud` (`NOSUPERUSER NOCREATEDB NOCREATEROLE`);
  - `openproject`: owned by `openproject` (`NOSUPERUSER NOCREATEDB NOCREATEROLE`, extensions: `btree_gist`, `pg_trgm`, `unaccent`);
  - `postgres`: owned by `postgres` (superuser administrative database).
- **Application Topology**:
  - **Mattermost**: container `mattermost-mattermost-1` (`mattermost/mattermost-team-edition:latest`), external DB `postgres:5432/mattermost` via `postgres_net`, embedded DB disabled.
  - **Nextcloud**: containers `nextcloud-app-1`, `nextcloud-cron-1`, `nextcloud-redis-1`, external DB `postgres:5432/nextcloud` via `postgres_net`, storage `/srv/cloud` and `/srv/nextcloud/data`.
  - **OpenProject**: containers `openproject-web-1`, `openproject-proxy-1`, `openproject-worker-1`, `openproject-cron-1`, `openproject-cache-1`, `openproject-autoheal-1`, external DB `postgres:5432/openproject` via `postgres_net`, embedded DB and Hocuspocus disabled, collaborative editing disabled.
- **Rollback Containers (Preserved / Stopped)**:
  - `mattermost-postgres-1` (`postgres:18-alpine`, Exited (0));
  - `nextcloud-db-1` (`postgres:18-alpine`, Exited (0));
  - `openproject-db-1` (`postgres:17`, Exited (0));
  - `openproject-hocuspocus-1` (`openproject/hocuspocus:17.8.0`, Exited (0)).

## Stage 2 Live Topology: Maintenance Center & Semaphore Normalization (2026-09-29)

- **Status**: **VERIFIED / PENDING ACCEPTANCE**;
- **Ownership Policy**: native-first; Maintenance execution plane: strictly manual-only;
- **Target Model**: `update_units_v5`;
- **Actionable Manual Units**: exactly 16 (`APT_EDGE`, `XRAY`, `HYSTERIA2`, `BACKREST`, `RESTIC`, `RCLONE`, `SEMAPHORE`, `N8N`, `AUTHELIA`, `MATTERMOST`, `POSTGRESQL`, `STALWART`, `BULWARK`, `NEXTCLOUD`, `NEXTCLOUD_REDIS`, `OPENPROJECT`);
- **Master Batch Order**: 16 units dependency-ordered (`XRAY` -> `HYSTERIA2` -> `BACKREST` -> `RESTIC` -> `RCLONE` -> `N8N` -> `AUTHELIA` -> `POSTGRESQL` -> `MATTERMOST` -> `STALWART` -> `BULWARK` -> `NEXTCLOUD` -> `NEXTCLOUD_REDIS` -> `OPENPROJECT` -> `SEMAPHORE` -> `APT_EDGE`);
- **PostgreSQL Unit**: unified single unit ID `POSTGRESQL`, display `PostgreSQL`, directory `/opt/postgres`, Compose `compose.yaml`, service `postgres`, container `postgres`, image track `18`, major policy `18` (major 19+ upgrades discovery disabled);
- **OpenProject Unit**: unified logical unit ID `OPENPROJECT`, display `OpenProject`, directory `/opt/openproject`, files `docker-compose.yml` + `docker-compose.override.yml`, service `web`, branch `stable/17`, driver `openproject_compose` (dedicated helper `/opt/edge-maintenance/scripts/update-openproject`), application version `17.8.0`;
- **Removed Stale Units**: `NEXTCLOUD_POSTGRESQL` completely purged from units, master order, collector, renderer labels, contract tests, and Semaphore templates;
- **Orphan Container Safety**: unconditional `--remove-orphans` purged from generic Compose driver in `manual-update`; rollback containers (`openproject-db-1`, `openproject-hocuspocus-1`, `mattermost-postgres-1`, `nextcloud-db-1`) remain intact and protected;
- **Semaphore Templates**: template 11 (`33. Update PostgreSQL`, playbook `maintenance/edge/playbooks/updates/postgresql.yml`), template 19 updated to `Update OpenProject` (playbook `maintenance/edge/playbooks/updates/openproject.yml`);
- **Dashboard / UI**: `update.escloud.us` reflects normalized topology with 16 manual actionable targets, 23 monitored components, showing `PostgreSQL` and `OpenProject`, with zero `NOT_INSTALLED` or stale container errors;
- **Verification Gates**:
  - `POSTGRESQL_IMAGE_TRACK=18`
  - `POSTGRESQL_MAJOR_UPGRADE_DISCOVERY=DISABLED`
  - `EDGE_MAINTENANCE_CONTRACT=PASS`
  - `EDGE_MASTER_CONTRACT=PASS`
  - `MASTER_HEALTH_GATE=PASS`
  - 16/16 `manual-update <TARGET> --preflight` returned `PASS` with `REAL_UPDATE_EXECUTED=NO`
  - `READ_ONLY_REFRESH=PASS`


### Shared PostgreSQL 18 production topology (accepted 2026-09-29)

- Production database service: Docker container `postgres`, image track `postgres:18`, persistent data `/srv/postgres`, no host-published 5432.
- Databases: `mattermost`, `nextcloud`, `openproject` with separate roles.
- Backrest `edge-state` preparation creates logical dumps for all three databases plus PostgreSQL globals and stages OpenProject `openproject_opdata`; OpenProject restart is guarded by readiness wait.
- Edge Monitor current Docker contract: 15 persistent production containers, including shared `postgres` and the OpenProject web/worker/cron/cache/proxy/autoheal services.
- Retired from runtime: `mattermost-postgres-1`, `nextcloud-db-1`, `openproject-db-1`, `openproject-hocuspocus-1`, their superseded database data/volume, migration rollback files, and obsolete `postgres:17`, `postgres:18-alpine`, `openproject/hocuspocus:17.8.0` images.


### Final normalized edge runtime inventory (accepted 2026-09-29)

- Docker steady state: 15 running production containers, 12 active images, 1 persistent local volume (`openproject_opdata`), 0 stopped containers, 0 dangling images, 0 dangling volumes, 0 build cache.
- OpenProject Maintenance helper: `/opt/edge-maintenance/scripts/update-openproject`; retired rollback-container requirements removed; current preflight PASS.
- NetBird normalized local integration:
  - `/etc/systemd/system/netbird.service.d/90-restart-policy.conf`
  - `/etc/systemd/system/netbird.service.d/95-wt0-prestart.conf`
  - `/usr/local/sbin/netbird-wt0-prestart`
- Nginx normalized active configs:
  - `/etc/nginx/sites-available/maintenance-internal.conf` with enabled symlink
  - `/etc/nginx/sites-available/escloud-us.conf` with enabled symlink
- T3 retained runtime generations:
  - `0.0.43-nightly.20260923.2150` (service launcher reference)
  - `0.0.43-nightly.20260928.2402` (native runtime state reference)
  - `0.0.43-nightly.20260929.2428` (current serve/runtime processes)
- Codex: current standalone release `0.159.0-x86_64-unknown-linux-musl` only; native managed remote-control app-server/updater recovered; zombie count 0.
- Hermes: default-only clean-sheet; one dependency environment after native PM GC; no `bootstrap/selflearning.json`; no `refs/hermes-update-backups/*`.
- Retired/absent residual paths include `/srv/mattermost/backups`, `/home/core/Documents`, `/home/core/.config/google-chrome-for-testing-headless`, and `/var/www/html`.
- Resource state: root filesystem 42G used / 113G available (27%); `/tmp` 3.4M used of 7.8G.


---

## 2026-09-30 — OpenProject Native GitHub Integration Assets

- OpenProject project: `Cloud Infrastructure` (identifier `cloud-infrastructure`), private/active, modules `github` + `work_package_tracking`.
- OpenProject integration actor: `github-integration`, active non-admin.
- OpenProject project role: `GitHub Integration`; requested permissions `view_work_packages` + `add_work_package_comments` plus upstream-added public project permissions.
- OpenProject API token: one token named `GitHub Webhook` assigned to `github-integration`; secret value intentionally not recorded.
- OpenProject GitHub webhook signature secret: configured; secret value intentionally not recorded.
- GitHub repository integration: `Eugene-SN/Cloud-Infrastructure`.
- GitHub repository webhook id: `689080899`; active; content type `application/json`; events `*` / “Send me everything”.
- Webhook endpoint base: `https://projects.escloud.us/webhooks/github`; authenticated with OpenProject API-token `key` query parameter and GitHub `X-Hub-Signature-256` secret validation.
- Native cache lifecycle: orphaned `GithubPullRequest` rows are cleaned by `Cron::ClearOldPullRequestsJob`; `GithubUser` lookup rows persist normally.
- Sample project `your-scrum-project` retired; `demo-project` retained.

---

## 2026-09-30 — OpenProject Outbound SMTP Integration Assets

- Sender mailbox: `openproject@escloud.us` in Stalwart.
- SMTP endpoint: `mail.escloud.us:465`.
- Transport: implicit TLS; certificate verification mode `peer`.
- Authentication: SMTP AUTH `plain`.
- OpenProject mail-from identity: `OpenProject <openproject@escloud.us>`.
- OpenProject SMTP local persistence: `/opt/openproject/.env` plus `/opt/openproject/docker-compose.override.yml`.
- SMTP credential is local-only and intentionally not recorded in the canonical repository.
- OpenProject SMTP consumers: `openproject-web-1`, `openproject-worker-1`, `openproject-cron-1`.
- Stalwart submission listener remains existing TCP/465; TCP/587 is not required for OpenProject.
- Temporary recovery-admin provisioning credential: absent from final runtime.
- Temporary `ghcr.io/stalwartlabs/cli:latest` provisioning image: removed after use.
- Permanent new runtime components: none.
- Inbound OpenProject mail/IMAP: deferred / not enabled.
- Acceptance marker: `OPENPROJECT_STALWART_SMTP_FINAL_ACCEPTANCE=PASS`.

---

## 2026-09-30 — OpenProject Work Package iCalendar Assets

- Project: `Cloud Infrastructure`.
- Enabled project modules: `calendar_view`, `github`, `work_package_tracking`.
- Meetings module: disabled.
- Saved calendar:
  - name `Cloud Infrastructure`;
  - query id `29`;
  - private;
  - admin-owned.
- Work Package iCalendar token:
  - token id `5`;
  - name `Apple Calendar iCloud`;
  - scoped to query id `29`.
- Subscription URL/token plaintext: intentionally not recorded.
- Feed endpoint model: native OpenProject tokenized iCalendar URL.
- Feed mode: read-only Work Package subscription.
- Feed refresh hint: `PT1H`.
- Apple Calendar/iCloud subscription: operator-confirmed active.
- Meeting iCalendar tokens for admin: 0.
- Permanent new runtime components: none.
- Acceptance marker: `OPENPROJECT_CALENDAR_ICAL_FINAL_ACCEPTANCE=PASS`.

---

## 2026-09-30 — OpenProject Docker hostname normalization

- OpenProject application/public hostname: `projects.escloud.us`.
- OpenProject Docker hostname for service `web`: `web`.
- Persistence: local `/opt/openproject/docker-compose.override.yml`.
- Purpose: prevent Docker embedded DNS from shadowing the public `projects.escloud.us` name on shared `postgres_net`.
- Nextcloud resolution after normalization: `projects.escloud.us -> 45.92.156.17`.
- Upstream tracked OpenProject Compose mutation: none.
- Acceptance marker: `OPENPROJECT_PUBLIC_FQDN_DOCKER_DNS_COLLISION_FIX=PASS`.

---

## 2026-09-30 — OpenProject ↔ Nextcloud integration — deferred / no runtime assets

- Status: `DEFERRED / CLEAN`.
- Nextcloud app `integration_openproject`: absent.
- Nextcloud integration app files/config/migrations/table/background jobs: absent.
- Nextcloud OAuth clients created for this integration: 0.
- OpenProject Nextcloud Storage objects: 0.
- OpenProject ProjectStorage links for this integration: 0.
- Nextcloud-specific OpenProject OAuth applications: absent.
- Local compatibility backports/shims: absent.
- Version pins/holds/downgrades for Nextcloud, OpenProject or the integration app: absent.
- Revisit only when a future stable `integration_openproject` release supports the deployed stable Nextcloud without local source patches.
- Independent OpenProject Docker hostname/DNS normalization remains accepted and active.
- Final marker: `OPINT4_DEFER_DB_RESIDUE_RECOVERY_AND_FINAL_ACCEPTANCE=PASS`.


---

## 2026-09-30 — Edge East-West Normalization Phase 1

- Network: `edge_internal`
  - Subnet: `172.30.0.0/24`
  - Gateway: `172.30.0.1`
  - Linux bridge name: `edge-internal`
  - Driver: `bridge`
  - External network declared in Compose configurations: `/opt/n8n/compose.yaml`, `/opt/mattermost/docker-compose.edge.yml`, `/opt/openproject/docker-compose.override.yml`.
- Container Membership:
  - `n8n`: IP `172.30.0.2`, aliases `['n8n', 'n8n', 'n8n']`, networks: `['edge_internal', 'n8n_hermes']`
  - `mattermost-mattermost-1`: IP `172.30.0.3`, aliases `['mattermost-mattermost-1', 'mattermost', 'mattermost']`, networks: `['edge_internal', 'mattermost_default', 'postgres_net']`
  - `openproject-web-1`: IP `172.30.0.5`, aliases `['openproject-web-1', 'web', 'openproject']`, networks: `['edge_internal', 'openproject_backend', 'openproject_frontend', 'postgres_net']`
  - `openproject-worker-1`: IP `172.30.0.4`, aliases `['openproject-worker-1', 'worker', 'openproject-worker']`, networks: `['edge_internal', 'openproject_backend', 'postgres_net']`
- Excluded Containers (verified NOT connected):
  - `postgres`, `nextcloud`, `openproject-cron`, `openproject-cache`, `openproject-proxy`, `openproject-autoheal`, `authelia`, `stalwart`, `bulwark`, `redis`.
- Updated Integration Endpoints:
  - `n8n` → `Mattermost`: `http://mattermost:8065` (credential `16a0a988ad514ab1`, name `Mattermost API - edge internal`)
  - `Hermes` → `Mattermost`: `http://127.0.0.1:18065` (in `/home/core/.hermes/.env`)
- Acceptance marker: `EDGE_EAST_WEST_NORMALIZATION_PHASE_1=PASS`.


---

## 2026-09-30 — OP-INT-5 — OpenProject ↔ n8n Event Ingress Integration

- OpenProject:
  - Outgoing Webhook: ID 1 (`n8n - Cloud Infrastructure`), URL `http://n8n:5678/webhook/openproject-events`, enabled: true, all_projects: false, project: `Cloud Infrastructure` (ID 4), events: `["work_package:created", "work_package:updated"]`, signature: HMAC-SHA1.
  - SSRF Allowlist: `OPENPROJECT_SSRF_PROTECTION_IP_ALLOWLIST: "172.30.0.0/24"` (defined in `/opt/openproject/docker-compose.override.yml` for `web` and `worker`).
  - Admin API Token: `n8n Integration` (user `admin`).
- n8n:
  - Active Workflow: `OpenProjectEventIngress01` (`OpenProject Event Ingress`), webhook listener at `POST /webhook/openproject-events`.
  - Credentials:
    - `OpenProjectWebhookHMAC01` (`OpenProject Webhook HMAC - edge internal`, type `crypto`): HMAC secret.
    - `OpenProjectAPI01` (`OpenProject API - edge internal`, type `httpBearerAuth`): OpenProject admin bearer token.
- Acceptance marker: `OPINT5_FINAL_ACCEPTANCE=PASS`.

## 2026-09-30 — OP-INT-6 — OpenProject Dedicated Mattermost Notification Integration

- Mattermost:
  - Bot: `openproject` (display name `OpenProject`, user ID `fc7je5jjqjfydgzjrb3nnz95gh`, active).
  - Channel: `openproject` (display name `OpenProject`, channel ID `5djtwy7c7jbpdkfxrgzbs9igna`, type `P` - private, team `es-cloud`), members: `eugene`, `openproject`.
- n8n:
  - Active Workflow: `OpenProjectMattermost01` (`OpenProject Mattermost Notifications`), sub-workflow triggered by `OpenProjectEventIngress01` via `waitForSubWorkflow=false`.
  - Credentials:
    - `OpenProjectMattermostAuth01` (`Mattermost API - OpenProject edge internal`, type `mattermostApi`): bot `openproject` API token targeting `http://mattermost:8065`.
- Acceptance marker: `OPINT6_FINAL_ACCEPTANCE=PASS`.

