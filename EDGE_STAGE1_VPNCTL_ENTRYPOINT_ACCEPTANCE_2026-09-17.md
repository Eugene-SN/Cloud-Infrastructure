# Edge Stage 1 vpnctl Entrypoint Acceptance — 2026-09-17

**Status:** ACCEPTED / PASS  
**Stage:** Stage 1 — Base `edge` Platform  
**Work branch:** `01 — Edge Clean Rebuild & Base Platform Deployment`

## Acceptance result

`EDGE_STAGE1_VPNCTL_ENTRYPOINT_ACCEPTANCE=PASS`

This is a subset acceptance inside Stage 1. Stage 1 remains **IN PROGRESS / NOT ACCEPTED** until the remaining base-platform scope and final integrated acceptance are complete.

## Restored entrypoint

Preserved production script:

- `/opt/vpn-stack/scripts/vpnctl`
- SHA256 `39363af55c71140cdd8fe7946fbcc228a958ad834e21b3ede9833cb0ec13b5b3`

Restored legacy convenience symlink:

- `/usr/local/bin/vpnctl -> /opt/vpn-stack/scripts/vpnctl`

`command -v vpnctl` resolves to `/usr/local/bin/vpnctl`.

## Functional verification

- target file exists and is executable: PASS;
- symlink identity: PASS;
- command resolution: PASS;
- `vpnctl help`: PASS.

## Production non-regression

- nginx active;
- Xray active;
- Hysteria2 active;
- Docker active;
- Authelia `running/healthy`;
- failed systemd units: `0`;
- `PRODUCTION_NON_REGRESSION=PASS`.

## Scope boundary

This acceptance restores only the historical `vpnctl` global entrypoint that was missed during Stage 1 reconstruction. It does not by itself complete Stage 1.
