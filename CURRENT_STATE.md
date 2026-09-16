# Cloud Infrastructure — Current State

## Snapshot status

**Current canonical work branch:** `01 — Edge Clean Rebuild & Base Platform Deployment`  
**Current implementation stage:** **Stage 1 — Base `edge` Platform — IN PROGRESS / NOT ACCEPTED**  
**Primary GitHub repository:** `Eugene-SN/Cloud-Infrastructure`

Stage 0 is complete. The clean provider rebuild and several Stage 1 foundation subsets are accepted, but Stage 1 as a whole is not yet accepted. Continue work in branch `01`; do not transition to a later branch until final Stage 1 deployment/non-regression acceptance.

Canonical implementation workflow and stage sequence: `IMPLEMENTATION_PHASES.md`.

## Stage 0 — complete / accepted

- legacy VPS audit and historical baseline complete;
- provider full-VPS backup complete;
- external sensitive migration archive verified;
- archive SHA256: `0203e5845f57bc1d04b384cef2b26a45fbff855c341e1edf1193034c34de9fdf`;
- sanitized `migration-reference/` accepted;
- clean provider-level rebuild selected and completed;
- recovery paths verified.

The sensitive archive remains outside GitHub and is the authoritative selective-recovery source for credential/private state. The provider backup remains the whole-VPS rollback path. Historical baseline artifacts remain unchanged.

## Stage 1 — accepted current runtime state

### Base OS / host

- logical node: `edge`;
- hostname/FQDN: `edge.escloud.us`;
- Ubuntu 26.04.1 LTS;
- kernel accepted at substrate stage: `7.0.0-31-generic`;
- x86_64 KVM VPS;
- 2 vCPU, ~15 GiB RAM;
- 4 GiB swap at `/swap.img`;
- root ext4 on `/dev/vda1`, ~155 GiB filesystem class;
- IPv4 `45.92.156.17/24`, gateway `45.92.156.1`;
- IPv6 `2a0c:b847:ffff:283::a/64`, gateway `2a0c:b847:ffff::1`;
- timezone intentionally retained as `Europe/Moscow`;
- SSH key-only root access accepted; password and keyboard-interactive auth disabled;
- OpenSSH socket activation via `ssh.socket` accepted;
- QEMU guest agent active;
- journald persistent-use ceiling `SystemMaxUse=500M`;
- provider cloud-init schema/deprecation warnings remain accepted/non-blocking because effective networking, swap and SSH are correct.

Accepted records include `EDGE_FRESH_OS_SUBSTRATE_ACCEPTANCE=PASS` and `EDGE_MINIMAL_BASE_BOOTSTRAP_ACCEPTANCE=PASS`.

### Docker foundation

`EDGE_STAGE1_DOCKER_FOUNDATION_ACCEPTANCE=PASS`.

Accepted runtime:

- Docker Engine `29.8.1` from the official Ubuntu resolute repository;
- Docker CLI `29.8.1`;
- containerd `2.3.5`;
- runc `1.5.1`;
- Buildx `0.37.1`;
- Docker Compose `5.5.1`;
- storage driver `overlayfs`;
- cgroup v2 / systemd driver;
- Docker root `/var/lib/docker`;
- `/etc/docker/daemon.json` contains `{"live-restore": true}`;
- Docker and containerd active/enabled;
- hello-world and Compose config tests passed;
- temporary Docker test artifacts removed.

Docker + Compose are the primary runtime for suitable application services. Host-native services remain allowed where materially simpler/better suited.

### nginx / HTTP / ACME foundation

`EDGE_STAGE1_NGINX_ACME_FOUNDATION_ACCEPTANCE=PASS`.

Accepted runtime:

- nginx `1.28.3-2ubuntu1.11`;
- public listeners TCP/80 IPv4/IPv6;
- loopback fallback listener `127.0.0.1:8080 proxy_protocol`;
- ACME webroot `/var/www/letsencrypt`;
- public webroot `/var/www/escloud.us/public`;
- `/health` endpoint returns `ok`;
- Proxy Protocol fallback path validated;
- current `index.html` is only a temporary neutral placeholder, not an accepted final decoy page.

### TLS / Certbot

`EDGE_STAGE1_TLS_CERTIFICATE_ACCEPTANCE=PASS`.

Accepted certificate:

- certificate name `escloud.us`;
- Certbot `4.0.0`;
- authenticator `webroot`;
- ECDSA P-256 / `secp256r1`;
- certificate `/etc/letsencrypt/live/escloud.us/fullchain.pem`;
- private key `/etc/letsencrypt/live/escloud.us/privkey.pem`;
- validity observed at acceptance: 2026-09-16 19:27:04 UTC through 2026-12-15 19:27:03 UTC;
- Certbot timer active/enabled;
- renewal dry-run PASS.

Accepted SAN set (10):

- `escloud.us`;
- `app.escloud.us`;
- `auth.escloud.us`;
- `chat.escloud.us`;
- `cloud.escloud.us`;
- `code.escloud.us`;
- `docs.escloud.us`;
- `go.escloud.us`;
- `mail.escloud.us`;
- `sync.escloud.us`.

### Xray runtime / VPN state

`EDGE_STAGE1_VPN_RUNTIME_FOUNDATION_ACCEPTANCE=PASS`.  
`EDGE_STAGE1_VPN_STATE_RENDER_ACCEPTANCE=PASS`.  
`EDGE_STAGE1_VPN_PUBLIC_ACCEPTANCE=PASS`.

Accepted Xray runtime:

- stable release resolved at deployment: `26.3.27`;
- binary `/usr/local/bin/xray`;
- release asset SHA256 verified: `23cd9af937744d97776ee35ecad4972cf4b2109d1e0fe6be9930467608f7c8ae`;
- systemd unit `/etc/systemd/system/xray.service`;
- service active and enabled;
- public listener TCP/443;
- preserved VLESS client count: 2;
- tag `vless-tls-edge`;
- TLS SNI `escloud.us`, ALPN `http/1.1`;
- fallback `127.0.0.1:8080`, Proxy Protocol `xver=1`;
- HTTPS through Xray → nginx fallback PASS;
- TLS verification PASS;
- `NRestarts=0` at public acceptance.

### Hysteria2 runtime / VPN state

Accepted Hysteria2 runtime:

- stable release resolved at deployment: `2.12.3`;
- binary `/usr/local/bin/hysteria`;
- release asset SHA256 verified: `8c7a68a906998b747a0db87586e364f995fbfddb95693ae6e2fdb68a6e920d3e`;
- systemd unit `/etc/systemd/system/hysteria-server.service`;
- service active and enabled;
- public listener UDP/443;
- preserved auth user count from CSV state: 2;
- `sniGuard: strict`;
- auth `userpass`;
- file masquerade rooted at `/var/www/escloud.us/public`;
- real local Hysteria client handshake using preserved primary credential PASS;
- HTTPS through the Hysteria tunnel returned HTTP 200;
- `NRestarts=0` at public acceptance.

### Preserved VPN state / tooling

Credential-bearing VPN state was selectively restored from the verified sensitive migration archive without regenerating credentials.

Current production state:

- `/opt/vpn-stack/state/services.env`;
- `/opt/vpn-stack/state/xray/users.csv`;
- `/opt/vpn-stack/state/hysteria2/users.csv`;
- `/opt/vpn-stack/conf/xray_primary_uuid.txt`;
- `/opt/vpn-stack/conf/hysteria2_primary.txt`;
- `/opt/vpn-stack/state/web-domains.txt`;
- `/opt/vpn-stack/scripts/vpnctl`.

Only node identity metadata was intentionally adapted:

- `DOMAIN=escloud.us` preserved;
- `NODE_CODE=edge`;
- `NODE_DISPLAY=Edge`;
- `XRAY_PORT=443` preserved;
- `HY2_PORT=443` preserved.

Xray UUID/password continuity and Hysteria2 credential continuity were verified against preserved CSV state and functionally verified after service start.

### Certificate synchronization lifecycle

`EDGE_STAGE1_CERT_SYNC_LIFECYCLE_ACCEPTANCE=PASS`.

Accepted lifecycle:

- sync script `/opt/vpn-stack/scripts/xray-cert-sync.sh`;
- Certbot deploy hook `/etc/letsencrypt/renewal-hooks/deploy/20-vpn-cert-sync`;
- renewed active certificate/key are copied into `/etc/xray/tls` and `/etc/hysteria/tls` with accepted ownership/modes;
- Xray and Hysteria2 are restarted after successful sync;
- service refresh errors are not suppressed;
- direct hook execution PASS;
- `certbot renew --cert-name escloud.us --dry-run --run-deploy-hooks` PASS;
- deploy hook execution during Certbot dry-run proven by service PID changes;
- active production certificate remained unchanged by staging dry-run;
- post-hook Xray TLS/fallback PASS;
- post-hook Hysteria handshake/proxy PASS;
- Certbot timer remains active/enabled.

### Current listener contract

Accepted public/service listeners now include:

- SSH TCP/22;
- nginx TCP/80;
- Xray TCP/443;
- Hysteria2 UDP/443;
- nginx loopback `127.0.0.1:8080` with Proxy Protocol.

There is intentionally no direct nginx TCP/443 listener because Xray owns TCP/443 and ordinary HTTPS reaches nginx through the Xray fallback path.

## Firewall current state

UFW is installed but currently **inactive** on the rebuilt host.

Legacy evidence proves the old VPS used UFW with default deny incoming and explicit SSH/HTTP/HTTPS/VPN/mail allowances. Whether/how to re-enable a minimal UFW policy on the new Docker-capable host remains a Stage 1 engineering decision because Docker published ports have special firewall semantics.

Do not add mail ports during Stage 1 unless required by an actually deployed Stage 1 service; mail belongs to a later stage.

## Stage 1 remaining work

Stage 1 is still **IN PROGRESS / NOT ACCEPTED**. Remaining work includes:

- decide/restore or explicitly replace the plausible public/decoy page; current page is temporary only;
- deploy/accept the Authelia common web-auth foundation using the preserved accepted scenario;
- decide and implement the minimal firewall/public exposure policy;
- finish any still-needed normalized persistent-directory/ownership conventions;
- define/implement the initial private Cloud Infrastructure page boundary required by Stage 1;
- take/verify the basic backup of the rebuilt base state required by Stage 1;
- verify the intended extension points for later WebUI/API/webhook/storage/Home/PAI/monitoring work;
- perform final Stage 1 composition and non-regression acceptance.

## Accepted-first implementation rule

For the remainder of the stage:

1. classify known/accepted implementation versus genuinely unresolved scope;
2. reconstruct accepted carry-forward components from preservation data;
3. deploy dependency-ready accepted components first;
4. research/select only genuinely unresolved mechanisms or actual incompatibilities;
5. verify/accept the remaining stage composition;
6. persist accepted state;
7. transition branches only after full Stage 1 acceptance.

Do not require re-selection of already accepted products from scratch.

## Accepted global product/direction anchors

Accepted without replacement research unless a concrete incompatibility or changed requirement appears:

- Xray;
- Hysteria2;
- nginx;
- n8n;
- CloudCLI;
- Stalwart;
- Bulwark;
- Authelia;
- Codex CLI;
- Antigravity CLI.

Additional accepted directions:

- Backrest using Restic for future backup management;
- dedicated Cloud Infrastructure portal replacing Homepage;
- maintenance page + Semaphore replacing the legacy custom Maintenance Center.

Canonical Obsidian vault remains on `ai-node` at `/srv/ai-data/knowledge/obsidian`; `edge` is not automatically a new canonical source of truth.

## Current branch / transition rule

Current canonical branch:

`01 — Edge Clean Rebuild & Base Platform Deployment`

Status:

**IN PROGRESS — public ingress/VPN/TLS foundation accepted; remaining Stage 1 platform components and final composition acceptance still pending.**

Do not transition to another branch until Stage 1 is fully deployed, verified and accepted.

After Stage 1 acceptance, the next branch should be `02 — Edge Core Applications`.
