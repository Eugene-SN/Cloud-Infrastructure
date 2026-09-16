# Edge Stage 1 Final Integrated Acceptance — 2026-09-17

**Status:** ACCEPTED / PASS  
**Stage:** Stage 1 — Base `edge` Platform  
**Completed work branch:** `01 — Edge Clean Rebuild & Base Platform Deployment`

## Final result

`EDGE_STAGE1_FINAL_INTEGRATED_ACCEPTANCE=PASS`

Stage 1 is **COMPLETE / ACCEPTED**.

## Verified final gates

The final integrated read-only acceptance returned RC=0 and verified:

- host identity `edge.escloud.us`;
- Ubuntu 26.04.1 LTS, kernel `7.0.0-31-generic`;
- timezone `Europe/Moscow` intentionally retained;
- system state `running`;
- failed systemd units `0`;
- Docker, containerd, nginx, Xray and Hysteria2 active/enabled;
- `ssh.socket` active/enabled;
- Certbot timer active/enabled;
- Docker `29.8.1`, Compose `5.5.1`, live-restore enabled;
- Authelia `running/healthy`, restart `unless-stopped`, loopback bind `127.0.0.1:19091`;
- persistent layout contract PASS;
- `maintctl` and `vpnctl` identities and convenience entrypoints PASS;
- nginx configuration PASS;
- accepted public masking page byte identity over HTTP and HTTPS PASS;
- HTTPS `/health` returns `ok`;
- `auth.escloud.us` HTTP redirect and HTTPS auth surface PASS;
- Xray public TCP/443 PASS;
- Hysteria2 public UDP/443 and masquerade-root contract PASS;
- UFW active;
- exact public listener set `tcp/22,tcp/80,tcp/443,udp/443`;
- certificate deploy-hook/sync lifecycle PASS;
- active certificate validity gate PASS;
- Stage 1 local checkpoint identity and integrity PASS;
- extension-point contract PASS;
- `maintctl dashboard` PASS;
- temporary acceptance artifacts cleaned;
- production non-regression PASS.

## Accepted Stage 1 composition

Stage 1 now provides the smallest stable standalone `edge` platform for later Cloud Infrastructure stages:

- clean supported Ubuntu substrate;
- stable host/network/SSH/firewall baseline;
- Docker + Compose application runtime foundation;
- normalized persistent path conventions;
- nginx public HTTP and loopback HTTPS fallback;
- shared `escloud.us` TLS lifecycle;
- Xray and Hysteria2 public VPN/DPI-bypass endpoints;
- accepted public masking/masquerade page;
- Authelia common private-auth foundation;
- restored operational VPN management entrypoints;
- local Stage 1 base-state recovery checkpoint;
- clean extension points for later application services.

## Private portal decision

The Stage 1 requirement for a private access boundary is satisfied by the accepted Authelia/public-ingress foundation.

A separate temporary private Cloud page is deliberately **not** deployed in Stage 1. The full dedicated Cloud Infrastructure portal remains Stage 2 scope, avoiding a disposable intermediate component.

## Recovery checkpoint

Accepted local same-VPS checkpoint:

- `/srv/backups/edge-stage1/edge-stage1-base-20260916T234611Z.tar.gz`;
- SHA256 `37486e763ddac4c5ef3a92a35c3dad49787d75ffd8b97499073c79af617cc566`.

This checkpoint is not off-host disaster recovery. Backrest/Restic and final repository/off-site topology remain later-stage work.

## Extension-point contract

- public HTTP: nginx TCP/80;
- public HTTPS: Xray TCP/443 -> nginx `127.0.0.1:8080`;
- Hysteria2: UDP/443;
- private auth backend: Authelia `127.0.0.1:19091`;
- future app ingress: loopback backend -> nginx;
- runtime definitions: `/opt/<service>`;
- persistent application state: `/srv/<service>`;
- host-native config: `/etc/<service>`;
- static roots: `/var/www/<site>`;
- Home/PAI connectivity remains outside Stage 1 foundation.

## Branch transition

Branch `01 — Edge Clean Rebuild & Base Platform Deployment` is complete.

The next canonical branch is:

`02 — Edge Core Applications`

Stage 2 must use the accepted-first workflow and must not reopen accepted Stage 1 architecture absent a concrete incompatibility or new requirement.
