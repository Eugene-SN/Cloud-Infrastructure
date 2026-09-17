# Cloud Infrastructure — Current State

## Canonical checkpoint

**Current implementation stage:** Stage 2 — Edge Core Applications — **IN PROGRESS**  
**Current work branch:** `02 — Edge Core Applications`  
**Primary GitHub repository:** `Eugene-SN/Cloud-Infrastructure`

Stage 0 and Stage 1 are **COMPLETE / ACCEPTED**. `EDGE_STAGE1_FINAL_INTEGRATED_ACCEPTANCE=PASS` on 2026-09-17. Stage 2 has begun; n8n is the first fully restored and integrated Stage 2 application component.

## Host

- logical node `edge`, FQDN `edge.escloud.us`;
- Ubuntu 26.04.1 LTS, kernel `7.0.0-31-generic`;
- KVM x86_64, 2 vCPU, ~15 GiB RAM;
- IPv4 `45.92.156.17/24`; IPv6 `2a0c:b847:ffff:283::a/64`;
- timezone `Europe/Moscow`;
- root SSH key-only through `ssh.socket`;
- 4 GiB swap;
- QEMU guest agent active;
- journald `SystemMaxUse=500M`.

`edge.escloud.us` public DNS is accepted as:

- A `45.92.156.17`;
- AAAA `2a0c:b847:ffff:283::a`.

## Runtime foundation

- Docker Engine `29.8.1`;
- Docker Compose `5.5.1`;
- containerd active;
- Docker `live-restore: true`;
- `/opt/<service>` runtime definitions/scripts;
- `/srv/<service>` persistent state;
- `/etc/<service>` host-native configuration;
- `/var/www/<site>` static roots.

Shared host service account:

- user/group `core`;
- UID/GID `1000:1000`;
- home `/home/core`, mode `0750`;
- password locked;
- no sudo and no Docker group membership;
- default owner for compatible application persistent state; preserve upstream container UID/GID when required.

## Stage 1 ingress / VPN foundation

### nginx

- nginx `1.28.3-2ubuntu1.11`;
- public TCP/80 IPv4/IPv6;
- loopback TLS fallback `127.0.0.1:8080 proxy_protocol`;
- ACME webroot `/var/www/letsencrypt`;
- public masking root `/var/www/escloud.us/public`.

### Xray / Hysteria2

- Xray `26.3.27`, host-native, owns public TCP/443 and falls back to nginx `127.0.0.1:8080` with `xver=1`;
- Hysteria2 `2.12.3`, host-native, owns public UDP/443, strict SNI guard, userpass auth;
- accepted public listeners remain TCP/22, TCP/80, TCP/443 and UDP/443 only.

### Authelia

- Authelia `4.39.27`;
- `/opt/authelia/compose.yaml`, persistent `/srv/authelia`;
- container `authelia`, `restart: unless-stopped`;
- loopback `127.0.0.1:19091 -> 9091/tcp`;
- current accepted state `running/healthy`;
- `auth.escloud.us` ingress is Xray -> nginx -> Authelia.

Current protected namespace rules include `app`, `n8n`, `backup`, `ops`, `docs`, `cloud`, `sync`, `code`, and `chat.escloud.us`; legacy `go.escloud.us` rule has been removed.

## TLS / certificate lifecycle

Certificate name: `escloud.us`; Certbot `4.0.0`; active lineage `/etc/letsencrypt/live/escloud.us`.

Accepted current SAN set:

- `escloud.us`;
- `app.escloud.us`;
- `auth.escloud.us`;
- `backup.escloud.us`;
- `chat.escloud.us`;
- `cloud.escloud.us`;
- `code.escloud.us`;
- `docs.escloud.us`;
- `mail.escloud.us`;
- `n8n.escloud.us`;
- `ops.escloud.us`;
- `sync.escloud.us`.

`go.escloud.us` is no longer part of the certificate target.

- Certbot timer active/enabled;
- deploy hook `/etc/letsencrypt/renewal-hooks/deploy/20-vpn-cert-sync`;
- Xray/Hysteria certificate fingerprints matched the live lineage after namespace normalization;
- manual certificate domain source `/opt/vpn-stack/state/web-domains.txt`, SHA256 `cab0467df32ef5cbed2af58f0ac91624962632de84af8faf86286788ca4a7eb9`;
- `/opt/vpn-stack/scripts/maintctl` SHA256 `0e7b2b2f6b1a3b3d6563157520d15060e3c29ce64c94e147035a3beddced3257`;
- `maintctl` primary domain file and fallback domain set match the accepted certificate SAN set; `maintctl web-check` passed for every accepted hostname.

## Domain namespace

Canonical allocation is documented in `DOMAIN_NAMESPACE.md`.

Active/current Stage 2 names:

- `escloud.us` — public masking page;
- `edge.escloud.us` — VPS infrastructure identity;
- `auth.escloud.us` — Authelia;
- `app.escloud.us` — future private Cloud Infrastructure portal;
- `n8n.escloud.us` — n8n;
- `code.escloud.us` — CloudCLI;
- `mail.escloud.us` — Stalwart + Bulwark;
- `backup.escloud.us` — Backrest;
- `ops.escloud.us` — Semaphore.

Reserved names:

- `docs.escloud.us` — future technical documentation library;
- `chat.escloud.us` — future service reserve;
- `cloud.escloud.us` — Stage 4 file-access layer;
- `sync.escloud.us` — Stage 4 synchronization layer.

Legacy `go.escloud.us` is retired from target configuration after accepted migration to `n8n.escloud.us`; its Cloudflare DNS record may be removed.

## n8n — Stage 2 accepted production state

`STAGE2_N8N_LOCAL_RESTORE_DEPLOYMENT=PASS`  
`STAGE2_N8N_PUBLIC_IDENTITY_MIGRATION=PASS`  
`STAGE2_N8N_INGRESS_DEPLOYMENT=PASS`  
`STAGE2_N8N_COMPONENT_ACCEPTANCE=PASS`  
`STAGE1_PRODUCTION_NON_REGRESSION=PASS`

Runtime:

- n8n `2.39.7`;
- OCI image `docker.n8n.io/n8nio/n8n:stable`;
- deployed image ID / repo digest `sha256:54323be085a6086acd87f612a25752d6582d3a0c0b07cc93c2b40a9356c3203b`;
- container `n8n`;
- restart policy `unless-stopped`;
- backend publish `127.0.0.1:15678 -> 5678/tcp` only;
- local readiness `/healthz/readiness` returned HTTP 200;
- public canonical URL `https://n8n.escloud.us/`;
- public HTTP redirects to HTTPS;
- HTTPS path is Xray TCP/443 -> nginx `127.0.0.1:8080` -> Authelia auth request -> n8n loopback backend;
- unauthenticated HTTPS request redirects to `https://auth.escloud.us/?rd=https://n8n.escloud.us/`;
- served TLS certificate contains `n8n.escloud.us`;
- no public TCP/15678 listener.

Paths and ownership:

- compose `/opt/n8n/compose.yaml`, root-owned mode `0644`, SHA256 `42009eb90d1411b168f4ff9fd072108021a8e9b2467f5c59a01bcf4dcc5ad5bf`;
- persistent state `/srv/n8n`, owned `core:core` / UID:GID `1000:1000`, directory mode `0750`;
- database `/srv/n8n/database.sqlite`, `core:core`, mode `0640`;
- n8n config `/srv/n8n/config`, `core:core`, mode `0600`, SHA256 `a3dbdaaed5a50616b46f55bc8cd02bef592f5ba14f26f3198c0e816769f12431`;
- nginx vhost `/etc/nginx/sites-available/n8n-escloud-us.conf`, enabled through `sites-enabled`, SHA256 `0c9e944233fa6243cb24f10d42157457d741f401bb555c62bb744382a03ed7ae`.

Preserved/restored application state after migration:

- SQLite quick/integrity checks `ok`;
- workflows `2`;
- credentials `1`;
- executions `0`;
- webhooks `0`;
- projects `1`;
- active workflows `0`;
- schema migrations `254`;
- latest migration `CreateAgentWorkflowDependencyTable1788522448804`;
- preserved credential decryptability gate PASS without exposing secret content.

n8n current identity variables:

- `N8N_HOST=n8n.escloud.us`;
- `N8N_PROTOCOL=https`;
- `WEBHOOK_URL=https://n8n.escloud.us/`;
- `N8N_EDITOR_BASE_URL=https://n8n.escloud.us/`.

The old `go.escloud.us` identity is no longer present in n8n runtime/compose, Authelia target policy, or certificate SANs.

## Firewall

UFW remains accepted from Stage 1:

- active/enabled;
- default incoming deny, outgoing allow, routed deny;
- inbound TCP/22, TCP/80, TCP/443, UDP/443 for IPv4/IPv6;
- Docker firewall rules enabled;
- application containers remain loopback-published by default.

## Recovery checkpoints

Stage 1 local recovery archive remains:

- `/srv/backups/edge-stage1/edge-stage1-base-20260916T234611Z.tar.gz`;
- SHA256 `37486e763ddac4c5ef3a92a35c3dad49787d75ffd8b97499073c79af617cc566`.

The external credential-bearing migration-preservation archive remains required during Stage 2 because other accepted services still need restoration/migration. Do not delete it after n8n alone.

## Current stage boundary

Stage 0: **COMPLETE / ACCEPTED**.  
Stage 1: **COMPLETE / ACCEPTED**.  
Stage 2: **IN PROGRESS**.

Accepted Stage 2 products still pending deployment/integration include Stalwart + Bulwark, CloudCLI, Codex CLI, Antigravity CLI, Backrest, Semaphore, maintenance page, and the full private Cloud Infrastructure portal.

Canonical Obsidian vault remains on `ai-node` at `/srv/ai-data/knowledge/obsidian`.
