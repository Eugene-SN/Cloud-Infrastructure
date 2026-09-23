# Stage 07.2 — Final Native Update Ownership Reconciliation

Date: 2026-09-23  
Status: **COMPLETE / ACCEPTED**

## Final ownership contract

Stage 07.2 uses native-first ownership while keeping the Maintenance execution
plane strictly manual.

Native automatic owners outside Maintenance:

- **Hermes** — native Hermes cron updater plus conditional settlement timer;
- **Codex** — native managed-daemon updater / `pid-update-loop`;
- **Ubuntu security** — package-owned `apt-daily*` / `unattended-upgrades`.

Maintenance/Semaphore owns exactly 18 operator-controlled targets:

- `APT_EDGE`, Xray, Hysteria2, Backrest, Restic, Rclone, Semaphore;
- n8n, Authelia, Mattermost, Mattermost PostgreSQL, Stalwart, Bulwark;
- Nextcloud application, Nextcloud PostgreSQL, Nextcloud Redis;
- CloudCLI, Antigravity.

Normal and third-party APT remain manual through `APT_EDGE`; automatic reboot
remains disabled.

## Final Maintenance model

- target model: `update_units_v5`;
- raw status rows: 25;
- Maintenance rows: exactly 18;
- all 18 rows are actionable and have `update_owner=maintenance_manual`;
- Hermes and Codex are absent from raw Maintenance collection,
  `maintenance.json`, `actions.json`, the Maintenance dashboard and
  Semaphore update templates;
- `actions.json` schema 10 has exactly 18 components,
  `execution_mode=manual_only`, and `auto_update=false`;
- Master Batch and `--plan-only` both require schema-2 manual enablement;
- Stage 8 `edge-monitor` reads
  `/var/www/maintenance-status/maintenance.json` as authoritative update
  state, so its update count represents manual Maintenance updates rather than
  native updater drift.

Semaphore template mapping remains unchanged from the prior reconciliation:
Refresh 1, Master 18, Rclone 14, Nextcloud 16, Nextcloud PostgreSQL 19,
Nextcloud Redis 20. No Hermes/Codex update templates exist.

## Corrective acceptance

`STAGE07_2_MAINTENANCE_MANUAL_TARGET_MODEL_CORRECTION_V3` completed with RC=0.

Acceptance evidence:

- `RAW_STATUS_ACCEPTANCE=PASS`;
- `MAINTENANCE_MODEL_ACCEPTANCE=PASS`;
- `ACTION_CONTRACT_ACCEPTANCE=PASS`;
- `MASTER_CACHE_PRECHECK_GATE=PASS|TOTAL=18|CURRENT=14|UPDATE_AVAILABLE=4`;
- `MASTER_PLAN_ONLY_GATE=PASS`;
- `SEMAPHORE_NON_REGRESSION=PASS`;
- `NATIVE_OWNER_NON_REGRESSION=PASS`;
- `EDGE_MONITOR_SOURCE_ACCEPTANCE=PASS`;
- `SERVICE_NON_REGRESSION=PASS`;
- `SOURCE_CLEANLINESS=PASS`;
- `STAGE07_2_CORRECTIVE_MIGRATION=PASS`.

No real component update was executed by the corrective migration.

At final acceptance the four pending manual updates were:

- `APT_EDGE`: 11 packages;
- n8n `2.39.10 -> 2.40.5`;
- Bulwark `1.9.2 -> 1.10.0`;
- Antigravity `1.2.7 -> 1.2.8`.

These pending operator-controlled updates do not block Stage 07.2 acceptance.

## Supersession

This final record supersedes
`STAGE_07_2_NATIVE_UPDATE_OWNERSHIP_ACCEPTANCE_2026-09-23.md` as current
Stage 07.2 authority because the earlier v4 model incorrectly retained Hermes
and Codex as monitor-only Maintenance rows and contained a stale real Master
enablement schema check.

The earlier file is retained as historical evidence and is not rewritten.

Historical Stage 7 acceptance remains historical evidence; only conflicting
current ownership/model rules are superseded.
