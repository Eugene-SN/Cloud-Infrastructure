# Edge Stage 1 Base-State Checkpoint Acceptance — 2026-09-17

**Status:** ACCEPTED / PASS  
**Stage:** Stage 1 — Base `edge` Platform  
**Work branch:** `01 — Edge Clean Rebuild & Base Platform Deployment`

## Acceptance result

`EDGE_STAGE1_BASE_STATE_CHECKPOINT_ACCEPTANCE=PASS`

This is a subset acceptance inside Stage 1. Stage 1 remains **IN PROGRESS / NOT ACCEPTED** until final integrated acceptance and canonical-state persistence are complete.

## Checkpoint identity

Local checkpoint:

- type: `LOCAL_BASE_STATE_RECOVERY_CHECKPOINT`;
- archive: `/srv/backups/edge-stage1/edge-stage1-base-20260916T234611Z.tar.gz`;
- size: `96838` bytes;
- SHA256: `37486e763ddac4c5ef3a92a35c3dad49787d75ffd8b97499073c79af617cc566`;
- inventory: `/srv/backups/edge-stage1/edge-stage1-base-20260916T234611Z.tar.gz.inventory.txt`;
- checksum: `/srv/backups/edge-stage1/edge-stage1-base-20260916T234611Z.tar.gz.sha256`;
- archive entry count: `148`.

Archive/checksum/inventory are local runtime recovery artifacts and are not committed to GitHub.

## Captured Stage 1 scope

The checkpoint includes the accepted Stage 1 base configuration/state needed for reconstruction, including:

- `/opt/vpn-stack`;
- `/opt/authelia`;
- `/srv/authelia`;
- Docker daemon configuration;
- nginx;
- Certbot/Let's Encrypt state;
- Xray;
- Hysteria2;
- UFW;
- SSH and netplan reference configuration;
- Xray/Hysteria systemd units;
- journald drop-in configuration;
- public masking page;
- ACME webroot;
- `maintctl` and `vpnctl` convenience entrypoints;
- checkpoint runtime manifest and source list.

## Consistency and integrity

Authelia was healthy before capture, stopped cleanly for consistent persistent-state capture, and returned to `running/healthy` afterward.

Verification passed:

- gzip integrity: PASS;
- tar readability: PASS;
- all required Stage 1 content gates: PASS;
- accepted masking page archive SHA256 equals live SHA256 `73ff3e57afa08c4f007f72902c1f2d3c8cf4e53920eabd10a86e32630106318e`;
- archived `maintctl` SHA256 equals live SHA256 `00f2bbe70f5adbb981e7a49b455ce40ae4c34980ce0b6fbb3d92eeb8dcca9f5d`;
- archived `vpnctl` SHA256 equals live SHA256 `39363af55c71140cdd8fe7946fbcc228a958ad834e21b3ede9833cb0ec13b5b3`;
- `CRITICAL_ARCHIVE_IDENTITY=PASS`.

## Production non-regression

After checkpoint creation:

- nginx configuration test: PASS;
- Docker active;
- nginx active;
- Xray active;
- Hysteria2 active;
- UFW active;
- Authelia `running/healthy`;
- HTTPS `/health` returns `ok`;
- public masking page served through HTTPS has the accepted SHA256;
- failed systemd units: `0`;
- `PRODUCTION_NON_REGRESSION=PASS`.

## Scope boundary

This is deliberately a **same-VPS local Stage 1 recovery checkpoint**. It is not off-host disaster recovery and does not replace the accepted future Backrest/Restic direction. Whole-VPS provider backup and the Stage 0 external preservation archive remain separate recovery layers. Full backup orchestration/off-site topology remains later-stage work.
