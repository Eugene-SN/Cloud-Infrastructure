# Cloud Infrastructure — Inventory

## Semantics

Fresh runtime verification outranks this file. This inventory records accepted live components, selected/deferred targets, external dependencies and unresolved later-stage choices.

## Nodes

| Node | Role | State |
|---|---|---|
| `edge` / `edge.escloud.us` | Cloud Infrastructure VPS | LIVE; Stage 0/1/2 accepted; Stage 02.5 research active |
| `nl-core-vds` | historical legacy VPS identity | HISTORICAL ONLY |
| `ai-node` | PAI compute/data/knowledge node | external dependency/context; Stage 3 private target; Stage 4 local-vLLM endpoint |
| PVE / Home Infrastructure | home infrastructure plane | external dependency/context; Stage 3 private routed fabric |
| CT300 `remote-access` | Home self-hosted NetBird control/routing plane | EXISTING / REUSE IN Stage 3 |
| VM100 `gateway-core` | Home VRRP/Mihomo gateway | EXISTING / routing participant for Home→NetBird account path |
| MikroTik | Home physical router / VRRP backup | EXISTING / routing participant and fallback |

## Live `edge` substrate

- Ubuntu 26.04.1 LTS, kernel `7.0.0-31-generic`;
- IPv4 `45.92.156.17`, IPv6 `2a0c:b847:ffff:283::a`;
- Docker `29.8.1`, Compose `5.5.1`, containerd;
- nginx `1.28.3-2ubuntu1.11`;
- Xray `26.3.27`;
- Hysteria2 `2.12.3`;
- Authelia `4.39.27`;
- service account `core` UID/GID `1000:1000`, locked password, no sudo/docker group;
- UFW intentional ingress: TCP 22/80/443/25/465/993 and UDP 443;
- WebUI application backends are loopback-only by default.

## Stage 2 — COMPLETE / ACCEPTED

`EDGE_STAGE2_FINAL_INTEGRATED_ACCEPTANCE=PASS` on 2026-09-17.

| Component | State | Runtime / notes |
|---|---|---|
| Authelia | LIVE / ACCEPTED | `4.39.27`; `127.0.0.1:19091`; fresh operator/auth secrets; `auth.escloud.us` |
| n8n | LIVE / ACCEPTED | `2.39.7`; `127.0.0.1:15678`; fresh one-owner state; `n8n.escloud.us`; Authelia protected |
| CloudCLI | LIVE / ACCEPTED | `1.37.3`; systemd; `127.0.0.1:18140`; fresh local user; `code.escloud.us`; Authelia protected |
| Codex CLI | LIVE / ACCEPTED | `0.154.0`; official standalone; fresh ChatGPT auth; managed Remote Control via Unix socket |
| Antigravity CLI | LIVE / ACCEPTED | `1.2.5`; fresh Google OAuth; instance `edge`; persistent user service, Online confirmed |
| Stalwart | LIVE / ACCEPTED | `0.16.22`; public SMTP25/SMTPS465/IMAPS993; useful mail data migrated; fresh auth/DKIM |
| Bulwark | LIVE / ACCEPTED | `1.9.2`; `127.0.0.1:18084`; fresh session/admin state; default webmail route on `mail.escloud.us` |

### Accepted identities / hashes

- Authelia compose SHA256 `265dc881294e4b14bf9da5b529570ff6a2f234de2a3e335681d34d3deb447e96`;
- n8n compose SHA256 `42009eb90d1411b168f4ff9fd072108021a8e9b2467f5c59a01bcf4dcc5ad5bf`;
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
- `chat.escloud.us` — reserved; not automatically assigned to Hermes;
- `cloud.escloud.us` — future file-access layer; implementation unresolved;
- `sync.escloud.us` — future synchronization layer; implementation unresolved;
- `go.escloud.us` — retired.

### Private `.lan`

- existing Home `.lan` namespace is accepted for NetBird split-DNS reuse on `edge`;
- `edge.lan` is planned only after Stage 3 enrollment/routing acceptance, through the existing canonical Home DNS mechanism;
- `.lan` does not replace public `*.escloud.us` service naming.

# Stage 02.5 — active research inventory

## Remaining Standalone Core Services

Status: **RESEARCH BLOCK COMPLETE / SELECTED**.

| Component | Outcome | Intended role |
|---|---|---|
| Hermes Agent | `SELECTED` | persistent cloud-side agent runtime for agentic reasoning, tools and delegation; future Stage 4 |

Accepted placement/integration direction:

- host-native under `core` by default;
- n8n remains deterministic workflow/orchestration plane;
- Hermes remains agentic reasoning/delegation plane;
- CloudCLI/Codex/Antigravity remain manually usable tools/executors;
- Stage 4 verifies `n8n -> Hermes -> Codex/AGY -> Hermes -> n8n`;
- Stage 4 also verifies real `Hermes -> vLLM on ai-node` through the Stage 3 private fabric;
- no public Hermes domain/listener is assumed.

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

Accepted Stage 3 target:

- host-native NetBird peer on `edge`;
- dedicated Cloud service-peer group/policy;
- Home LAN access for `edge`, no Home Internet Exit;
- provider-local `edge` default Internet route unchanged;
- Home/PAI clientless routing to `edge` via `100.105.0.0/16 -> CT300 192.168.1.90` on VM100 and MikroTik;
- narrow VM100 forwarding rule only;
- reuse existing NetBird-managed Site-to-VPN masquerade;
- reuse `.lan` split DNS and later add `edge.lan`;
- direct/relay, reboot, public-service non-regression and controlled VRRP acceptance.

Detailed record: `STAGE_02_5_CONNECTIVITY_SELECTION_ACCEPTANCE_2026-09-17.md`.

## Cross-site Data & Knowledge Services

Status: **CURRENT NEXT RESEARCH BLOCK**.

Unresolved:

- VPS working storage and web file management;
- MacBook/iPhone/iPad/`ai-node` file access;
- Filestash — candidate only;
- SFTPGo — candidate only;
- Syncthing — under review by use case;
- selected-directory synchronization;
- Self-hosted LiveSync/CouchDB — candidate only for Obsidian;
- other current free/self-hosted Obsidian mechanisms;
- exact `edge` Obsidian role.

Canonical Obsidian vault remains `/srv/ai-data/knowledge/obsidian` on `ai-node`.

# Planned deployment stage inventory

| Stage | Scope | Current status |
|---|---|---|
| 3 | Cross-site Connectivity Foundation | MECHANISM/ARCHITECTURE SELECTED; deployment blocked by Stage 02.5 completion |
| 4 | Hermes Agent Runtime | PRODUCT/ROLE/PLACEMENT SELECTED; depends on Stage 3; must include local-vLLM acceptance |
| 5 | Cross-site Data & Knowledge Services | RESEARCH REQUIRED; depends on Stage 3 connectivity |
| 6 | Remaining Infrastructure Services | CONDITIONAL; remove/renumber if no service is selected |
| 7 | Backrest & Recovery | PRODUCT DIRECTION ACCEPTED; topology research pending |
| 8 | Maintenance & Update: Semaphore + update workflow + Codex `update.escloud.us` substage | PRODUCT ACCEPTED / DEPLOYMENT DEFERRED until Stage 7 restore acceptance |
| 9 | Monitoring, Heartbeats & Alerts | REQUIRED / PRODUCT UNRESOLVED; deploy after stable inventory/lifecycle layers |
| 10 | Cloud Portal: `app.escloud.us` | CAPABILITY ACCEPTED / separate Codex substage after Stage 9 |
| 11 | Final Integrated Infrastructure Acceptance | REQUIRED / FINAL GATE |

## Post-infrastructure application/workflow layer

Continuous workstream after Stage 11, not an infrastructure-completion stage:

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
- authoritative migration-preservation archive `/tmp/edge-migration-preservation-20260916T141048Z.tar.gz`, SHA256 `0203e5845f57bc1d04b384cef2b26a45fbff855c341e1edf1193034c34de9fdf`, retained for later legacy-reference work.

## Stage boundary

Stage 0 — COMPLETE / ACCEPTED.  
Stage 1 — COMPLETE / ACCEPTED.  
Stage 2 — COMPLETE / ACCEPTED.  
Stage 02.5 — ACTIVE / RESEARCH-ONLY.

Cross-site Connectivity Foundation selection is complete. The next Stage 02.5 research block is Cross-site Data & Knowledge Services.