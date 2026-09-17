# Cloud Infrastructure — Current State

## Canonical checkpoint

**Current implementation stage:** Stage 2 — Edge Core Applications — **IN PROGRESS**  
**Current work branch:** `02 — Edge Core Applications`  
**Primary GitHub repository:** `Eugene-SN/Cloud-Infrastructure`

Stage 0 and Stage 1 are **COMPLETE / ACCEPTED**. `EDGE_STAGE1_FINAL_INTEGRATED_ACCEPTANCE=PASS` on 2026-09-17.

Current Stage 2 accepted application state includes clean-reinitialized Authelia, n8n and CloudCLI, fresh authorization for Codex CLI and Antigravity CLI, and the accepted production mail stack (Stalwart + Bulwark). Codex uses the official standalone runtime with managed Remote Control accepted server-side. Antigravity Remote Control is registered and running as the `core` user service with instance name `edge`; the user confirmed that `edge` is visible Online in the Antigravity Remote Control UI.

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
- Stage 1 baseline public listeners were TCP/22, TCP/80, TCP/443 and UDP/443; Stage 2 mail additionally exposes TCP/25, TCP/465 and TCP/993 on IPv4.

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

Protected namespace includes `app`, `n8n`, `backup`, `ops`, `docs`, `cloud`, `sync`, `code`, `chat.escloud.us`; legacy `go.escloud.us` removed. `mail.escloud.us` intentionally uses its native Stalwart/Bulwark authentication rather than Authelia.

## TLS / certificate lifecycle

Certificate `escloud.us`; Certbot `4.0.0`; lineage `/etc/letsencrypt/live/escloud.us`.

Current SANs: `escloud.us`, `app.escloud.us`, `auth.escloud.us`, `backup.escloud.us`, `chat.escloud.us`, `cloud.escloud.us`, `code.escloud.us`, `docs.escloud.us`, `mail.escloud.us`, `n8n.escloud.us`, `ops.escloud.us`, `sync.escloud.us`.

- Certbot timer active/enabled;
- deploy hook `/etc/letsencrypt/renewal-hooks/deploy/20-vpn-cert-sync`;
- hook synchronizes the shared certificate to Xray, Hysteria2 and Stalwart and restarts/revalidates their runtimes;
- `/opt/vpn-stack/state/web-domains.txt` SHA256 `cab0467df32ef5cbed2af58f0ac91624962632de84af8faf86286788ca4a7eb9`;
- `/opt/vpn-stack/scripts/maintctl` SHA256 `0e7b2b2f6b1a3b3d6563157520d15060e3c29ce64c94e147035a3beddced3257`;
- `maintctl web-check` PASS for accepted SAN names;
- current certificate fingerprint used by mail TLS acceptance: `3D:5A:77:15:78:4C:53:74:4B:D7:C2:6C:86:96:5B:10:DB:F9:7B:32:45:9A:F0:CD:B9:BD:39:A1:8B:9B:9B:F8`.

## Domain namespace

Canonical allocation: `DOMAIN_NAMESPACE.md`.

Active/current Stage 2 names: `escloud.us`, `edge.escloud.us`, `auth.escloud.us`, `n8n.escloud.us`, `code.escloud.us`, `mail.escloud.us`; allocated targets include `app`, `backup`, `ops.escloud.us`; `docs`, `chat`, `cloud`, `sync.escloud.us` remain reserved according to their planned stages. `go.escloud.us` is retired.

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
`STAGE2_ANTIGRAVITY_REMOTE_CONTROL_UI_ONLINE=PASS`

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
- user confirmed `edge` is visible Online in the Antigravity Remote Control Instances UI;
- authenticated Antigravity probe returned `ANTIGRAVITY_REMOTE_AUTH_OK`, RC `0` after Remote Control activation;
- Codex authorization and managed daemon remained healthy after Antigravity Remote Control activation;
- legacy custom `codex-app-server` and `codex-runner` remain absent; official Codex managed daemon replaces the legacy custom app-server service.

## Stage 2 mail — production accepted

`STAGE2_MAIL_PUBLIC_PROTOCOL_EXPOSURE_ACCEPTANCE=PASS`  
`STAGE2_MAIL_EXTERNAL_E2E_OUTBOUND_SEND=PASS`  
`STAGE2_MAIL_EXTERNAL_E2E_INBOUND_ACCEPTANCE=PASS`  
`STAGE2_MAIL_POST_ACCEPTANCE_CLEANUP=PASS`

### Runtime and paths

- Stalwart `0.16.22`, image `stalwartlabs/stalwart:v0.16`, deployed digest `sha256:388dcb75a70727c5b551249a6d34b1f1321294852489e4fa3a4e6be698b7c4f0`;
- Bulwark `1.9.2`, image `ghcr.io/bulwarkmail/webmail:1.9.2`, deployed digest `sha256:0e8d1339277033b6569a76c6f8192396e6edd66fd917d64d9ed505e8b81dac6d`;
- compose `/opt/mail-stack/compose.yaml`, accepted SHA256 `7de766ed23fd7c30f63870f25af648f018d3295685fb58e40b88eaa578d2d4de`;
- Stalwart state `/srv/mail/stalwart/etc` and `/srv/mail/stalwart/lib`;
- Bulwark state `/srv/mail/bulwark/{settings,admin,admin-state,telemetry}`;
- Stalwart admin backend `127.0.0.1:18083 -> 8080/tcp`;
- Bulwark backend `127.0.0.1:18084 -> 3000/tcp`;
- nginx vhost `/etc/nginx/sites-available/mail-escloud-us.conf`, SHA256 `601ff1feffcef8729901b1e00ab98001934db03a1315b55233965ba5d75f079c`;
- accepted split routing: default `/` -> Bulwark, Stalwart management/JMAP paths -> Stalwart;
- public webmail `https://mail.escloud.us/` redirects to Bulwark locale path; `/admin/` reaches Stalwart management UI;
- Stalwart and Bulwark `restart: unless-stopped`, running with zero restarts at final acceptance.

### Public mail protocol contract

- IPv4 Docker listeners: `0.0.0.0:25`, `0.0.0.0:465`, `0.0.0.0:993`;
- TCP/25 SMTP, TCP/465 implicit-TLS SMTP submission, TCP/993 IMAPS accepted end-to-end;
- TCP/587, TCP/995 and TCP/4190 are intentionally not published on the host;
- UFW contains Stage 2 mail ALLOW rules for TCP/25, TCP/465 and TCP/993; UFW also generated matching IPv6 rules, while Docker mail protocol publication is IPv4-only because `mail.escloud.us` currently has only an A record;
- SMTP/25 advertises STARTTLS and accepted SMTP feature set;
- SMTP/465 advertises `AUTH PLAIN LOGIN XOAUTH2 OAUTHBEARER` after TLS;
- IMAPS/993 advertises Stalwart IMAP4rev2/IMAP4rev1 capabilities;
- TCP/465 and TCP/993 serve the accepted shared `escloud.us` certificate with fingerprint `3D:5A:77:15:78:4C:53:74:4B:D7:C2:6C:86:96:5B:10:DB:F9:7B:32:45:9A:F0:CD:B9:BD:39:A1:8B:9B:9B:F8`.

### Mail identities and migrated data

- domain `escloud.us`;
- `es@escloud.us` (`Eugene S`) uses a new production password and retained useful mailbox/account data;
- migrated data includes 6 mailboxes and 14 messages plus address-book/calendar/identity state captured from the accepted legacy source;
- malformed legacy contact `Евгений Сидоренко <evg.sidorenko@gmail.com>` was reconstructed in target state with a new valid UID while preserving its useful content and Trusted Senders address-book relationship;
- legacy `admin@escloud.us` was directly audited: 0 emails and only default/automatic mailbox/address-book/calendar/identity state, so no useful admin data was migrated; target administrative credentials/state remain new;
- no legacy Stalwart user/admin credentials, Bulwark session secret, Bulwark admin auth state or legacy DKIM private key were reused;
- Bulwark uses a new session secret and newly bootstrapped persistent admin state; bootstrap password environment material was removed after persistence verification.

### DNS and external E2E acceptance

- MX `10 mail.escloud.us.`;
- `mail.escloud.us` A `45.92.156.17`, no mail AAAA record;
- PTR `45.92.156.17 -> mail.escloud.us`;
- SPF `v=spf1 ip4:45.92.156.17 -all`;
- DMARC `v=DMARC1; p=none; adkim=s; aspf=s`;
- active DKIM RSA selector `v1-rsa-20260917`;
- active DKIM Ed25519 selector `v1-ed25519-20260917`;
- legacy selector `v1-rsa-20260713` retired from both authoritative Cloudflare nameservers and recursive DNS after successful E2E acceptance;
- Gmail external outbound acceptance: SPF PASS, RSA DKIM PASS using `v1-rsa-20260917`, DMARC PASS; Gmail reported the additional Ed25519 signature as neutral/no-key but this did not affect RSA DKIM or DMARC acceptance;
- Gmail -> `es@escloud.us` inbound reply accepted through public SMTP/25 and read back through IMAPS/993; Stalwart recorded Gmail SPF PASS, DKIM PASS and DMARC PASS;
- external test reply `In-Reply-To`/`References` matched the exact outbound E2E Message-ID, proving bidirectional message flow through the new production stack.

### Cleanup / retained recovery state

- temporary Vandelay capture `/tmp/stalwart-vandelay-capture` was removed after final mail acceptance;
- temporary mail recovery containers/networks and bootstrap artifacts are absent;
- migration-preservation archive `/tmp/edge-migration-preservation-20260916T141048Z.tar.gz`, SHA256 `0203e5845f57bc1d04b384cef2b26a45fbff855c341e1edf1193034c34de9fdf`, remains intentionally retained through the remainder of Stage 2 because other legacy Stage 2 service settings/scenarios may still need reference material;
- mail production state remained non-regressed after DKIM retirement and Vandelay cleanup.

## Firewall

UFW remains accepted: active/enabled; default incoming deny, outgoing allow, routed deny. Current intentional ingress is TCP/22, TCP/80, TCP/443 and UDP/443 for the Stage 1 substrate plus Stage 2 mail TCP/25, TCP/465 and TCP/993. Docker firewall remains enabled; non-mail application services remain loopback-published by default.

## Recovery checkpoints

Stage 1 recovery archive:

- `/srv/backups/edge-stage1/edge-stage1-base-20260916T234611Z.tar.gz`;
- SHA256 `37486e763ddac4c5ef3a92a35c3dad49787d75ffd8b97499073c79af617cc566`.

External migration-preservation archive remains retained through the remainder of Stage 2 as technical reference/recovery input for still-pending legacy-derived service configuration. Do not restore application credentials from it. Remove it during final Stage 2 cleanup once no remaining task depends on it.

## Current stage boundary

Stage 0: **COMPLETE / ACCEPTED**.  
Stage 1: **COMPLETE / ACCEPTED**.  
Stage 2: **IN PROGRESS**.

Accepted Stage 2 components now include Authelia, n8n, CloudCLI, Codex CLI, Antigravity CLI, Stalwart and Bulwark mail. Pending Stage 2 work includes Backrest, Semaphore, maintenance page, and full private Cloud Infrastructure portal.

Canonical Obsidian vault remains on `ai-node` at `/srv/ai-data/knowledge/obsidian`.