# Edge Stage 1 maintctl Restore Acceptance — 2026-09-17

**Status:** ACCEPTED / PASS  
**Stage:** Stage 1 — Base `edge` Platform  
**Work branch:** `01 — Edge Clean Rebuild & Base Platform Deployment`

## Acceptance result

`EDGE_STAGE1_MAINTCTL_RESTORE_ACCEPTANCE=PASS`

This is a subset acceptance inside Stage 1. Stage 1 remains **IN PROGRESS / NOT ACCEPTED**.

## Restored legacy maintenance entrypoints

Production script restored at:

- `/opt/vpn-stack/scripts/maintctl`

Legacy symlink entrypoints restored exactly as preserved:

- `/root/maintctl -> /opt/vpn-stack/scripts/maintctl`
- `/usr/local/bin/maintctl -> /opt/vpn-stack/scripts/maintctl`

`command -v maintctl` resolves to `/usr/local/bin/maintctl`.

## Source identity and controlled adaptation

Preserved source from the verified migration archive:

- size: `39627` bytes;
- SHA256: `8fe0d35cfee813f3a3ab5aca4f4188c22d9f0b70db8a61a0354293d7d6010d7f`.

Installed adapted script:

- size: `39634` bytes;
- SHA256: `00f2bbe70f5adbb981e7a49b455ce40ae4c34980ce0b6fbb3d92eeb8dcca9f5d`;
- mode: `0755`;
- owner/group: root/root.

The exact diff gate proved that only two lines changed from the preserved source:

- `CERT_HOOK` changed from `/etc/letsencrypt/renewal-hooks/deploy/xray-cert-sync.sh` to `/etc/letsencrypt/renewal-hooks/deploy/20-vpn-cert-sync`;
- `CERT_SYNC_SCRIPT` changed from `/usr/local/bin/xray-cert-sync.sh` to `/opt/vpn-stack/scripts/xray-cert-sync.sh`.

These two changes align maintctl with the already accepted Stage 1 certificate synchronization lifecycle. No other script logic was changed.

## Functional verification

- Bash syntax: PASS;
- legacy path residue: absent;
- `maintctl help`: PASS;
- `maintctl dashboard`: PASS;
- node identity displayed as `Edge` / `escloud.us`;
- nginx active;
- Xray active;
- Hysteria2 active;
- Certbot timer active;
- UFW active;
- public IPv4 resolved as `45.92.156.17`;
- DNS A for `escloud.us` resolved as `45.92.156.17`;
- preserved Xray user count: 2;
- preserved Hysteria2 user count: 2;
- failed systemd units: 0.

## Production non-regression

- Docker active;
- nginx active;
- Xray active;
- Hysteria2 active;
- UFW active;
- Authelia running/healthy;
- failed systemd units: 0.

## Remaining Stage 1 blocker

The intended historical `escloud.us — Private File Exchange` masking page has not yet been restored. The temporary 1376-byte `ES Cloud` page is not accepted as the Stage 1 public masking page. Do not create the final Stage 1 checkpoint or declare Stage 1 complete until the exact prior masking-page artifact is recovered and verified.
