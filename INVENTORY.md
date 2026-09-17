# Cloud Infrastructure — Inventory

## Inventory semantics

This inventory distinguishes live accepted runtime from future accepted/planned components and unresolved later-stage choices. Fresh runtime verification has priority over this file.

## Nodes

| Node | Role | State |
|---|---|---|
| `nl-core-vds` | Legacy external VPS identity | LEGACY-AS-IS historical only |
| `edge` / `edge.escloud.us` | Current Cloud Infrastructure VPS | LIVE; Stage 1 accepted, Stage 2 in progress |
| `ai-node` | PAI compute/data/knowledge node | Existing external dependency/context |
| PVE/Home Infrastructure | Home general-purpose infrastructure plane | Existing external dependency/context |

## Current live `edge` substrate

Accepted live foundation:

- Ubuntu 26.04.1 LTS;
- hostname `edge`, FQDN `edge.escloud.us`;
- IPv4 `45.92.156.17`, IPv6 `2a0c:b847:ffff:283::a`;
- key-only root SSH through `ssh.socket`;
- Docker Engine `29.8.1`, Compose `5.5.1`, containerd;
- nginx `1.28.3-2ubuntu1.11`;
- Xray `26.3.27`;
- Hysteria2 `2.12.3`;
- Authelia `4.39.27`;
- UFW Stage 1 listener contract: TCP 22/80/443 and UDP 443 only;
- shared application service account `core`, UID/GID `1000:1000`, locked password, no sudo/docker group.

## Stage 2 application inventory

| Component | Current status | Runtime / notes |
|---|---|---|
| n8n | LIVE / ACCEPTED | `2.39.7`; container `n8n`; `127.0.0.1:15678`; public `https://n8n.escloud.us/`; Authelia protected; state `/srv/n8n`; compose `/opt/n8n/compose.yaml` |
| Stalwart | TARGET-ACCEPTED / pending Stage 2 | mail server; restore/integration pending |
| Bulwark | TARGET-ACCEPTED / pending Stage 2 | webmail frontend; restore/integration pending |
| CloudCLI | TARGET-ACCEPTED / pending Stage 2 | cloud AI workspace/interface |
| Codex CLI | TARGET-ACCEPTED / pending Stage 2 | subscription cloud-model tooling |
| Antigravity CLI | TARGET-ACCEPTED / pending Stage 2 | accepted additional cloud AI CLI |
| Backrest | TARGET-ACCEPTED / pending Stage 2 | backup-management plane; `backup.escloud.us` allocated |
| Semaphore | TARGET-ACCEPTED / pending Stage 2 | operational execution plane; `ops.escloud.us` allocated |
| Cloud Infrastructure portal | TARGET-ACCEPTED / pending Stage 2 | `app.escloud.us`; replaces legacy Homepage |
| maintenance page | TARGET-ACCEPTED / pending Stage 2 | portal/ops integration; replaces legacy custom Maintenance Center |

### n8n accepted identities

- image ID / repo digest `sha256:54323be085a6086acd87f612a25752d6582d3a0c0b07cc93c2b40a9356c3203b`;
- compose SHA256 `42009eb90d1411b168f4ff9fd072108021a8e9b2467f5c59a01bcf4dcc5ad5bf`;
- nginx vhost SHA256 `0c9e944233fa6243cb24f10d42157457d741f401bb555c62bb744382a03ed7ae`;
- config SHA256 `a3dbdaaed5a50616b46f55bc8cd02bef592f5ba14f26f3198c0e816769f12431`;
- workflows 2, credentials 1, executions 0, webhooks 0, projects 1, active workflows 0;
- migrations 254, latest `CreateAgentWorkflowDependencyTable1788522448804`;
- credential decryptability acceptance PASS;
- no public `15678` listener.

## Domain inventory

Canonical allocation is in `DOMAIN_NAMESPACE.md`.

Current active/allocated names:

- `escloud.us` — public masking page;
- `edge.escloud.us` — infrastructure hostname;
- `auth.escloud.us` — Authelia;
- `app.escloud.us` — Stage 2 portal target;
- `n8n.escloud.us` — live accepted n8n;
- `code.escloud.us` — CloudCLI target;
- `mail.escloud.us` — Stalwart/Bulwark target;
- `backup.escloud.us` — Backrest target;
- `ops.escloud.us` — Semaphore target;
- `docs.escloud.us` — reserved technical documentation library;
- `chat.escloud.us` — reserved future service;
- `cloud.escloud.us` — reserved Stage 4 file-access layer;
- `sync.escloud.us` — reserved Stage 4 synchronization layer.

Legacy `go.escloud.us` has been removed from the target TLS/Authelia/n8n configuration and its DNS record may be deleted after the accepted migration.

## TLS / certificate inventory

Current shared `escloud.us` certificate SANs:

`escloud.us`, `app`, `auth`, `backup`, `chat`, `cloud`, `code`, `docs`, `mail`, `n8n`, `ops`, `sync.escloud.us`.

Manual certificate lifecycle state:

- `/opt/vpn-stack/state/web-domains.txt` SHA256 `cab0467df32ef5cbed2af58f0ac91624962632de84af8faf86286788ca4a7eb9`;
- `/opt/vpn-stack/scripts/maintctl` SHA256 `0e7b2b2f6b1a3b3d6563157520d15060e3c29ce64c94e147035a3beddced3257`;
- `maintctl web-check` PASS for all current SAN names;
- Certbot deploy hook synchronizes Xray/Hysteria certificate copies.

## Backup / operations direction

| Component | Future status | Notes |
|---|---|---|
| Restic | accepted underlying tool/backend | legacy same-host repository is not final DR topology |
| Backrest | TARGET-ACCEPTED | Stage 2 deployment pending |
| Homepage | DO-NOT-CARRY-AS-IS | replaced by dedicated Cloud Infrastructure portal |
| custom Maintenance Center | DO-NOT-CARRY-AS-IS | replaced by maintenance page + Semaphore |
| Semaphore | TARGET-ACCEPTED | Stage 2 deployment pending |

## File/storage/synchronization — Stage 4 unresolved

| Component | Status | Notes |
|---|---|---|
| Filestash | UNDER-REVIEW | compare against Stage 4 requirements |
| SFTPGo | UNDER-REVIEW candidate | not accepted merely from prior proposal |
| `/srv/cloud` | legacy path under review | not target path by assumption |
| Syncthing | UNDER-REVIEW | evaluate general sync, `edge ↔ ai-node`, and Obsidian separately |
| Self-hosted LiveSync / CouchDB | UNDER-REVIEW candidate | not accepted final Obsidian mechanism |
| Obsidian `edge` role | UNDER-REVIEW | canonical vault remains on `ai-node` |

## Private connectivity — Stage 6 unresolved

| Component | Status | Notes |
|---|---|---|
| NetBird | UNDER-REVIEW candidate | not accepted for `edge` merely from earlier proposal |
| WireGuard/direct tunnel alternatives | UNDER-REVIEW | choose from actual Stage 6 flows |
| Authenticated HTTPS over Home public IP | UNDER-REVIEW | compare where simpler/adequate |

## Historical / recovery artifacts

- canonical legacy baseline: `NL_CORE_VDS_Current_State_Baseline_2026-09-14.md`;
- Stage 1 local recovery archive: `/srv/backups/edge-stage1/edge-stage1-base-20260916T234611Z.tar.gz`, SHA256 `37486e763ddac4c5ef3a92a35c3dad49787d75ffd8b97499073c79af617cc566`;
- external credential-bearing migration archive remains required through Stage 2 while additional accepted services are restored.

## Current stage boundary

Stage 0 — COMPLETE / ACCEPTED.  
Stage 1 — COMPLETE / ACCEPTED.  
Stage 2 — IN PROGRESS; n8n component accepted.
