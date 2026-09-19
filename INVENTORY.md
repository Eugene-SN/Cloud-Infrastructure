# Cloud Infrastructure — Inventory

## Semantics

Fresh runtime verification outranks this file. This inventory records accepted live components, selected/deferred targets, external dependencies and unresolved later-stage choices.

## Nodes

| Node | Role | State |
|---|---|---|
| `edge` / `edge.escloud.us` | Cloud Infrastructure VPS | LIVE; Stage 0–4 accepted; Stage 05.1 accepted; edge deployment planned for 05.3 |
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

- NetBird `0.78.2` host-native on `edge`;
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

## Stage 2 — COMPLETE / ACCEPTED

`EDGE_STAGE2_FINAL_INTEGRATED_ACCEPTANCE=PASS` on 2026-09-17.

| Component | State | Runtime / notes |
|---|---|---|
| Authelia | LIVE / ACCEPTED | `4.39.27`; `127.0.0.1:19091`; fresh operator/auth secrets; `auth.escloud.us` |
| n8n | LIVE / ACCEPTED | `2.39.7`; `127.0.0.1:15678`; fresh one-owner state; `n8n.escloud.us`; Authelia protected |
| CloudCLI | LIVE / ACCEPTED | `1.37.3`; systemd; `127.0.0.1:18140`; fresh local user; `code.escloud.us`; Authelia protected |
| Codex CLI | LIVE / ACCEPTED | `0.154.0`; official standalone; fresh ChatGPT auth; managed Remote Control via Unix socket |
| Antigravity CLI | LIVE / ACCEPTED | current `1.2.7`; Stage 4G accepted `1.2.6`; Stage 2/4B historical `1.2.5`; Google OAuth; instance `edge`; persistent user service |
| Stalwart | LIVE / ACCEPTED | `0.16.22`; public SMTP25/SMTPS465/IMAPS993; useful mail data migrated; fresh auth/DKIM |
| Bulwark | LIVE / ACCEPTED | `1.9.2`; `127.0.0.1:18084`; fresh session/admin state; default webmail route on `mail.escloud.us` |

### Accepted identities / hashes

- Authelia compose SHA256 `265dc881294e4b14bf9da5b529570ff6a2f234de2a3e335681d34d3deb447e96`;
- n8n compose SHA256 `03f6e88c137dedf5c5ed5cb8481c097bc2ab322e612c745f636a8fcc9117dda0`;
- CloudCLI systemd unit SHA256 `8bf303e000b3de0f5a761fc0a466139a75e72fd6ec5d07b08ab7cb82f95382af`;
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
- `code.escloud.us` — live CloudCLI;
- `mail.escloud.us` — live Stalwart + Bulwark;
- `backup.escloud.us` — future Backrest management UI;
- `ops.escloud.us` — future Semaphore operational execution UI;
- `update.escloud.us` — future dedicated custom maintenance/update page; Cloudflare record already exists; dedicated Codex substage after backend contract;
- `app.escloud.us` — future final Cloud Infrastructure portal/dashboard; dedicated Codex substage after monitoring/status sources;
- `docs.escloud.us` — reserved;
- `hermes.escloud.us` — LIVE accepted Hermes Dashboard/Remote Gateway; native self-hosted OIDC through Authelia; backend loopback-only;
- `chat.escloud.us` — LIVE Mattermost human endpoint; core runtime and public nginx ingress accepted; native Mattermost authentication without Authelia;
- `cloud.escloud.us` — future file-access layer; implementation unresolved;
- `sync.escloud.us` — future synchronization layer; implementation unresolved;
- `go.escloud.us` — retired.

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
- CloudCLI/Codex/Antigravity remain manually usable tools/executors;
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
| 6 | Backrest & Recovery | PRODUCT DIRECTION ACCEPTED; topology research pending |
| 7 | Maintenance & Update | Semaphore accepted; deploy only after Stage 6 restore acceptance |
| 8 | Monitoring, Heartbeats & Alerts | REQUIRED / PRODUCT UNRESOLVED |
| 9 | Cloud Portal: `app.escloud.us` | CAPABILITY ACCEPTED / dedicated Codex substage |
| 10 | Final Integrated Infrastructure Acceptance | REQUIRED / FINAL GATE |

## Post-infrastructure application/workflow layer

Continuous workstream after Stage 10, not an infrastructure-completion stage:

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
- n8n workflow `Hermes Machine Invocation`, ID `Hermes4FMachine01`, active/published;
- n8n encrypted Bearer credential `Hermes4FAuth01`;
- selector values: `vllm`, `codex`, `antigravity`;
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

`EDGE_STAGE3_FINAL_INTEGRATED_ACCEPTANCE=PASS`. Final Stage 3 record: `STAGE_03_ACCEPTANCE_2026-09-18.md`. Stage 4 — Edge Hermes Agent Runtime is COMPLETE / ACCEPTED with `STAGE4_FINAL_ACCEPTANCE=PASS`; final record: `STAGE_04_FINAL_ACCEPTANCE_2026-09-18.md`.
