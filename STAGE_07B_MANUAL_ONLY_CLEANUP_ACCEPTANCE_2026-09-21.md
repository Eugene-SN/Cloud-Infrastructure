# Stage 7B Manual-only Enforcement & Cleanup Acceptance — 2026-09-21

## Result

`STAGE07B_MANUAL_ONLY_CLEANUP=PASS`

Stage 7B — Edge Update Drivers & Recovery — is COMPLETE / ACCEPTED.

## Accepted runtime contract

- Every real update remains manually initiated from `update.escloud.us`.
- `/etc/apt/apt.conf.d/99-edge-maintenance-manual-only` is the canonical local
  APT override; all APT periodic actions resolve to `0`.
- `apt-daily.timer`, `apt-daily.service`, `apt-daily-upgrade.timer`,
  `apt-daily-upgrade.service` and `unattended-upgrades.service` are
  masked/inactive.
- The manual `APT_EDGE` driver remains functional because it invokes `apt-get`
  explicitly and does not depend on periodic units.
- Direct and Semaphore Refresh paths both use the single renderer at
  `/opt/edge-maintenance/scripts/maintenance-status-render`.
- `/var/www/maintenance-status/actions.json` is the only runtime action
  artifact and remains atomically generated from canonical inputs.

## Cleanup performed

- Removed inactive `/opt/edge-maintenance` playbook, dashboard and Semaphore
  installer payload plus the old README deployment copy.
- Removed the duplicate `/usr/local/bin/maintenance-status-render`.
- Removed 51 Stage 7 test/browser/HTTP artifacts from `/tmp` and generated
  Python bytecode caches.
- Removed the unused anonymous PostgreSQL probe volume.
- Removed all unused Docker images; total reclaimed space was approximately
  2.39 GB.
- Archived the unique Stage 4 scratch workspace before removing it:
  `/srv/backups/edge-stage4-work-final-20260921T1907.tar.gz`, SHA256
  `8e7f164526e0916ce0876b49ef51bb6609a0eef1553d366ed06c6e9470a88050`.
- Preserved Semaphore-managed repository checkouts and all intentional
  rollback/recovery backups.

## Verification

- Canonical Edge contract: PASS.
- Master Batch synthetic contract: PASS.
- Post-cleanup live read-only Refresh: PASS.
- Action targets: 16; monitored components: 23; unresolved/check-failed: 0;
  pending reboot: 0.
- Master health gate: PASS — 10 system services, 3 user services, 6 Docker
  targets, 2 SQLite databases and PostgreSQL readiness.
- nginx configuration: PASS.
- failed systemd units: 0.
- Docker: 6 active images for 6 running containers; 0 unused images; 0 local
  volumes; 0 reclaimable image bytes.
- Runtime action artifacts below `/opt` and `/var/www`: exactly 1.

One currently available Hermes upstream revision remains an ordinary pending
manual update, not an acceptance failure. Its execution remains operator-owned
through the Maintenance WebUI.
