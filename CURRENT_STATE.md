# Cloud Infrastructure — Current State

## Canonical checkpoint

**Stage 0 — COMPLETE / ACCEPTED**  
**Stage 1 — COMPLETE / ACCEPTED**  
**Stage 2 — Edge Core Applications — COMPLETE / ACCEPTED**  
**Stage 02.5 — Remaining Functional Scope Reconciliation & Research — ACTIVE / RESEARCH-ONLY**

`EDGE_STAGE2_FINAL_INTEGRATED_ACCEPTANCE=PASS` on 2026-09-17.

Current work branch: `02.5 — Remaining Functional Scope Reconciliation & Research`.

Primary repository: `Eugene-SN/Cloud-Infrastructure`.

The accepted Stage 2 production set is Authelia, n8n, CloudCLI, Codex CLI, Antigravity CLI, Stalwart and Bulwark.

Stage 02.5 has selected **Hermes Agent** as the only `Remaining Standalone Core Service`. The future Stage 3 is `03 — Edge Hermes Agent Runtime`; Hermes is not yet installed because Stage 02.5 remains research-only and must finish all required research/deliverables before any new production branch opens.

Accepted Hermes direction:

- persistent cloud-side agent runtime on `edge`;
- runs in parallel with n8n, not as a replacement;
- preferred host-native placement under `core`;
- Docker is not preferred because direct reuse of the existing host-native Codex/Antigravity executors and their user/runtime context would otherwise require unnecessary bridging;
- Stage 3 verifies `n8n -> Hermes -> Codex/AGY -> Hermes -> n8n` as an infrastructure path;
- Hermes access to local vLLM on `ai-node` is deferred until cross-site connectivity is accepted;
- user-specific n8n/Hermes workflows remain post-infrastructure work.

## Accepted remaining roadmap direction

Planned dependency order after Stage 02.5:

1. **Stage 3 — Edge Hermes Agent Runtime**;
2. **Stage 4 — Edge Cross-site Connectivity Foundation**;
3. **Stage 5 — Edge Cross-site Data & Knowledge Services**;
4. **Stage 6 — Edge Remaining Infrastructure Services** only if Stage 02.5 selects another full service; remove/renumber if empty;
5. **Stage 7 — Edge Backrest & Recovery**;
6. **Stage 8 — Edge Maintenance & Update** with Semaphore and a dedicated Codex substage for `update.escloud.us`;
7. **Stage 9 — Edge Monitoring, Heartbeats & Alerts** against the substantially complete infrastructure;
8. **Stage 10 — Edge Cloud Portal** with a dedicated Codex substage for `app.escloud.us`;
9. **Stage 11 — Edge Final Integrated Infrastructure Acceptance** and cleanup;
10. post-infrastructure **Automation & User Workflows** as a continuous workstream rather than an infrastructure-completion stage.

Backrest-before-Semaphore remains mandatory. Production monitoring remains late so it is built once against the final inventory. `update.escloud.us` and `app.escloud.us` remain separate UI responsibilities.

## Host / foundation

- logical node/FQDN: `edge.escloud.us`;
- Ubuntu 26.04.1 LTS, kernel `7.0.0-31-generic`;
- KVM x86_64, 2 vCPU, ~15 GiB RAM, 4 GiB swap;
- IPv4 `45.92.156.17/24`, IPv6 `2a0c:b847:ffff:283::a/64`;
- timezone `Europe/Moscow`;
- root SSH key-only through `ssh.socket`;
- Docker Engine `29.8.1`, Compose `5.5.1`, containerd;
- nginx `1.28.3-2ubuntu1.11`;
- Xray `26.3.27` on public TCP/443 with nginx fallback;
- Hysteria2 `2.12.3` on public UDP/443;
- UFW active: default deny incoming, allow outgoing, deny routed;
- intentional public TCP listeners: 22, 80, 443, 25, 465, 993; UDP 443;
- application WebUI backends remain loopback-only unless explicitly accepted otherwise.

Shared service account `core`: UID/GID `1000:1000`, password locked, no sudo/docker group. `core` linger is enabled for Antigravity Remote Control; `user@1000.service` and `/run/user/1000/bus` are accepted runtime dependencies.

## Authentication / ingress

### Authelia

- version `4.39.27`;
- compose `/opt/authelia/compose.yaml`, SHA256 `265dc881294e4b14bf9da5b529570ff6a2f234de2a3e335681d34d3deb447e96`;
- state `/srv/authelia`;
- backend `127.0.0.1:19091 -> 9091`;
- fresh operator `eugene`, fresh JWT/session/storage-encryption secrets;
- no legacy password/session/TOTP/WebAuthn/auth state reused;
- public `auth.escloud.us` accepted.

Protected private web namespace includes `n8n`, `code`, future `app`, `backup`, `ops`, `update`, `docs`, `cloud`, `sync`, `chat`. `mail.escloud.us` intentionally uses native mail-stack authentication.

## TLS

Shared Certbot lineage: `/etc/letsencrypt/live/escloud.us`.

Current SAN set includes `escloud.us`, `app`, `auth`, `backup`, `chat`, `cloud`, `code`, `docs`, `mail`, `n8n`, `ops`, `sync.escloud.us`. `update.escloud.us` has been added in Cloudflare for the future dedicated maintenance/update page; certificate/ingress activation is deferred until its deployment stage.

Certbot deploy hook synchronizes/reloads Xray, Hysteria2 and Stalwart. Accepted mail TLS fingerprint:

`3D:5A:77:15:78:4C:53:74:4B:D7:C2:6C:86:96:5B:10:DB:F9:7B:32:45:9A:F0:CD:B9:BD:39:A1:8B:9B:9B:F8`

## Stage 2 applications

### n8n

- `2.39.7`;
- image digest `sha256:54323be085a6086acd87f612a25752d6582d3a0c0b07cc93c2b40a9356c3203b`;
- compose SHA256 `42009eb90d1411b168f4ff9fd072108021a8e9b2467f5c59a01bcf4dcc5ad5bf`;
- backend `127.0.0.1:15678` only;
- public `https://n8n.escloud.us/` through Authelia;
- clean state: one new owner; workflows/credentials/executions/webhooks all zero at acceptance;
- no legacy auth/credential/project state restored.

### CloudCLI

- `1.37.3` under `/home/core/.local`;
- systemd unit SHA256 `8bf303e000b3de0f5a761fc0a466139a75e72fd6ec5d07b08ab7cb82f95382af`;
- backend `127.0.0.1:18140` only;
- public `https://code.escloud.us/` through Authelia;
- one new local user; projects/sessions/user_credentials zero at acceptance;
- no legacy CloudCLI auth/session state restored.

### Codex CLI

- `0.154.0` official standalone runtime;
- launcher `/home/core/.local/bin/codex` -> `/home/core/.codex/packages/standalone/current/bin/codex`;
- fresh ChatGPT authorization;
- managed Remote Control enabled through Unix control socket only;
- no public Codex network listener;
- legacy custom `codex-app-server` / `codex-runner` absent.

### Antigravity CLI

- `1.2.5`;
- fresh Google OAuth;
- Remote Control instance `edge`;
- user service `/home/core/.config/systemd/user/antigravity-cli-daemon.service` active/enabled with `NRestarts=0` at final Stage 2 acceptance;
- user confirmed `edge` Online in the Antigravity UI.

## Mail — production accepted

### Runtime

- Stalwart `0.16.22`, digest `sha256:388dcb75a70727c5b551249a6d34b1f1321294852489e4fa3a4e6be698b7c4f0`;
- Bulwark `1.9.2`, digest `sha256:0e8d1339277033b6569a76c6f8192396e6edd66fd917d64d9ed505e8b81dac6d`;
- compose `/opt/mail-stack/compose.yaml`, SHA256 `7de766ed23fd7c30f63870f25af648f018d3295685fb58e40b88eaa578d2d4de`;
- nginx vhost SHA256 `601ff1feffcef8729901b1e00ab98001934db03a1315b55233965ba5d75f079c`;
- loopback web backends: Stalwart `127.0.0.1:18083`, Bulwark `127.0.0.1:18084`;
- public mail protocols: IPv4 TCP/25 SMTP, TCP/465 SMTPS submission, TCP/993 IMAPS;
- 587/995/4190 intentionally unpublished.

### Data / auth

- `es@escloud.us` retained useful mailbox/account data with a new password;
- 6 mailboxes and 14 messages migrated plus useful address-book/calendar/identity state;
- malformed legacy contact reconstructed with a new valid UID;
- legacy `admin@escloud.us` contained no useful message data and was not migrated;
- new Stalwart user/admin credentials, new Bulwark session/admin state, new DKIM key material;
- no legacy authentication/session/private-key state reused.

### DNS / E2E

- MX `10 mail.escloud.us.`;
- A `45.92.156.17`, no mail AAAA;
- PTR `45.92.156.17 -> mail.escloud.us`;
- SPF `v=spf1 ip4:45.92.156.17 -all`;
- DMARC `v=DMARC1; p=none; adkim=s; aspf=s`;
- active DKIM selectors `v1-rsa-20260917` and `v1-ed25519-20260917`;
- legacy selector `v1-rsa-20260713` retired;
- Gmail outbound delivery: SPF PASS, RSA DKIM PASS, DMARC PASS;
- Gmail inbound reply: delivery PASS and Stalwart SPF/DKIM/DMARC PASS;
- bidirectional mail E2E acceptance PASS.

## Stage 2 final integrated acceptance

Final recovery run proved:

- foundation services active;
- Authelia/n8n/Stalwart/Bulwark containers running with zero restarts;
- CloudCLI active with zero restarts;
- Antigravity user service active/enabled with zero restarts;
- all application WebUI backends bound only to loopback;
- intentional public listener/UFW contract correct;
- public routes for `auth`, `n8n`, `code`, `mail` correct;
- local readiness/health checks correct;
- SMTP/TLS/DNS/DKIM identity non-regressed;
- accepted config hashes unchanged;
- no production mutation performed by acceptance runs.

`EDGE_STAGE2_FINAL_INTEGRATED_ACCEPTANCE=PASS`

The V1 and V2 acceptance interruptions were diagnostic-script defects only (root-to-user systemd bus context and an unanchored public-listener regex). They did not mutate or regress production state.

## Recovery / temporary state

- Stage 1 recovery archive: `/srv/backups/edge-stage1/edge-stage1-base-20260916T234611Z.tar.gz`, SHA256 `37486e763ddac4c5ef3a92a35c3dad49787d75ffd8b97499073c79af617cc566`;
- temporary Vandelay migration directory removed;
- authoritative migration-preservation archive `/tmp/edge-migration-preservation-20260916T141048Z.tar.gz`, SHA256 `0203e5845f57bc1d04b384cef2b26a45fbff855c341e1edf1193034c34de9fdf`, intentionally retained beyond Stage 2 because later functional stages may still need legacy configuration/reference material; do not restore legacy credentials from it.

Canonical Obsidian vault remains on `ai-node` at `/srv/ai-data/knowledge/obsidian`.

## Current next research block

**Cross-site Connectivity Foundation — базовая связь `edge ↔ ai-node ↔ PVE/Home`.**

Stage 02.5 must research and accept the required flows and transport before Stage 3 deployment is opened; Stage 3 itself remains the first planned post-02.5 production branch.