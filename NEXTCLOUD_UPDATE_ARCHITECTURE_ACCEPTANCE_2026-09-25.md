# Nextcloud Update Architecture Acceptance — 2026-09-25

Status: **COMPLETE / ACCEPTED**

Acceptance marker:

`NEXTCLOUD_UPDATE_ARCHITECTURE=PASS`

Confirmed runtime state at acceptance:

- installed Nextcloud runtime remains `34.0.4`;
- no real Nextcloud application update was executed;
- Maintenance discovery reports `UPDATE_AVAILABLE`;
- installed application version: `34.0.4`;
- latest stable application version: `35.0.1`;
- official deployment track selected by the implementation: `nextcloud:35.0-apache`;
- discovery source: `NEXTCLOUD_UPSTREAM_STABLE_AND_OFFICIAL_DOCKER`;
- framework contract verification passed;
- actions renderer maps `nextcloud_compose` to Docker and exposes the accepted executable action;
- dedicated Nextcloud driver preflight passed;
- update execution remains operator-initiated only.

The accepted architecture separates version discovery from deployment mechanics:

1. Maintenance resolves the latest stable Nextcloud Server release from authoritative upstream Nextcloud release metadata.
2. The official Docker image is used as the deployment artifact rather than as the authority for the latest stable application version.
3. Docker deployment follows the upstream Compose image replacement lifecycle.
4. Any upstream-required intermediate upgrade sequence is treated as execution procedure only and does not hide the final latest-stable target.
5. No update is executed without explicit operator initiation.

Evidence: `NEXTCLOUD_UPDATE_ARCHITECTURE_RECOVERY_V3` completed with `RC=0`.
