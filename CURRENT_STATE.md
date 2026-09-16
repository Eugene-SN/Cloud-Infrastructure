# Cloud Infrastructure — Current State

## Canonical checkpoint

**Current implementation stage:** Stage 1 — Base `edge` Platform — **COMPLETE / ACCEPTED**  
**Completed work branch:** `01 — Edge Clean Rebuild & Base Platform Deployment`  
**Next work branch:** `02 — Edge Core Applications`  
**Primary GitHub repository:** `Eugene-SN/Cloud-Infrastructure`

`EDGE_STAGE1_FINAL_INTEGRATED_ACCEPTANCE=PASS` on 2026-09-17. Stage 1 production non-regression passed and no remaining Stage 1 runtime blocker is known.

## Host

- logical node: `edge`;
- FQDN: `edge.escloud.us`;
- Ubuntu 26.04.1 LTS;
- kernel `7.0.0-31-generic`;
- KVM x86_64, 2 vCPU, ~15 GiB RAM;
- root ext4 filesystem class ~155 GiB;
- swap `/swap.img` 4 GiB;
- IPv4 `45.92.156.17/24`, gateway `45.92.156.1`;
- IPv6 `2a0c:b847:ffff:283::a/64`, gateway `2a0c:b847:ffff::1`;
- timezone intentionally retained as `Europe/Moscow`;
- root SSH key-only access through accepted `ssh.socket` activation;
- QEMU guest agent active;
- journald `SystemMaxUse=500M`;
- system state `running`, failed units `0` at final Stage 1 acceptance.

## Runtime foundation

### Docker

- Docker Engine `29.8.1`;
- Docker Compose `5.5.1`;
- containerd active/enabled;
- Docker root `/var/lib/docker`;
- `/etc/docker/daemon.json` uses `live-restore: true`;
- Docker + Compose are the default runtime for suitable application services; host-native remains valid where materially simpler.

### Persistent layout contract

Accepted convention:

- `/opt/<service>` — runtime definitions/scripts;
- `/srv/<service>` — persistent application state;
- `/etc/<service>` — host-native configuration;
- `/var/www/<site>` — static web roots.

Current Stage 1 paths conform to this model, including `/opt/vpn-stack`, `/opt/authelia`, `/srv/authelia`, `/etc/xray`, `/etc/hysteria`, `/etc/nginx`, `/etc/letsencrypt`, `/var/www/escloud.us/public`, and `/var/www/letsencrypt`.

## Public ingress and VPN edge

### nginx

- nginx `1.28.3-2ubuntu1.11`;
- public TCP/80 IPv4/IPv6;
- loopback fallback `127.0.0.1:8080` with Proxy Protocol;
- ACME webroot `/var/www/letsencrypt`;
- public webroot `/var/www/escloud.us/public`;
- `/health` returns `ok`.

### Xray

- version `26.3.27`;
- host-native, active/enabled;
- owns public TCP/443;
- VLESS/TLS;
- fallback to nginx `127.0.0.1:8080` with `xver=1`;
- preserved client count: 2.

### Hysteria2

- version `2.12.3`;
- host-native, active/enabled;
- owns public UDP/443;
- `sniGuard: strict`;
- `userpass` authentication;
- masquerade root `/var/www/escloud.us/public`;
- preserved user count: 2.

### Public listener contract

Only these wildcard/public listeners are accepted at Stage 1:

- TCP/22 — SSH;
- TCP/80 — nginx;
- TCP/443 — Xray;
- UDP/443 — Hysteria2.

Expected loopback listeners include nginx `127.0.0.1:8080` and Authelia `127.0.0.1:19091`.

## TLS / certificate lifecycle

- certificate name `escloud.us`;
- Certbot `4.0.0`;
- ECDSA P-256;
- active lineage `/etc/letsencrypt/live/escloud.us`;
- SANs cover `escloud.us`, `app`, `auth`, `chat`, `cloud`, `code`, `docs`, `go`, `mail`, and `sync.escloud.us`;
- Certbot timer active/enabled;
- deploy hook `/etc/letsencrypt/renewal-hooks/deploy/20-vpn-cert-sync`;
- sync script `/opt/vpn-stack/scripts/xray-cert-sync.sh`;
- certificate copies for Xray/Hysteria2 verified;
- final Stage 1 certificate validity gate PASS.

## Public masking page

`EDGE_STAGE1_PUBLIC_MASKING_PAGE_ACCEPTANCE=PASS`.

Accepted page:

- `/var/www/escloud.us/public/index.html`;
- title `ES Cloud — Private Workspace`;
- size `22014` bytes;
- SHA256 `73ff3e57afa08c4f007f72902c1f2d3c8cf4e53920eabd10a86e32630106318e`;
- self-contained static implementation;
- all apparent navigation opens a local visual login/password dialog;
- entered values are not transmitted, stored or logged by page JavaScript.

The historical `escloud.us — Private File Exchange` page is no longer required for current Stage 1 recovery. The earlier 1376-byte temporary replacement remains rejected/superseded.

## Authelia / private-auth boundary

- Authelia `4.39.27`;
- Compose definition `/opt/authelia/compose.yaml`;
- persistent state `/srv/authelia`;
- container `authelia`, restart `unless-stopped`;
- loopback publish `127.0.0.1:19091 -> 9091/tcp`;
- current state `running/healthy` at acceptance;
- preserved user database/secrets retained;
- SQLite schema 29 accepted;
- `auth.escloud.us` HTTP redirects to HTTPS;
- HTTPS path is Xray TCP/443 -> nginx loopback fallback -> Authelia loopback backend;
- no direct public TCP/19091 exposure.

Stage 1 accepts this as the private authentication/ingress boundary. A full private Cloud Infrastructure portal is intentionally **deferred to Stage 2** rather than deploying a temporary portal that would immediately be replaced.

## Firewall

`EDGE_STAGE1_FIREWALL_ACCEPTANCE=PASS`.

- UFW active/enabled;
- logging low;
- default incoming deny;
- default outgoing allow;
- default routed deny;
- IPv6 enabled;
- allowed inbound: TCP/22, TCP/80, TCP/443, UDP/443 for IPv4 and IPv6;
- Docker-generated firewall rules remain enabled;
- application containers should remain loopback-published by default and use nginx/Xray ingress unless a later accepted design requires otherwise.

## VPN management carry-forward

Accepted scripts:

- `/opt/vpn-stack/scripts/maintctl` SHA256 `00f2bbe70f5adbb981e7a49b455ce40ae4c34980ce0b6fbb3d92eeb8dcca9f5d`;
- `/opt/vpn-stack/scripts/vpnctl` SHA256 `39363af55c71140cdd8fe7946fbcc228a958ad834e21b3ede9833cb0ec13b5b3`.

Accepted entrypoints:

- `/root/maintctl -> /opt/vpn-stack/scripts/maintctl`;
- `/usr/local/bin/maintctl -> /opt/vpn-stack/scripts/maintctl`;
- `/usr/local/bin/vpnctl -> /opt/vpn-stack/scripts/vpnctl`.

`maintctl` was preserved with exactly two accepted Stage 1 certificate-path adaptations. `maintctl help`, `maintctl dashboard`, and `vpnctl help` passed.

## Stage 1 recovery checkpoint

`EDGE_STAGE1_BASE_STATE_CHECKPOINT_ACCEPTANCE=PASS`.

Local same-VPS checkpoint:

- archive `/srv/backups/edge-stage1/edge-stage1-base-20260916T234611Z.tar.gz`;
- SHA256 `37486e763ddac4c5ef3a92a35c3dad49787d75ffd8b97499073c79af617cc566`;
- inventory and checksum files adjacent to the archive;
- archive integrity/readability PASS;
- critical archived file identities match live accepted state;
- Authelia was quiesced for consistent persistent-state capture and returned healthy.

This is a local base-state recovery checkpoint, not off-host DR. Future Backrest/Restic and off-site topology remain later-stage work.

Stage 0 provider full-VPS backup and external migration-preservation archive remain separate historical/recovery layers.

## Extension-point contract

Accepted Stage 1 extension points:

- public HTTP: nginx TCP/80;
- public HTTPS: Xray TCP/443 -> nginx `127.0.0.1:8080`;
- Hysteria2: UDP/443;
- private auth backend: Authelia `127.0.0.1:19091`;
- future application ingress: loopback backend -> nginx;
- runtime definitions: `/opt/<service>`;
- persistent state: `/srv/<service>`;
- host-native configuration: `/etc/<service>`;
- static roots: `/var/www/<site>`;
- Home/PAI connectivity is not a Stage 1 foundation dependency.

## Stage status and next branch

Stage 0: **COMPLETE / ACCEPTED**.  
Stage 1: **COMPLETE / ACCEPTED**.  
Final gate: `EDGE_STAGE1_FINAL_INTEGRATED_ACCEPTANCE=PASS`.

Next canonical work branch:

`02 — Edge Core Applications`

Stage 2 must follow the accepted-first workflow: reconstruct/deploy already accepted carry-forward applications where their implementation is known, and research only genuinely unresolved adjacent mechanisms. Current Stage 2 candidates include Stalwart, Bulwark, n8n, CloudCLI, Codex CLI, Antigravity CLI, Backrest, Semaphore, maintenance page, and the full private Cloud Infrastructure portal.

Canonical Obsidian remains on `ai-node` at `/srv/ai-data/knowledge/obsidian`; no Stage 1 acceptance changes that invariant.
