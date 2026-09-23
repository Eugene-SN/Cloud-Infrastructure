# Stage 07.2 — Final Current-State Acceptance

Date: 2026-09-23  
Status: **COMPLETE / ACCEPTED**

## Scope

This record is the final current-state acceptance for Stage 07.2 after:

- the v5 native-first/manual-only ownership correction;
- recovery from the failed real Master Batch Task 23;
- successful real Master Batch Task 26;
- the subsequent cleanup/backup-rotation driver changes;
- final read-only reconciliation of canonical `main` against deployed runtime.

It supersedes the earlier Stage 07.2 acceptance records as **current authority**.
Those records remain historical evidence.

## Final runtime/canonical alignment

`STAGE07_2_FINAL_CURRENT_STATE_AUDIT_V1` completed with RC=0.

The deployed runtime matched the current `main` blobs for:

- `update-units.json`;
- `manual-update`;
- `update-github-binary`;
- `master-batch-update`;
- `master-health-validate`;
- `master-post-scan-validate`;
- `maintenance-targets-refresh`;
- `maintenance-actions-render`;
- Maintenance dashboard `index.html`.

Acceptance marker: `CANONICAL_RUNTIME_ALIGNMENT=PASS`.

## Final Maintenance model

- target model: `update_units_v5`;
- raw monitored rows: 25;
- manual Maintenance targets: 18;
- all 18 targets are actionable and `update_owner=maintenance_manual`;
- all 18 manual targets are `CURRENT`;
- `UPDATE_AVAILABLE=0`;
- `CHECK_FAILED=0`;
- Hermes and Codex remain absent from the Maintenance target/action model;
- actions contract remains manual-only with `auto_update=false`;
- Stage 8 reads `maintenance.json` as authoritative Maintenance state.

Current accepted versions observed by the final audit include:

- n8n `2.40.5`;
- Bulwark `1.10.0`;
- Antigravity `1.2.9`;
- Xray `26.3.27`;
- Hysteria2 `2.12.3`;
- Nextcloud `34.0.4`;
- Rclone `1.75.1`;
- Semaphore `2.19.12`.

## Real Master execution acceptance

Semaphore Task 26 is the accepted real execution proof:

- template ID 18;
- task status `success`;
- `MASTER_BATCH_DRIVER_RC=0`;
- `MASTER_BATCH_POST_SCAN_RC=0`;
- `MASTER_BATCH_HEALTH_RC=0`;
- `MASTER_BATCH_SUMMARY|TOTAL=18|SUCCESS=18|FAILED=0|FAILED_TARGETS=NONE`;
- `MASTER_POST_SCAN_GATE=PASS|MANUAL_TOTAL=18|MANUAL_CURRENT=18|REBOOT_REQUIRED=0`;
- `MASTER_HEALTH_GATE=PASS|SYSTEM_SERVICES=10|USER_SERVICES=4|DOCKER_UNITS=9|DOCKER_SERVICES=10|SQLITE_DATABASES=2|POSTGRES_READINESS=PASS`.

The final audit reran the current health validator and received the same health PASS.

## Native update owners

Native ownership remains non-regressed:

- Codex managed daemon: running, version `0.156.1`, native `pid-update-loop` active;
- Hermes native automatic update cron active, settlement timer loaded/active/enabled;
- Ubuntu `apt-daily.timer`, `apt-daily-upgrade.timer`, and `unattended-upgrades.service` loaded/active/enabled.

## Cleanup and rotation state

The current post-Task-26 cleanup model is accepted:

- APT autoremove candidates: 0;
- APT package archive: no cached `.deb` files;
- Docker dangling images: 0;
- Docker reported 0 reclaimable image space;
- `/usr/bin/rclone.old`: absent;
- `manual-update` contains the accepted schema-2, Compose orphan/image cleanup, DB backup rotation, APT cleanup and Rclone old-binary cleanup contracts;
- runtime `maintctl` contains Xray/Hysteria update-backup rotation retaining the two newest update backups.

The runtime `maintctl` implementation is host-native and is not represented as a file under `maintenance/edge`; this final audit verifies its relevant rotation behavior directly from the deployed runtime rather than claiming repo byte identity for that script.

## Final service state

- zero failed systemd units;
- nginx, Xray, Hysteria2, Backrest, Semaphore, NetBird, Docker, containerd, CloudCLI and edge-monitor active;
- Hermes gateway/dashboard, Antigravity daemon and `projects-webdav.service` active.

## Final markers

- `STAGE07_2_CORRECTIVE_MIGRATION=PASS`;
- `STAGE07_2_FINAL_MASTER_BATCH_EXECUTION=PASS`;
- `EDGE_MAINTENANCE_CLEANUP_ROTATION_ARCHITECTURE=PASS`;
- `STAGE07_2_CURRENT_STATE_AUDIT=PASS`.

**Final Stage 07.2 status: COMPLETE / ACCEPTED.**
