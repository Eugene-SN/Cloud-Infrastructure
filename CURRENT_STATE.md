# Cloud Infrastructure — Current State

## Snapshot status

**Current canonical work branch:** `01 — Edge Clean Rebuild & Base Platform Deployment`  
**Current implementation stage:** **Stage 1 — Base `edge` Platform — IN PROGRESS / NOT ACCEPTED**  
**Primary GitHub repository:** `Eugene-SN/Cloud-Infrastructure`

Stage 0 is complete. The rebuilt host substrate, Docker, nginx/ACME, TLS, Xray/Hysteria2, certificate synchronization, Authelia foundation/public ingress, and minimal host firewall are now accepted. Stage 1 still requires the remaining base-platform scope and final integrated acceptance before branch transition.

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
- provider cloud-init warnings remain accepted/non-blocking because effective networking, swap and SSH are correct.

Accepted records include `EDGE_FRESH_OS_SUBSTRATE_ACCEPTANCE=PASS` and `EDGE_MINIMAL_BASE_BOOTSTRAP_ACCEPTANCE=PASS`.

### Docker foundation

`EDGE_STAGE1_DOCKER_FOUNDATION_ACCEPTANCE=PASS`.

Accepted runtime:

- Docker Engine/CLI `29.8.1`;
- containerd `2.3.5`;
- runc `1.5.1`;
- Buildx `0.37.1`;
- Docker Compose `5.5.1`;
- storage driver `overlayfs`;
- cgroup v2 / systemd driver;
- Docker root `/var/lib/docker`;
- `/etc/docker/daemon.json`: `{"live-restore": true}`;
- Docker/containerd active and enabled.

Docker + Compose are the primary runtime for suitable application services. Host-native services remain allowed where materially simpler/better suited.

### nginx / HTTP / ACME

`EDGE_STAGE1_NGINX_ACME_FOUNDATION_ACCEPTANCE=PASS`.

Accepted runtime:

- nginx `1.28.3-2ubuntu1.11`;
- public TCP/80 IPv4/IPv6;
- loopback fallback `127.0.0.1:8080 proxy_protocol`;
- ACME webroot `/var/www/letsencrypt`;
- public webroot `/var/www/escloud.us/public`;
- `/health` returns `ok`;
- Proxy Protocol fallback validated;
- current `index.html` remains only a temporary neutral placeholder and is not yet the accepted final decoy/public page.

### TLS / Certbot / certificate sync

`EDGE_STAGE1_TLS_CERTIFICATE_ACCEPTANCE=PASS`.  
`EDGE_STAGE1_CERT_SYNC_LIFECYCLE_ACCEPTANCE=PASS`.

Accepted certificate/lifecycle:

- certificate name `escloud.us`;
- Certbot `4.0.0`;
- ECDSA P-256;
- active lineage `/etc/letsencrypt/live/escloud.us`;
- SANs: `escloud.us`, `app.escloud.us`, `auth.escloud.us`, `chat.escloud.us`, `cloud.escloud.us`, `code.escloud.us`, `docs.escloud.us`, `go.escloud.us`, `mail.escloud.us`, `sync.escloud.us`;
- Certbot timer active/enabled;
- deploy hook `/etc/letsencrypt/renewal-hooks/deploy/20-vpn-cert-sync`;
- sync script `/opt/vpn-stack/scripts/xray-cert-sync.sh`;
- certificate/key copies to Xray/Hysteria2 verified;
- `certbot renew --cert-name escloud.us --dry-run --run-deploy-hooks` PASS;
- post-hook Xray TLS/fallback and Hysteria authenticated proxy path PASS.

### Xray / Hysteria2 / preserved VPN state

`EDGE_STAGE1_VPN_RUNTIME_FOUNDATION_ACCEPTANCE=PASS`.  
`EDGE_STAGE1_VPN_STATE_RENDER_ACCEPTANCE=PASS`.  
`EDGE_STAGE1_VPN_PUBLIC_ACCEPTANCE=PASS`.

Xray:

- version `26.3.27`;
- active/enabled;
- public TCP/443;
- VLESS/TLS;
- tag `vless-tls-edge`;
- TLS SNI `escloud.us`, ALPN `http/1.1`;
- fallback `127.0.0.1:8080`, Proxy Protocol `xver=1`;
- preserved client count 2;
- functional HTTPS fallback PASS.

Hysteria2:

- version `2.12.3`;
- active/enabled;
- public UDP/443;
- `sniGuard: strict`;
- `userpass` auth;
- file masquerade `/var/www/escloud.us/public`;
- preserved auth user count 2;
- authenticated client handshake and HTTPS proxy test PASS.

Preserved VPN state is current under `/opt/vpn-stack`; credentials were not regenerated. Node identity was intentionally adapted to `NODE_CODE=edge`, `NODE_DISPLAY=Edge` while preserving `DOMAIN=escloud.us` and port contracts.

### Authelia foundation / public ingress

`EDGE_STAGE1_AUTHELIA_STATE_RESTORE_ACCEPTANCE=PASS`.  
`EDGE_STAGE1_AUTHELIA_LOCAL_RUNTIME_ACCEPTANCE=PASS`.  
`EDGE_STAGE1_AUTHELIA_PUBLIC_INGRESS_ACCEPTANCE=PASS`.

Accepted runtime:

- Authelia `4.39.27` from current stable `docker.io/authelia/authelia:latest` channel at deployment time;
- resolved image digest at restore time `sha256:40005803cd4e2eaeea4418517e9e9c7f515b55b31071a02829341ca2e50ca7c0`;
- runtime definition `/opt/authelia/compose.yaml`;
- persistent state `/srv/authelia`;
- container `authelia`, restart `unless-stopped`;
- loopback publish `127.0.0.1:19091 -> 9091/tcp` only;
- Docker health healthy;
- preserved file/Argon2 user database and three existing secrets retained;
- SQLite integrity PASS;
- first current-version start migrated SQLite schema 28 -> 29 successfully; schema 29 is now the accepted live state;
- explicit container restart acceptance PASS.

Public ingress:

- `auth.escloud.us` HTTP/80 redirects to HTTPS;
- HTTPS path: client -> Xray TCP/443 -> nginx `127.0.0.1:8080 proxy_protocol` -> Authelia `127.0.0.1:19091`;
- root and `/api/health` through public HTTPS PASS;
- TLS verification PASS;
- no direct public TCP/19091 exposure;
- unrelated future application vhosts remain intentionally undeployed.

### Firewall / public exposure

`EDGE_STAGE1_FIREWALL_ACCEPTANCE=PASS`.

Accepted UFW policy:

- UFW active and enabled;
- logging low;
- default incoming deny;
- default outgoing allow;
- default routed deny;
- IPv6 enabled;
- allowed host ingress for both IPv4 and IPv6:
  - `22/tcp` SSH;
  - `80/tcp` nginx/ACME;
  - `443/tcp` Xray;
  - `443/udp` Hysteria2.

Docker firewall interaction:

- Docker-generated rules remain enabled;
- FORWARD policy remains DROP;
- `DOCKER-USER` remains present and contains no custom rules;
- application containers should remain loopback-published by default and use the accepted nginx/Xray ingress path;
- current Authelia publication remains loopback-only.

Post-enable non-regression passed for active SSH session, SSH listener/socket, HTTP, public IPv4 HTTP/HTTPS, Xray fallback, Hysteria2 listener, Authelia HTTPS/runtime, Docker/nginx/Xray/Hysteria2 service state, and failed systemd units = 0.

## Current listener contract

Expected Stage 1 public listeners:

- SSH TCP/22;
- nginx TCP/80;
- Xray TCP/443;
- Hysteria2 UDP/443.

Expected loopback listeners:

- nginx `127.0.0.1:8080` Proxy Protocol fallback;
- Authelia `127.0.0.1:19091`.

There is intentionally no direct nginx TCP/443 listener because Xray owns TCP/443 and ordinary HTTPS reaches nginx through the Xray fallback path.

## Stage 1 remaining work

Stage 1 is still **IN PROGRESS / NOT ACCEPTED**. Remaining bounded scope:

- decide/restore or explicitly replace the plausible public/decoy page; current page is temporary only;
- finish any still-needed normalized persistent-directory/ownership conventions;
- define/implement the minimal initial private Cloud Infrastructure page boundary required for Stage 1, without pulling future application deployment into this stage;
- create and verify the basic backup/checkpoint of the rebuilt base state required by Stage 1;
- verify/document extension points for later WebUI/API/webhook/storage/Home/PAI/monitoring work;
- perform final Stage 1 composition/non-regression acceptance and persist the result.

Authelia and firewall are no longer pending Stage 1 items.

## Accepted-first implementation rule

For the remainder of the stage:

1. classify known/accepted implementation versus genuinely unresolved scope;
2. reconstruct accepted carry-forward components from preservation data;
3. deploy dependency-ready accepted components first;
4. research/select only genuinely unresolved mechanisms or actual incompatibilities;
5. verify/accept the remaining stage composition;
6. persist accepted state;
7. transition branches only after full Stage 1 acceptance.

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

**IN PROGRESS — host/public-edge foundation, Authelia, and firewall accepted; bounded remaining Stage 1 base-platform scope still pending.**

Do not transition to another branch until Stage 1 is fully deployed, verified and accepted.

After Stage 1 acceptance, the next branch should be `02 — Edge Core Applications`.
