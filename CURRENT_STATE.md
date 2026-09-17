# Cloud Infrastructure — Current State

## Canonical checkpoint

**Current implementation stage:** Stage 2 — Edge Core Applications — **IN PROGRESS**  
**Current work branch:** `02 — Edge Core Applications`  
**Primary GitHub repository:** `Eugene-SN/Cloud-Infrastructure`

Stage 0 and Stage 1 are **COMPLETE / ACCEPTED**. `EDGE_STAGE1_FINAL_INTEGRATED_ACCEPTANCE=PASS` on 2026-09-17.

Current Stage 2 accepted application state includes clean-reinitialized Authelia, n8n and CloudCLI plus fresh authorization for Codex CLI and Antigravity CLI. Codex uses the official standalone runtime with managed Remote Control accepted server-side. Antigravity Remote Control is registered and running as the `core` user service with instance name `edge`.

## Stage 2 rebuild / credential policy

Current accepted rebuild rule:

- application authentication credentials are recreated fresh for **every service without exception**;
- legacy usernames/password hashes, passwords, API tokens, OAuth/session state and application auth databases are not restored as production credentials;
- services may preserve useful non-authentication configuration/data only where explicitly required;
- **mail is the data-preservation exception, not a credential exception**: preserve the existing useful mailbox/account identity, addresses/aliases, mailbox data and required mail settings/state, but create new mail-user and administrative authentication credentials;
- native application credentials behind Authelia remain new and unique; Authelia is the primary human-facing Web UI gate where applicable;
- migration-preservation material remains reference/recovery input and is not automatically restored into production auth state.

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

`edge.escloud.us` DNS: A `45.92.156.17`, AAAA `2a0c:b847:ffff:283::a`.

## Runtime foundation

- Docker Engine `29.8.1`;
- Docker Compose `5.5.1`;
- containerd active;
- Docker `live-restore: true`;
- `/opt/<service>` runtime definitions/scripts;
- `/srv/<service>` persistent state;
- `/etc/<service>` host-native configuration;
- `/var/www/<site>` static roots.

Shared service account `core`: UID/GID `1000:1000`, home `/home/core` mode `0750`, password locked, no sudo/docker group. `loginctl` linger is enabled for `core` because Antigravity Remote Control is a persistent systemd user service; `user@1000.service` and `/run/user/1000/bus` are active/present at acceptance.

## Stage 1 ingress / VPN foundation

### nginx

- nginx `1.28.3-2ubuntu1.11`;
- public TCP/80 IPv4/IPv6;
- loopback TLS fallback `127.0.0.1:8080 proxy_protocol`;
- ACME webroot `/var/www/letsencrypt`;
- public masking root `/var/www/escloud.us/public`.

### Xray / Hysteria2

- Xray `26.3.27`, host-native, public TCP/443, fallback to nginx `127.0.0.1:8080` with `xver=1`;
- Hysteria2 `2.12.3`, host-native, public UDP/443, strict SNI guard, userpass auth;
- accepted public listeners: TCP/22, TCP/80, TCP/443, UDP/443 only.

### Authelia — clean accepted state

`STAGE2_AUTHELIA_CLEAN_REINITIALIZATION=PASS`  
`STAGE1_PRODUCTION_NON_REGRESSION=PASS`

- Authelia `4.39.27`;
- compose `/opt/authelia/compose.yaml`, SHA256 `265dc881294e4b14bf9da5b529570ff6a2f234de2a3e335681d34d3deb447e96`;
- persistent root `/srv/authelia`;
- container `authelia`, `restart: unless-stopped`, `running/healthy`;
- loopback `127.0.0.1:19091 -> 9091/tcp`;
- public `auth.escloud.us` via Xray -> nginx -> Authelia;
- configuration `/srv/authelia/config/configuration.yml`, SHA256 `4c5343de85783bb0ed4973722f36df73c550708b7ffc48b2292f95aef6d62574`;
- fresh operator account `eugene` created with a new Argon2id password hash;
- legacy user/password hash, session/TOTP/WebAuthn/preferences/storage state removed;
- JWT/session/storage-encryption secrets regenerated;
- current user DB SHA256 `7d3407a469ca5755056e60508b553511f5792e114640c69ea3e60062a81daff9`;
- clean storage DB SHA256 after reinitialization `d06edef4c052839e25f0b2cb79f12e1350ba4ce14b6cdf9cf5ec78691081ae0d`;
- temporary recovery archive from reinitialization removed after acceptance.

Protected namespace includes `app`, `n8n`, `backup`, `ops`, `docs`, `cloud`, `sync`, `code`, `chat.escloud.us`; legacy `go.escloud.us` removed.

## TLS / certificate lifecycle

Certificate `escloud.us`; Certbot `4.0.0`; lineage `/etc/letsencrypt/live/escloud.us`.

Current SANs: `escloud.us`, `app.escloud.us`, `auth.escloud.us`, `backup.escloud.us`, `chat.escloud.us`, `cloud.escloud.us`, `code.escloud.us`, `docs.escloud.us`, `mail.escloud.us`, `n8n.escloud.us`, `ops.escloud.us`, `sync.escloud.us`.

- Certbot timer active/enabled;
- deploy hook `/etc/letsencrypt/renewal-hooks/deploy/20-vpn-cert-sync`;
- `/opt/vpn-stack/state/web-domains.txt` SHA256 `cab0467df32ef5cbed2af58f0ac91624962632de84af8faf86286788ca4a7eb9`;
- `/opt/vpn-stack/scripts/maintctl` SHA256 `0e7b2b2f6b1a3b3d6563157520d15060e3c29ce64c94e147035a3beddced3257`;
- `maintctl web-check` PASS for accepted SAN names.

## Domain namespace

Canonical allocation: `DOMAIN_NAMESPACE.md`.

Active/current Stage 2 names: `escloud.us`, `edge.escloud.us`, `auth.escloud.us`, `n8n.escloud.us`, `code.escloud.us`; allocated targets include `app`, `mail`, `backup`, `ops.escloud.us`; `docs`, `chat`, `cloud`, `sync.escloud.us` remain reserved according to their planned stages. `go.escloud.us` is retired.

## n8n — clean accepted Stage 2 state

`STAGE2_N8N_CLEAN_REINITIALIZATION=PASS`  
`STAGE2_N8N_BOOTSTRAP_OWNER_STATE=PASS`  
`STAGE2_N8N_POST_ONBOARDING_ACCEPTANCE=PASS`  
`STAGE2_NEW_APPLICATION_CREDENTIAL_POLICY=PASS`

Runtime:

- n8n `2.39.7`;
- image `docker.n8n.io/n8nio/n8n:stable`;
- deployed image ID/repo digest `sha256:54323be085a6086acd87f612a25752d6582d3a0c0b07cc93c2b40a9356c3203b`;
- container `n8n`, `restart: unless-stopped`, `running/healthy`;
- backend `127.0.0.1:15678 -> 5678/tcp` only;
- readiness `/healthz/readiness` HTTP 200;
- public `https://n8n.escloud.us/` through Xray -> nginx -> Authelia -> loopback backend;
- unauthenticated HTTPS redirects to `https://auth.escloud.us/?rd=https://n8n.escloud.us/`;
- no public TCP/15678 listener.

Paths:

- compose `/opt/n8n/compose.yaml`, SHA256 `42009eb90d1411b168f4ff9fd072108021a8e9b2467f5c59a01bcf4dcc5ad5bf`;
- state `/srv/n8n`, `core:core` UID:GID `1000:1000`;
- database `/srv/n8n/database.sqlite`, current post-onboarding SHA256 `b7e3a41780dbcb65d214fca4484ad68910c5e34649c368507dd77c08af89d0c4`;
- config `/srv/n8n/config`, SHA256 `48887ced0df600f4b20f93062414fa585448cda2c9c1b89176a1ecb5ea89b11f`;
- fresh encryption-key SHA256 `be3df4bce01e664d188d2be5d781e52fe8d923eeb2b98b387b56b92f5ae6c284`;
- nginx vhost `/etc/nginx/sites-available/n8n-escloud-us.conf`, SHA256 `0c9e944233fa6243cb24f10d42157457d741f401bb555c62bb744382a03ed7ae`.

Current clean application state after fresh owner onboarding:

- users `1` — new owner account with new password;
- workflows `0`;
- credentials `0`;
- executions `0`;
- webhooks `0`;
- legacy workflows/credential/project/auth state removed;
- retained recovery archive from failed V1 acceptance was removed after successful recovery V2.

Identity variables remain `N8N_HOST=n8n.escloud.us`, `N8N_PROTOCOL=https`, `WEBHOOK_URL=https://n8n.escloud.us/`, `N8N_EDITOR_BASE_URL=https://n8n.escloud.us/`.

## CloudCLI — clean accepted Stage 2 state

`STAGE2_CLOUDCLI_LOCAL_RUNTIME_DEPLOYMENT=PASS`  
`STAGE2_CLOUDCLI_INGRESS_DEPLOYMENT=PASS`  
`STAGE2_CLOUDCLI_PRE_ONBOARDING_ACCEPTANCE=PASS`  
`STAGE2_CLOUDCLI_POST_ONBOARDING_ACCEPTANCE=PASS`

- CloudCLI `1.37.3` installed for `core` under `/home/core/.local`;
- systemd unit `/etc/systemd/system/cloudcli.service`, SHA256 `8bf303e000b3de0f5a761fc0a466139a75e72fd6ec5d07b08ab7cb82f95382af`;
- service active/enabled, `NRestarts=0` at deployment acceptance;
- working directory `/srv/ai-workspace`, `core:core`, mode `0750`;
- backend strictly `127.0.0.1:18140`;
- persistent DB `/home/core/.cloudcli/auth.db`;
- public `https://code.escloud.us/` through Xray -> nginx -> Authelia -> loopback backend;
- nginx vhost `/etc/nginx/sites-available/code-escloud-us.conf`, SHA256 `6e6bd9f82fa9ea0f8bc576b6e4d71fcf583abef4b748c6326a7a2a7ca8de1896`;
- fresh local CloudCLI user exists with populated new `password_hash` and username;
- current post-onboarding DB SHA256 `8ae972e3e0183ed9f17f7138d9e63cfa169be043f7345f29ce6857cee72874a8`;
- clean state at post-onboarding acceptance: users `1`, projects `0`, sessions `0`, `user_credentials` `0`;
- no legacy CloudCLI auth DB/config/workspace/session state restored.

## Cloud AI CLI tooling — fresh authorization and Remote Control accepted

`STAGE2_CODEX_FRESH_CHATGPT_AUTH=PASS`  
`STAGE2_CODEX_CLEAN_STANDALONE_REINSTALL=PASS`  
`STAGE2_CODEX_SINGLE_INSTALL=PASS`  
`STAGE2_CODEX_MANAGED_DAEMON=PASS`  
`STAGE2_CODEX_REMOTE_CONTROL_ENABLED=PASS`  
`STAGE2_CODEX_REMOTE_CONTROL_SERVER_ACCEPTANCE=PASS`  
`STAGE2_CODEX_STANDALONE_RUNTIME_ACCEPTANCE=PASS`  
`STAGE2_ANTIGRAVITY_FRESH_GOOGLE_AUTH=PASS`  
`STAGE2_ANTIGRAVITY_USER_MANAGER_RECOVERY=PASS`  
`STAGE2_ANTIGRAVITY_REMOTE_CONTROL_REGISTERED=PASS`  
`STAGE2_ANTIGRAVITY_REMOTE_CONTROL_RUNNING=PASS`  
`STAGE2_ANTIGRAVITY_HEADLESS_LINGER=PASS`

- Node `22.22.1`;
- npm `9.2.0`;
- Codex CLI `0.154.0` uses the official standalone installation layout; earlier npm `@openai/codex` runtime removed;
- launcher `/home/core/.local/bin/codex` -> `/home/core/.codex/packages/standalone/current/bin/codex`;
- fresh ChatGPT device authorization preserved across reinstall; `codex login status` reports `Logged in using ChatGPT`;
- Codex auth object `/home/core/.codex/auth.json`, `core:core`, mode `0600`; no legacy Codex auth/config restored;
- Codex managed app-server backend `pid`, auto-update enabled, Remote Control enabled;
- managed path `/home/core/.codex/packages/standalone/current/bin/codex`, CLI/app-server version `0.154.0`;
- managed processes: `codex app-server --remote-control --listen unix://` and `codex app-server daemon pid-update-loop`;
- local control socket `/home/core/.codex/app-server-control/app-server-control.sock`, `core:core`, mode `0600`;
- no Codex/app-server public network listener exposed;
- Codex Remote Control manual pairing configured by the user on iPhone, MacBook and iPad; server-side acceptance PASS, while a client-originated end-to-end remote task has not yet been separately recorded as accepted evidence;
- Antigravity CLI `1.2.5` at `/home/core/.local/bin/agy`;
- Antigravity fresh Google OAuth completed successfully under `core`;
- Antigravity OAuth state stored under `/home/core/.gemini/antigravity-cli`; credential contents not persisted in project documentation;
- Antigravity Remote Control instance name `edge`;
- `/home/core/.config/systemd/user/antigravity-cli-daemon.service` is enabled and active/running;
- active daemon command `/home/core/.local/bin/agy remote-control serve`;
- `core` linger enabled so the user service persists on the headless VPS; `user@1000.service` active and user bus present;
- `agy remote-control status` reports daemon `active` and instance name `edge`;
- authenticated Antigravity probe returned `ANTIGRAVITY_REMOTE_AUTH_OK`, RC `0` after Remote Control activation;
- Codex authorization and managed daemon remained healthy after Antigravity Remote Control activation;
- legacy custom `codex-app-server` and `codex-runner` remain absent; official Codex managed daemon replaces the legacy custom app-server service.

## Firewall

UFW remains accepted: active/enabled; default incoming deny, outgoing allow, routed deny; inbound TCP/22, TCP/80, TCP/443 and UDP/443 for IPv4/IPv6; Docker firewall enabled; application services loopback-published by default.

## Recovery checkpoints

Stage 1 recovery archive:

- `/srv/backups/edge-stage1/edge-stage1-base-20260916T234611Z.tar.gz`;
- SHA256 `37486e763ddac4c5ef3a92a35c3dad49787d75ffd8b97499073c79af617cc566`.

External migration-preservation archive remains required during Stage 2 primarily for mail data/settings reconstruction. Do not restore its application credentials into production.

## Current stage boundary

Stage 0: **COMPLETE / ACCEPTED**.  
Stage 1: **COMPLETE / ACCEPTED**.  
Stage 2: **IN PROGRESS**.

Pending Stage 2 work includes Stalwart + Bulwark mail migration with new credentials, Backrest, Semaphore, maintenance page, and full private Cloud Infrastructure portal.

Canonical Obsidian vault remains on `ai-node` at `/srv/ai-data/knowledge/obsidian`.
