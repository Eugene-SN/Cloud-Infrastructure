# Edge Maintenance

Current source for the single `edge` maintenance/update subsystem.

## Ownership model

Stage 07.2 uses a **native-first hybrid** ownership model:

- upstream/vendor-native automatic lifecycle remains authoritative when it is supported and production-safe;
- Maintenance/Semaphore is the manual update owner only for components without an accepted native automatic owner;
- native-owned components remain visible in status but are never exposed as competing manual update actions.

Current native-owned monitor-only targets:

- `CODEX` — Codex managed-daemon native updater;
- `HERMES` — Hermes native cron updater plus conditional settlement timer;
- Ubuntu security updates — package-owned `apt-daily*` / `unattended-upgrades`.

Normal and third-party APT updates remain manual through `APT_EDGE`. Automatic reboot is disabled.

## Manual update model

There are 18 manual update targets:

`APT_EDGE`, `XRAY`, `HYSTERIA2`, `BACKREST`, `RESTIC`, `RCLONE`,
`SEMAPHORE`, `N8N`, `AUTHELIA`, `MATTERMOST`, `POSTGRESQL`,
`STALWART`, `BULWARK`, `NEXTCLOUD`, `NEXTCLOUD_POSTGRESQL`,
`NEXTCLOUD_REDIS`, `CLOUDCLI`, `ANTIGRAVITY`.

`update.escloud.us` remains the single operator launch surface. Semaphore is the
manual backend executor/orchestrator and does not schedule real updates.

The four Stage 12 targets use the existing generic `playbooks/update-unit.yml`
path. Rclone updates with upstream `rclone selfupdate --stable` and then restarts
the `core` user service `projects-webdav.service`. Nextcloud application,
PostgreSQL and Redis are distinct Compose image targets.

Bulwark tracks upstream stable through `ghcr.io/bulwarkmail/webmail:latest`;
changing the tracked tag does not itself update/recreate the running container.
The actual image update remains operator-triggered through Maintenance.

## Generated contracts

`/var/www/maintenance-status/maintenance.json` uses target model
`update_units_v4`. It contains 18 actionable manual rows plus two monitor-only
native rows (`CODEX`, `HERMES`).

`/var/www/maintenance-status/actions.json` is generated from:

- `config/update-units.json`;
- `config/semaphore-templates.json`;
- root-owned `/etc/edge-maintenance/manual-driver-enablement.json`.

Unknown or disabled manual targets fail closed. Monitor-only targets have no
Semaphore template ID and are rendered as native-owned/non-executable.

Master Batch evaluates only the 18 manual targets. Semaphore remains
individual-only because self-updating the orchestrator inside its own batch can
interrupt final acceptance. A reboot-required state blocks clean Master
acceptance.

## APT policy

The old Stage 7 blanket manual-only APT override is superseded.

Package-owned `apt-daily.timer`, `apt-daily-upgrade.timer` and
`unattended-upgrades.service` are enabled for Ubuntu security updates.
Normal `-updates` and third-party package upgrades remain manual through
`APT_EDGE`; unattended automatic reboot remains disabled.

Do not reinstall the retired `99-edge-maintenance-manual-only` override or
re-mask package-owned APT lifecycle units unless a later accepted decision
explicitly supersedes Stage 07.2.

## Safety boundary

Real manual updates require an enabled target in
`/etc/edge-maintenance/manual-driver-enablement.json`, a fresh
`UPDATE_AVAILABLE` cache row, and operator initiation from
`update.escloud.us`.

Read-only refreshes may run independently; they never chain into real updates.
