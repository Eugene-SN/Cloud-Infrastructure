# Edge Maintenance

Current source for the single `edge` maintenance/update subsystem.

## Ownership model

Stage 07.2 uses **native-first ownership**:

- a supported upstream/vendor-native automatic lifecycle remains authoritative when production-safe;
- Maintenance/Semaphore owns only components whose updates remain operator-controlled;
- native-auto products are deliberately absent from Maintenance rather than represented as disabled or monitor-only update targets.

Native automatic owners outside Maintenance:

- `HERMES` — Hermes native cron updater plus conditional settlement timer;
- `CODEX` — Codex managed-daemon updater / `pid-update-loop`;
- `UBUNTU_SECURITY` — package-owned `apt-daily*` / `unattended-upgrades`.

Normal and third-party APT updates remain manual through `APT_EDGE`. Automatic reboot is disabled.

## Maintenance target model

Generated target model: `update_units_v5`.

Maintenance contains exactly 17 actionable manual targets:

`APT_EDGE`, `XRAY`, `HYSTERIA2`, `BACKREST`, `RESTIC`, `RCLONE`,
`SEMAPHORE`, `N8N`, `AUTHELIA`, `MATTERMOST`, `POSTGRESQL`,
`STALWART`, `BULWARK`, `NEXTCLOUD`, `NEXTCLOUD_POSTGRESQL`,
`NEXTCLOUD_REDIS`, `ANTIGRAVITY`.

`HERMES` and `CODEX` do not appear in raw Maintenance version rows,
`maintenance.json`, `actions.json`, the Maintenance dashboard or Semaphore
update templates.

`actions.json` contains exactly the 17 manual actions, has
`execution_mode=manual_only`, and `auto_update=false`.

`update.escloud.us` remains the operator launch surface. Semaphore is the
manual executor/orchestrator and has no autonomous update schedule.

## Stage 12 targets

Rclone uses upstream `rclone selfupdate --stable`, followed by restart of the
persistent `core` user service `projects-webdav.service`.

Nextcloud application, PostgreSQL and Redis are distinct manual Compose targets.
The Nextcloud application action recreates both `app` and `cron`.

Bulwark tracks upstream stable through `ghcr.io/bulwarkmail/webmail:latest`.
Changing the tracked tag does not itself update/recreate the running container;
the actual image update remains operator-triggered.

## Master Batch

Master Batch derives its 18-target plan from `config/update-units.json`.
Both real execution and `--plan-only` require the accepted schema-2
`/etc/edge-maintenance/manual-driver-enablement.json`.

Semaphore remains `individual_only` because updating the running orchestrator
inside its own batch could interrupt final acceptance.

## Monitoring integration

Stage 8 `edge-monitor` consumes
`/var/www/maintenance-status/maintenance.json` as the authoritative update
state. Therefore its `UPDATE_AVAILABLE` count represents manual Maintenance
updates, not native updater drift.

## Safety boundary

A manual component update requires:

- the target to be one of the 18 manifest units;
- schema-2 enablement to permit the target;
- a fresh `UPDATE_AVAILABLE` row;
- explicit operator initiation.

Read-only Refresh never chains into a component update.
