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

- Ubuntu 26.04.1 LTS;
- hostname `edge`, FQDN `edge.escloud.us`;
- IPv4 `45.92.156.17`, IPv6 `2a0c:b847:ffff:283::a`;
- key-only root SSH through `ssh.socket`;
- Docker Engine `29.8.1`, Compose `5.5.1`, containerd;
- nginx `1.28.3-2ubuntu1.11`;
- Xray `26.3.27`;
- Hysteria2 `2.12.3`;
- Authelia `4.39.27`;
- UFW listener contract: Stage 1 TCP 22/80/443 and UDP 443 plus Stage 2 mail TCP 25/465/993; Docker mail publication is IPv4-only;
- shared service account `core`, UID/GID `1000:1000`, locked password, no sudo/docker group;
- `core` linger enabled for persistent headless Antigravity systemd user service; `user@1000.service` active and `/run/user/1000/bus` present at acceptance.

## Stage 2 credential migration rule

- Every service receives fresh authentication credentials.
- Legacy password hashes, passwords, API/OAuth/session tokens and application auth state are not restored into production.
- Mail is the only planned data/settings preservation exception: preserve useful account/mailbox identity, addresses/aliases, messages/settings/state as required, while still creating new mail-user/admin authentication credentials.
- Migration archive remains reference/recovery material, not a source of production credentials.

## Stage 2 application inventory

| Component | Current status | Runtime / notes |
|---|---|---|
| Authelia | LIVE / ACCEPTED | `4.39.27`; container `authelia`; `127.0.0.1:19091`; fresh operator account/secrets/storage; public `auth.escloud.us` |
| n8n | LIVE / ACCEPTED | `2.39.7`; clean state; one new owner; `127.0.0.1:15678`; public `https://n8n.escloud.us/`; Authelia protected |
| CloudCLI | LIVE / ACCEPTED | `1.37.3`; systemd `cloudcli.service`; one new local user; `127.0.0.1:18140`; public `https://code.escloud.us/`; Authelia protected |
| Codex CLI | LIVE / ACCEPTED | `0.154.0`; official standalone runtime; fresh ChatGPT auth; managed app-server Remote Control enabled and server-side accepted |
| Antigravity CLI | LIVE / ACCEPTED | `1.2.5`; fresh Google OAuth; instance `edge`; `antigravity-cli-daemon.service` enabled/running under `core`; headless Remote Control registered/running; user confirmed `edge` Online in UI |
| Stalwart | LIVE / ACCEPTED | `0.16.22`; fresh production credentials/keys; public SMTP 25, SMTPS 465, IMAPS 993; useful legacy user data migrated and E2E accepted |
| Bulwark | LIVE / ACCEPTED | `1.9.2`; fresh session/admin state; `127.0.0.1:18084`; public default webmail route on `mail.escloud.us` |
| Backrest | TARGET-ACCEPTED / pending Stage 2 | `backup.escloud.us` allocated; clean deployment/credentials |
| Semaphore | TARGET-ACCEPTED / pending Stage 2 | `ops.escloud.us` allocated; clean deployment/credentials |
| Cloud Infrastructure portal | TARGET-ACCEPTED / pending Stage 2 | `app.escloud.us`; replaces legacy Homepage |
| maintenance page | TARGET-ACCEPTED / pending Stage 2 | portal/ops integration; replaces legacy custom Maintenance Center |

### Authelia accepted identities

- compose `/opt/authelia/compose.yaml`, SHA256 `265dc881294e4b14bf9da5b529570ff6a2f234de2a3e335681d34d3deb447e96`;
- config SHA256 `4c5343de85783bb0ed4973722f36df73c550708b7ffc48b2292f95aef6d62574`;
- current user DB SHA256 `7d3407a469ca5755056e60508b553511f5792e114640c69ea3e60062a81daff9`;
- clean storage DB SHA256 at reinit acceptance `d06edef4c052839e25f0b2cb79f12e1350ba4ce14b6cdf9cf5ec78691081ae0d`;
- operator `eugene`, new Argon2id password hash;
- JWT/session/storage secrets regenerated; legacy sessions/TOTP/WebAuthn/preferences removed.

### n8n accepted identities

- image ID/repo digest `sha256:54323be085a6086acd87f612a25752d6582d3a0c0b07cc93c2b40a9356c3203b`;
- compose SHA256 `42009eb90d1411b168f4ff9fd072108021a8e9b2467f5c59a01bcf4dcc5ad5bf`;
- nginx vhost SHA256 `0c9e944233fa6243cb24f10d42157457d741f401bb555c62bb744382a03ed7ae`;
- config SHA256 `48887ced0df600f4b20f93062414fa585448cda2c9c1b89176a1ecb5ea89b11f`;
- DB SHA256 `b7e3a41780dbcb65d214fca4484ad68910c5e34649c368507dd77c08af89d0c4`;
- fresh encryption-key SHA256 `be3df4bce01e664d188d2be5d781e52fe8d923eeb2b98b387b56b92f5ae6c284`;
- users `1` new owner; workflows `0`; credentials `0`; executions `0`; webhooks `0`;
- no public `15678` listener;
- retained temporary recovery artifact removed after clean acceptance.

### CloudCLI accepted identities

- version `1.37.3`;
- systemd unit `/etc/systemd/system/cloudcli.service`, SHA256 `8bf303e000b3de0f5a761fc0a466139a75e72fd6ec5d07b08ab7cb82f95382af`;
- workspace `/srv/ai-workspace`, `core:core`, mode `0750`;
- state DB `/home/core/.cloudcli/auth.db`, current SHA256 `8ae972e3e0183ed9f17f7138d9e63cfa169be043f7345f29ce6857cee72874a8`;
- nginx vhost `/etc/nginx/sites-available/code-escloud-us.conf`, SHA256 `6e6bd9f82fa9ea0f8bc576b6e4d71fcf583abef4b748c6326a7a2a7ca8de1896`;
- users `1` with new password hash; projects `0`; sessions `0`; `user_credentials` `0`;
- backend `127.0.0.1:18140` only; no public listener.

### Cloud AI CLI accepted identities

- Node `22.22.1`, npm `9.2.0`;
- Codex CLI `0.154.0` uses the official standalone install, not npm `@openai/codex`;
- launcher `/home/core/.local/bin/codex` -> `/home/core/.codex/packages/standalone/current/bin/codex`;
- fresh ChatGPT device authorization accepted and preserved across reinstall; auth object `/home/core/.codex/auth.json`, `core:core`, mode `0600`;
- Codex managed app-server backend `pid`, auto-update enabled, Remote Control enabled;
- Codex app-server/control runtime version `0.154.0` matches CLI;
- Codex control socket `/home/core/.codex/app-server-control/app-server-control.sock`, `core:core`, mode `0600`;
- Codex active managed processes: app-server with `--remote-control --listen unix://` and daemon `pid-update-loop`;
- no public Codex/app-server network listener;
- user configured Codex Remote Control pairing on iPhone, MacBook and iPad; server-side acceptance PASS; client-originated end-to-end remote task acceptance not separately recorded yet;
- Antigravity CLI `1.2.5`, `/home/core/.local/bin/agy`; fresh Google OAuth accepted;
- Antigravity state root `/home/core/.gemini/antigravity-cli`; OAuth credential contents are not documented;
- Antigravity Remote Control instance name `edge`;
- user unit `/home/core/.config/systemd/user/antigravity-cli-daemon.service` enabled and active/running;
- active daemon `/home/core/.local/bin/agy remote-control serve`;
- `core` linger enabled; `user@1000.service` active; `/run/user/1000/bus` present;
- `agy remote-control status` reports `Daemon status: active` and instance name `edge`;
- authenticated Antigravity post-activation probe returned `ANTIGRAVITY_REMOTE_AUTH_OK`, RC `0`;
- user confirmed `edge` appears Online in Antigravity Remote Control Instances;
- Codex login and managed daemon remained healthy after Antigravity Remote Control activation;
- legacy custom `codex-app-server` and `codex-runner` are absent; official Codex managed daemon supersedes their function.

### Mail accepted production inventory

- Stalwart `0.16.22`, image `stalwartlabs/stalwart:v0.16`, digest `sha256:388dcb75a70727c5b551249a6d34b1f1321294852489e4fa3a4e6be698b7c4f0`;
- Bulwark `1.9.2`, image `ghcr.io/bulwarkmail/webmail:1.9.2`, digest `sha256:0e8d1339277033b6569a76c6f8192396e6edd66fd917d64d9ed505e8b81dac6d`;
- compose `/opt/mail-stack/compose.yaml`, SHA256 `7de766ed23fd7c30f63870f25af648f018d3295685fb58e40b88eaa578d2d4de`;
- nginx vhost `/etc/nginx/sites-available/mail-escloud-us.conf`, SHA256 `601ff1feffcef8729901b1e00ab98001934db03a1315b55233965ba5d75f079c`;
- Stalwart state `/srv/mail/stalwart/etc`, `/srv/mail/stalwart/lib`; Bulwark state `/srv/mail/bulwark/{settings,admin,admin-state,telemetry}`;
- loopback web backends: Stalwart `127.0.0.1:18083 -> 8080`, Bulwark `127.0.0.1:18084 -> 3000`;
- split-route contract: default webmail routes to Bulwark; Stalwart management/JMAP routes remain on Stalwart;
- public protocol listeners: IPv4 TCP/25 SMTP, TCP/465 SMTPS submission, TCP/993 IMAPS; TCP/587, TCP/995 and TCP/4190 remain unpublished;
- fresh mail user/admin credentials, fresh Bulwark session secret/admin state, fresh DKIM key material; no legacy authentication/session/key material reused;
- `es@escloud.us` useful source data migrated: 6 mailboxes, 14 emails, address-book/calendar/identity state; malformed legacy contact reconstructed with a new valid UID while preserving its useful fields and Trusted Senders relationship;
- legacy `admin@escloud.us` direct audit found 0 messages and only default/automatic state; no useful admin data required migration;
- MX `10 mail.escloud.us.`, A `45.92.156.17`, PTR `mail.escloud.us`, SPF `v=spf1 ip4:45.92.156.17 -all`, DMARC `v=DMARC1; p=none; adkim=s; aspf=s`;
- active DKIM selectors: `v1-rsa-20260917` and `v1-ed25519-20260917`; legacy `v1-rsa-20260713` retired after E2E acceptance;
- external Gmail outbound test: delivery PASS, SPF PASS, RSA DKIM PASS using `v1-rsa-20260917`, DMARC PASS; Gmail reported the parallel Ed25519 signature neutral/no-key without affecting RSA/DMARC acceptance;
- external Gmail inbound reply: delivery PASS through SMTP/25, readback PASS through IMAPS/993; Stalwart recorded Gmail SPF/DKIM/DMARC PASS and reply references matched the exact outbound test message;
- temporary Vandelay capture `/tmp/stalwart-vandelay-capture` removed after final acceptance;
- migration-preservation archive `/tmp/edge-migration-preservation-20260916T141048Z.tar.gz`, SHA256 `0203e5845f57bc1d04b384cef2b26a45fbff855c341e1edf1193034c34de9fdf`, intentionally retained through the remainder of Stage 2 for still-pending legacy-reference work.

## Domain inventory

Canonical allocation is in `DOMAIN_NAMESPACE.md`.

Current active/allocated names:

- `escloud.us` — public masking page;
- `edge.escloud.us` — infrastructure hostname;
- `auth.escloud.us` — live Authelia;
- `app.escloud.us` — Stage 2 portal target;
- `n8n.escloud.us` — live accepted n8n;
- `code.escloud.us` — live accepted CloudCLI;
- `mail.escloud.us` — live accepted Stalwart/Bulwark mail stack;
- `backup.escloud.us` — Backrest target;
- `ops.escloud.us` — Semaphore target;
- `docs.escloud.us` — reserved technical documentation library;
- `chat.escloud.us` — reserved future service;
- `cloud.escloud.us` — reserved Stage 4 file-access layer;
- `sync.escloud.us` — reserved Stage 4 synchronization layer.

Legacy `go.escloud.us` is retired from target TLS/Authelia/n8n configuration.

## TLS / certificate inventory

Current shared SANs: `escloud.us`, `app`, `auth`, `backup`, `chat`, `cloud`, `code`, `docs`, `mail`, `n8n`, `ops`, `sync.escloud.us`.

- `/opt/vpn-stack/state/web-domains.txt` SHA256 `cab0467df32ef5cbed2af58f0ac91624962632de84af8faf86286788ca4a7eb9`;
- `/opt/vpn-stack/scripts/maintctl` SHA256 `0e7b2b2f6b1a3b3d6563157520d15060e3c29ce64c94e147035a3beddced3257`;
- `maintctl web-check` PASS for current SAN names;
- Certbot deploy hook synchronizes Xray/Hysteria/Stalwart certificate copies;
- mail TLS acceptance fingerprint `3D:5A:77:15:78:4C:53:74:4B:D7:C2:6C:86:96:5B:10:DB:F9:7B:32:45:9A:F0:CD:B9:BD:39:A1:8B:9B:9B:F8`.

## Backup / operations direction

| Component | Future status | Notes |
|---|---|---|
| Restic | accepted underlying tool/backend | legacy same-host repository is not final DR topology |
| Backrest | TARGET-ACCEPTED | Stage 2 clean deployment pending |
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
- Stage 1 recovery archive: `/srv/backups/edge-stage1/edge-stage1-base-20260916T234611Z.tar.gz`, SHA256 `37486e763ddac4c5ef3a92a35c3dad49787d75ffd8b97499073c79af617cc566`;
- external migration-preservation archive `/tmp/edge-migration-preservation-20260916T141048Z.tar.gz`, SHA256 `0203e5845f57bc1d04b384cef2b26a45fbff855c341e1edf1193034c34de9fdf`, remains required through the remainder of Stage 2 for still-pending legacy-derived configuration/reference work; do not restore credentials from it;
- temporary Vandelay archive and extracted binaries were removed after mail migration acceptance.

## Current stage boundary

Stage 0 — COMPLETE / ACCEPTED.  
Stage 1 — COMPLETE / ACCEPTED.  
Stage 2 — IN PROGRESS; Authelia, n8n, CloudCLI, Codex CLI, Antigravity CLI, Stalwart and Bulwark accepted; Backrest, Semaphore, maintenance page and full private portal remain pending.