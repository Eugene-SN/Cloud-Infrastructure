# Edge Stage 1 Docker Foundation Acceptance — 2026-09-16

**Status:** ACCEPTED / PASS  
**Stage:** Stage 1 — Base `edge` Platform  
**Work branch:** `01 — Edge Clean Rebuild & Base Platform Deployment`

## Acceptance result

`EDGE_STAGE1_DOCKER_FOUNDATION_ACCEPTANCE=PASS`

This is a subset acceptance inside Stage 1. Stage 1 remains **IN PROGRESS / NOT ACCEPTED**.

## Accepted runtime state

Installed from the official Docker Ubuntu `resolute` stable repository:

- Docker Engine `29.8.1` (`docker-ce 5:29.8.1-1~ubuntu.26.04~resolute`);
- Docker CLI `29.8.1`;
- containerd `2.3.5`;
- runc `1.5.1`;
- Docker Buildx `0.37.1`;
- Docker Compose `5.5.1`.

Runtime properties verified:

- storage driver: `overlayfs`;
- cgroup driver: `systemd`;
- cgroup version: `2`;
- Docker root: `/var/lib/docker`;
- `live-restore: true` configured in `/etc/docker/daemon.json`;
- Docker daemon configuration validation: PASS;
- `docker.service`: active/enabled;
- `containerd.service`: active/enabled;
- Docker Engine functional `hello-world` test: PASS;
- Docker Compose config test: PASS;
- all temporary acceptance container/image/files removed after test.

Additional accepted foundation packages installed:

- Certbot `4.0.0-4` — installed but not yet configured;
- qrencode `4.1.1-2build1` — installed for preserved VPN user/QR workflow.

## Network / firewall non-regression

- UFW remained installed but inactive; no firewall policy was applied in this subphase.
- Docker created its normal forwarding chains, including `DOCKER-USER` and `DOCKER-FORWARD`.
- No application container remains running after acceptance tests.
- Public listeners remained limited to the pre-existing SSH listener on TCP/22 plus local system resolver/chrony sockets.
- SSH key-only access remained intact.
- System state remained `running` with zero failed systemd units.

Two `networkctl` errors for short-lived `veth*` interfaces occurred while the temporary Docker test container/network was being removed. They are classified as transient container-lifecycle noise, not a host-network regression. A separate SSH `kex_exchange_identification: Connection reset by peer` entry did not affect accepted SSH access/state.

## Deferred from this subphase

Not yet deployed/configured:

- nginx;
- Certbot certificate issuance/renewal contract;
- Xray;
- Hysteria2;
- public decoy page;
- Authelia;
- UFW policy;
- Stage 1 persistent application layout and remaining base-state backup.

## Next accepted-first activity

Continue reconstructing the preserved legacy public-edge baseline in dependency order:

1. nginx + public decoy + ACME webroot;
2. verify DNS and intended certificate SAN set;
3. configure/issue the `escloud.us` certificate and renewal path;
4. restore/adapt Xray TCP/443 fallback contract;
5. restore/adapt Hysteria2 UDP/443 masquerade contract;
6. restore/adapt VPN state/tooling;
7. deploy Authelia foundation;
8. then resolve remaining genuinely unresolved Stage 1 items.
