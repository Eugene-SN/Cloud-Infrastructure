# Cloud Infrastructure — Inventory

## Semantics

Fresh runtime verification outranks this file. This inventory records accepted live components, selected/deferred targets, and unresolved later-stage choices.

## Nodes

| Node | Role | State |
|---|---|---|
| `edge` / `edge.escloud.us` | Cloud Infrastructure VPS | LIVE; Stage 0/1/2 accepted; Stage 02.5 research active |
| `nl-core-vds` | historical legacy VPS identity | HISTORICAL ONLY |
| `ai-node` | PAI compute/data/knowledge node | external dependency/context; future cross-site peer and local-vLLM endpoint |
| PVE / Home Infrastructure | home infrastructure plane | external dependency/context; future cross-site peer |

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
- malformed legacy contact repaired with a new valid UID;
- legacy admin mailbox contained no useful mail data;
- outbound Gmail: delivery/SPF/RSA-DKIM/DMARC PASS;
- inbound Gmail reply: delivery/readback/SPF/DKIM/DMARC PASS.

## Domain inventory

- `escloud.us` — public masking/masquerade page;
- `edge.escloud.us` — infrastructure hostname;
- `auth.escloud.us` — live Authelia;
- `n8n.escloud.us` — live n8n;
- `code.escloud.us` — live CloudCLI;
- `mail.escloud.us` — live Stalwart + Bulwark;
- `backup.escloud.us` — future Backrest management UI;
- `ops.escloud.us` — future Semaphore operational execution UI;
- `update.escloud.us` — future dedicated custom maintenance/update page; Cloudflare record already created by the user; dedicated Codex substage after Semaphore/update backend contract exists;
- `app.escloud.us` — future final private Cloud Infrastructure portal/dashboard; dedicated Codex substage after monitoring/status sources exist;
- `docs.escloud.us` — reserved;
- `chat.escloud.us` — reserved; not automatically assigned to Hermes;
- `cloud.escloud.us` — future file-access layer; implementation unresolved;
- `sync.escloud.us` — future synchronization layer; implementation unresolved;
- `go.escloud.us` — retired.

## Stage 02.5 — active research inventory

### Remaining Standalone Core Services

Status: **RESEARCH BLOCK COMPLETE / SELECTED**.

Selected product:

| Component | Outcome | Intended role |
|---|---|---|
| Hermes Agent | `SELECTED` | persistent cloud-side agent runtime for agentic reasoning, tools and delegation; future Stage 3 |

Accepted placement/integration direction:

- host-native under `core` by default;
- Docker not preferred because it would complicate direct reuse of host-native Codex/Antigravity binaries and user/runtime context;
- n8n remains deterministic workflow/orchestration plane;
- Hermes remains agentic reasoning/delegation plane;
- CloudCLI/Codex/Antigravity remain manually usable tools/executors;
- Stage 3 verifies `n8n -> Hermes -> Codex/AGY -> Hermes -> n8n` at infrastructure level;
- Hermes -> local vLLM on `ai-node` is deferred until Stage 4 cross-site connectivity is accepted;
- no public Hermes domain/listener is assumed.

Other previously considered standalone candidates are not part of Stage 3. Notification brokers remain a later monitoring/alerts decision; password/2FA remains optional; feed/change-detection/search/capture products remain workflow-layer decisions unless a later concrete requirement proves a dedicated service necessary.

### Cross-site Connectivity Foundation

Status: **UNRESOLVED / CURRENT NEXT RESEARCH BLOCK**.

- real `edge ↔ ai-node ↔ PVE/Home` flows must be defined first;
- NetBird is candidate only;
- direct WireGuard is candidate only;
- authenticated HTTPS/public mechanisms remain valid candidates where simpler;
- final transport/topology must be driven by actual required flows and real connectivity conditions;
- accepted connectivity will also enable Hermes to use the local vLLM endpoint on `ai-node`.

### Cross-site Data & Knowledge Services

Status: **UNRESOLVED / DEPENDS ON CONNECTIVITY**.

- VPS working storage and web file management;
- MacBook/iPhone/iPad/`ai-node` file access;
- Filestash — candidate only;
- SFTPGo — candidate only;
- Syncthing — under review by use case;
- selected-directory synchronization — unresolved;
- Self-hosted LiveSync/CouchDB — candidate only for Obsidian;
- other current free/self-hosted Obsidian mechanisms must be researched;
- canonical Obsidian vault remains `/srv/ai-data/knowledge/obsidian` on `ai-node`;
- `edge` role for Obsidian remains to be selected.

## Planned deployment stage inventory

| Stage | Scope | Current status |
|---|---|---|
| 3 | Hermes Agent Runtime | PRODUCT/ROLE/PLACEMENT SELECTED; deployment blocked by Stage 02.5 completion |
| 4 | Cross-site Connectivity Foundation | RESEARCH REQUIRED |
| 5 | Cross-site Data & Knowledge Services | DEPENDS ON Stage 4; RESEARCH REQUIRED |
| 6 | Remaining Infrastructure Services | CONDITIONAL; remove/renumber if no service is selected |
| 7 | Backrest & Recovery | PRODUCT DIRECTION ACCEPTED; topology research pending |
| 8 | Maintenance & Update: Semaphore + update workflow + Codex `update.escloud.us` substage | PRODUCT ACCEPTED / DEPLOYMENT DEFERRED until Stage 7 restore acceptance |
| 9 | Monitoring, Heartbeats & Alerts | REQUIRED / PRODUCT UNRESOLVED; deploy after stable inventory/lifecycle layers |
| 10 | Cloud Portal: `app.escloud.us` | CAPABILITY ACCEPTED / separate Codex substage after Stage 9 |
| 11 | Final Integrated Infrastructure Acceptance | REQUIRED / FINAL GATE |

## Post-infrastructure application/workflow layer

This is a continuous workstream after Stage 11, not an infrastructure-completion stage:

- n8n workflows;
- Hermes/agent workflows;
- Universal Capture Inbox — low-friction submission of URLs/text/files/images/commands into workflows;
- human-in-the-loop approvals — explicit approve/reject/choice gates in workflows;
- mail-triggered automation;
- continuous information intake/change detection workflows;
- bounded AI research jobs;
- durable application-level store-and-forward/retry for actual cross-site tasks;
- optional messaging/bot command frontend;
- user-specific orchestration among n8n, Hermes, Codex CLI, Antigravity CLI and local vLLM/PAI.

## Optional capabilities still requiring disposition

- password/2FA vault;
- limited failover/secondary-endpoint role;
- additional messaging/control frontend only if it adds value beyond the chosen workflow interaction surfaces.

## Recovery artifacts

- historical baseline: `NL_CORE_VDS_Current_State_Baseline_2026-09-14.md`;
- Stage 1 recovery archive `/srv/backups/edge-stage1/edge-stage1-base-20260916T234611Z.tar.gz`, SHA256 `37486e763ddac4c5ef3a92a35c3dad49787d75ffd8b97499073c79af617cc566`;
- authoritative migration-preservation archive `/tmp/edge-migration-preservation-20260916T141048Z.tar.gz`, SHA256 `0203e5845f57bc1d04b384cef2b26a45fbff855c341e1edf1193034c34de9fdf`, retained for later legacy-reference work.

## Stage boundary

Stage 0 — COMPLETE / ACCEPTED.  
Stage 1 — COMPLETE / ACCEPTED.  
Stage 2 — COMPLETE / ACCEPTED.  
Stage 02.5 — ACTIVE / RESEARCH-ONLY.

The old thematic Stage 3–7 grouping is no longer authoritative. Stage 3 Hermes composition is accepted; later stages follow the dependency-aware roadmap above and remain subject to the remaining Stage 02.5 research.