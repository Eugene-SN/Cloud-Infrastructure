# Edge Maintenance

Current contract (2026-10-01 after Plane Part 1): 16 manual targets, 9 Docker units, 23 monitored components. PLANE is an official-release unit using `plane_compose`, manual helper `scripts/update-plane`, Git playbook `playbooks/updates/plane.yml`, and Semaphore template 21. Current/latest stable v1.4.2 CURRENT; preflight checks native vendor/site graphs, public routes/variables and actual Backrest recovery contents, and real updates require a completed backup before migration. No scheduled Plane update. Full contract: `../../deployments/plane/README.md`; acceptance: `../../PLANE_PART_1_ACCEPTANCE_2026-10-01.md`. Shared PostgreSQL and every other update driver remain. Earlier stage target counts below are historical checkpoints.

Current source for the single `edge` maintenance/update subsystem.

## Ownership model

Stage 07.2 uses **native-first ownership**:

- a supported upstream/vendor-native automatic lifecycle remains authoritative when production-safe;
- Maintenance/Semaphore owns only components whose updates remain operator-controlled;
- native-auto products are deliberately absent from Maintenance rather than represented as disabled or monitor-only update targets.

Native automatic owners outside Maintenance:

- `HERMES` — Hermes native cron updater plus conditional settlement timer;
- `CODEX` — Codex managed-daemon updater / `pid-update-loop`;
- `UBUNTU_SECURITY` — package-owned `apt-daily*` / `unattended-upgrades`;
- `ANTIGRAVITY` — upstream-native background self-updater.

Normal and third-party APT updates remain manual through `APT_EDGE`. Automatic reboot is disabled.

## Maintenance target model

Generated target model: `update_units_v5`.

Maintenance contains exactly 16 actionable manual targets:

`APT_EDGE`, `XRAY`, `HYSTERIA2`, `BACKREST`, `RESTIC`, `RCLONE`,
`SEMAPHORE`, `N8N`, `AUTHELIA`, `MATTERMOST`, `POSTGRESQL`,
`STALWART`, `BULWARK`, `NEXTCLOUD`, `PLANE`,
`NEXTCLOUD_REDIS`.

`HERMES`, `CODEX` and `ANTIGRAVITY` do not appear in raw Maintenance version rows,
`maintenance.json`, `actions.json`, the Maintenance dashboard or Semaphore
update templates.

`actions.json` contains exactly the 16 manual actions, has
`execution_mode=manual_only`, and `auto_update=false`.

`update.escloud.us` remains the operator launch surface. Semaphore is the
manual executor/orchestrator and has no autonomous update schedule.

## Stage 12 targets

Rclone uses upstream `rclone selfupdate --stable`, followed by restart of the
persistent `core` user service `projects-webdav.service`.

Nextcloud application, shared PostgreSQL and Redis are distinct manual Compose targets; Plane reuses the shared PostgreSQL unit and has its own coherent release unit.
The Nextcloud application action recreates both `app` and `cron`.

Bulwark tracks upstream stable through `ghcr.io/bulwarkmail/webmail:latest`.
Changing the tracked tag does not itself update/recreate the running container;
the actual image update remains operator-triggered.

## Master Batch

Master Batch derives its 16-target plan from `config/update-units.json`.
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

- the target to be one of the 16 manifest units;
- schema-2 enablement to permit the target;
- a fresh `UPDATE_AVAILABLE` row;
- explicit operator initiation.

Read-only Refresh never chains into a component update.
